"""
Test synthesizer for merging clustered tests using LLM
Two-phase synthesis: cluster-level → final unification
"""

import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from loguru import logger

from app.config import config
from app.utils.exceptions import SynthesisError
from app.utils.streaming import StreamingQueue, SSEStream


class TestSynthesizer:
    """Synthesizes final tests from clusters using two-phase LLM approach"""

    def __init__(self, streaming_queue: Optional[StreamingQueue] = None):
        self.streaming_queue = streaming_queue
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=config.REQUEST_TIMEOUT)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def synthesize_clusters_individually(
            self,
            clusters: Dict[int, Dict[str, Any]],
            function_name: str,
            function_code: str
    ) -> List[str]:
        """
        PHASE 1: Synthesize each cluster into a single high-quality test
        ⚠️ DOES NOT STREAM - processes silently in background

        Args:
            clusters: Dictionary mapping cluster_id to cluster data (tests, category)
            function_name: Name of the function being tested
            function_code: Source code of the function

        Returns:
            List of synthesized test codes, one per cluster
        """
        if not clusters:
            raise SynthesisError("No clusters provided for synthesis")

        # Send synthesis start event
        if self.streaming_queue:
            await self.streaming_queue.put(
                await SSEStream.send_synthesis_start_event(
                    clusters_to_synthesize=len(clusters)
                )
            )

        logger.info(f"Phase 1: Synthesizing {len(clusters)} clusters individually (no streaming)")

        # Process clusters concurrently
        tasks = []
        for cluster_id, cluster_data in clusters.items():
            task = self._synthesize_single_cluster(
                cluster_id=cluster_id,
                cluster_tests=cluster_data["tests"],
                category=cluster_data["category"],
                function_name=function_name,
                function_code=function_code,
                stream_thinking=False  # ✅ DISABLED for Phase 1
            )
            tasks.append(task)

        # Wait for all cluster syntheses to complete
        synthesized_tests = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out errors
        valid_tests = []
        for idx, result in enumerate(synthesized_tests):
            if isinstance(result, Exception):
                logger.error(f"Cluster {idx} synthesis failed: {result}")
            elif result:
                valid_tests.append(result)

        logger.info(f"Successfully synthesized {len(valid_tests)} out of {len(clusters)} clusters")

        return valid_tests

    async def _synthesize_single_cluster(
            self,
            cluster_id: int,
            cluster_tests: List[str],
            category: str,
            function_name: str,
            function_code: str,
            stream_thinking: bool = False  # ✅ NEW parameter
    ) -> str:
        """
        Synthesize a single cluster into one comprehensive test

        Args:
            cluster_id: Cluster identifier
            cluster_tests: List of test codes in this cluster
            category: Test category (positive/negative/edge/etc.)
            function_name: Function being tested
            function_code: Source code of the function
            stream_thinking: Whether to stream thinking chunks

        Returns:
            Synthesized test code for this cluster
        """
        logger.info(f"Synthesizing cluster {cluster_id} ({len(cluster_tests)} tests, category: {category})")

        # Build cluster synthesis prompt
        prompt = self._build_cluster_synthesis_prompt(
            cluster_tests=cluster_tests,
            category=category,
            function_name=function_name,
            function_code=function_code,
            cluster_id=cluster_id
        )

        # Call LLM for this cluster
        synthesized_test = await self._call_synthesis_llm(
            prompt=prompt,
            context_info=f"Cluster {cluster_id}",
            stream_thinking=stream_thinking  # ✅ Pass the flag
        )

        # Clean the output
        cleaned_test = self._clean_cluster_output(synthesized_test, function_name)

        return cleaned_test

    def _build_cluster_synthesis_prompt(
            self,
            cluster_tests: List[str],
            category: str,
            function_name: str,
            function_code: str,
            cluster_id: int
    ) -> str:
        """Build prompt for synthesizing a single cluster"""

        # Format all tests in the cluster
        tests_formatted = []
        for idx, test in enumerate(cluster_tests, 1):
            tests_formatted.append(f"""### Test Variant {idx}:
```python
{test}
```""")

        all_tests_text = "\n".join(tests_formatted)

        prompt = f"""You are synthesizing a SINGLE comprehensive test from similar test variants.

## Function Under Test:
```python
{function_code}
```

## Context:
- **Cluster ID**: {cluster_id}
- **Category**: {category}
- **Number of variants**: {len(cluster_tests)}

## Test Variants in This Cluster:
{all_tests_text}

## Your Task:
Create ONE excellent test function that:
1. **Preserves all unique testing insights** from the variants above
2. **Combines the best aspects** of each variant (assertions, edge cases, error handling)
3. **Eliminates redundancy** - don't repeat the same assertion multiple times
4. **Maintains clarity** - the test should be readable and well-documented
5. **Follows pytest best practices** - proper naming, fixtures, parametrization if needed

## Guidelines:
- Test name should be: `test_{function_name}_<descriptive_scenario>`
- Include a docstring explaining what this test validates
- Use clear variable names and assertions
- If variants test different inputs, consider using `@pytest.mark.parametrize`
- Preserve any unique error handling or edge case checks
- DO NOT include imports (they will be added later)
- Output ONLY the test function, nothing else

Generate the synthesized test function now:
"""

        return prompt

    async def create_final_test_file(
            self,
            cluster_tests: List[str],
            function_name: str,
            function_code: str
    ) -> str:
        """
        PHASE 2: Create final unified test file from cluster-synthesized tests
        ✅ STREAMS the complete final code to frontend

        Args:
            cluster_tests: List of synthesized tests (one per cluster)
            function_name: Name of the function being tested
            function_code: Source code of the function

        Returns:
            Complete, runnable test file
        """
        logger.info(f"Phase 2: Creating final unified test file from {len(cluster_tests)} synthesized tests (WITH STREAMING)")

        # Build final unification prompt
        prompt = self._build_final_unification_prompt(
            cluster_tests=cluster_tests,
            function_name=function_name,
            function_code=function_code
        )

        # Call LLM for final unification WITH STREAMING
        final_code = await self._call_synthesis_llm(
            prompt=prompt,
            context_info="Final Unification",
            stream_thinking=True  # ✅ ENABLED for Phase 2
        )

        # Clean and validate
        final_code = self._clean_final_output(final_code, function_name, function_code)

        return final_code

    def _build_final_unification_prompt(
            self,
            cluster_tests: List[str],
            function_name: str,
            function_code: str
    ) -> str:
        """Build prompt for final test file unification"""

        # Format all synthesized tests
        tests_formatted = []
        for idx, test in enumerate(cluster_tests, 1):
            tests_formatted.append(f"""### Synthesized Test {idx}:
```python
{test}
```""")

        all_tests_text = "\n".join(tests_formatted)

        prompt = f"""You are creating a COMPLETE, RUNNABLE test file.

## Function Under Test:
```python
{function_code}
```

## Synthesized Tests from Clusters:
You have {len(cluster_tests)} high-quality tests, each representing a cluster of similar test variants:

{all_tests_text}

## Your Task:
Create a **complete, production-ready test file** that:

1. **Includes all necessary imports** (pytest, any needed standard library modules)
2. **Includes the function under test** in the file (copy it exactly)
3. **Includes all synthesized tests** with any final refinements:
   - Ensure tests don't conflict or duplicate
   - Organize tests logically (positive → negative → edge → security → performance)
   - Add any shared fixtures if needed
   - Ensure consistent coding style and conventions
4. **Compiles and runs correctly** - this must be valid Python code
5. **Follows best practices**:
   - Clear test names
   - Good docstrings
   - Proper assertions
   - pytest conventions

## Output Format:
```python
\"\"\"
Test suite for {function_name}
Auto-generated by TestGen Council
\"\"\"

import pytest
# Add other necessary imports

# ==================== Function Under Test ====================

{function_code}

# ==================== Test Cases ====================

def test_{function_name}_scenario1():
    \"\"\"Description of what this tests.\"\"\"
    # Test implementation
    assert condition

def test_{function_name}_scenario2():
    \"\"\"Description of what this tests.\"\"\"
    # Test implementation
    assert condition

# ... more tests ...
```

Generate the complete, final test file now:
"""

        return prompt

    async def _call_synthesis_llm(
            self,
            prompt: str,
            context_info: str = "Synthesis",
            stream_thinking: bool = False  # ✅ NEW parameter
    ) -> str:
        """
        Call LLM for synthesis with optional streaming

        Args:
            prompt: Synthesis prompt
            context_info: Context for logging (e.g., "Cluster 1" or "Final Unification")
            stream_thinking: Whether to stream thinking chunks to frontend

        Returns:
            Synthesized code
        """
        # Use the best model for synthesis
        model_id = config.SYNTHESIS_MODEL
        model_config = config.LLM_MODELS[model_id]
        api_base = config.LLM_API_BASES[model_config["provider"]]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.LLM_API_KEY}"
        }

        payload = {
            "model": model_config["api_name"],
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert at synthesizing high-quality, production-ready test suites. You write clean, maintainable, and comprehensive tests."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4,  # Lower temperature for focused synthesis
            "max_tokens": 8000,
            "stream": True
        }

        full_response = ""

        try:
            async with self.session.post(
                    f"{api_base}/chat/completions",
                    headers=headers,
                    json=payload
            ) as response:
                response.raise_for_status()

                async for line in response.content:
                    line = line.decode('utf-8').strip()

                    if not line or line == "data: [DONE]":
                        continue

                    if line.startswith("data: "):
                        try:
                            import json
                            data = json.loads(line[6:])

                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")

                                if content:
                                    full_response += content

                                    # ✅ Only send thinking chunks if streaming is enabled
                                    if stream_thinking and self.streaming_queue:
                                        await self.streaming_queue.put(
                                            await SSEStream.send_synthesis_thinking_event(
                                                thinking_chunk=content
                                            )
                                        )

                        except json.JSONDecodeError:
                            continue

            logger.info(f"{context_info} complete: {len(full_response)} characters")
            return full_response

        except Exception as e:
            logger.error(f"{context_info} LLM call failed: {e}", exc_info=True)
            raise SynthesisError(f"Failed to call synthesis LLM for {context_info}: {str(e)}")

    def _clean_cluster_output(self, raw_output: str, function_name: str) -> str:
        """
        Clean cluster synthesis output

        Args:
            raw_output: Raw LLM output
            function_name: Function name for validation

        Returns:
            Cleaned test function code
        """
        cleaned = raw_output.strip()

        # Remove markdown code fences
        if cleaned.startswith("```python"):
            cleaned = cleaned[9:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        # Validate that we have a test function
        if "def test_" not in cleaned:
            logger.warning(f"Cluster output doesn't contain a test function")

        return cleaned

    def _clean_final_output(
            self,
            raw_output: str,
            function_name: str,
            function_code: str
    ) -> str:
        """
        Clean and validate final test file output

        Args:
            raw_output: Raw LLM output
            function_name: Function name for validation
            function_code: Original function code

        Returns:
            Cleaned complete test file
        """
        cleaned = raw_output.strip()

        # Remove markdown code fences
        if cleaned.startswith("```python"):
            cleaned = cleaned[9:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        # Ensure imports are present
        if "import pytest" not in cleaned:
            cleaned = "import pytest\n\n" + cleaned

        # Ensure function under test is present
        if function_code.strip() not in cleaned:
            logger.warning("Function under test not found in final output, adding it")
            # Insert after imports
            import_end = cleaned.find("\n\n")
            if import_end != -1:
                cleaned = (
                        cleaned[:import_end + 2] +
                        f"# ==================== Function Under Test ====================\n\n"
                        f"{function_code}\n\n"
                        f"# ==================== Test Cases ====================\n\n" +
                        cleaned[import_end + 2:]
                )

        # Validate that we have test functions
        if f"def test_{function_name}" not in cleaned and "def test_" not in cleaned:
            logger.warning("Final output doesn't contain expected test functions")

        return cleaned