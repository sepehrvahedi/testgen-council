"""
LLM Council module for parallel test generation using multiple models and roles
"""
import ast
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import time
from loguru import logger
import re

from app.config import config
from app.utils.exceptions import LLMError
from app.utils.streaming import StreamingQueue, SSEStream


class LLMCouncil:
    """Manages parallel test generation using multiple LLM models and roles"""

    def __init__(self, streaming_queue: Optional[StreamingQueue] = None):
        self.streaming_queue = streaming_queue
        self.results: List[Dict[str, Any]] = []
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

    def _clean_streaming_content(self, content: str) -> str:
        """
        Clean streaming content by removing ONLY code fences and language identifiers

        Args:
            content: Raw streaming chunk

        Returns:
            Cleaned content without code fences but preserving all valid Python code
        """
        # ✅ DON'T strip the content - preserve all whitespace
        cleaned = content

        # Remove opening code fence if present
        if cleaned.startswith("```python"):
            cleaned = cleaned[9:]  # Remove "```python"
        elif cleaned.startswith("```py"):
            cleaned = cleaned[5:]  # Remove "```py"
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]  # Remove "```"

        # Remove closing code fence if present
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        # ✅ ONLY skip if chunk is JUST the language identifier (no newlines)
        stripped = cleaned.strip().lower()
        if stripped in ["python", "py", ""]:
            # But keep the newlines that might follow
            if cleaned and not cleaned.strip():
                return cleaned  # This is whitespace, keep it
            return ""  # This is just "python" or "py", skip it

        return cleaned

    async def generate_tests_generic(
            self,
            function_context: str,
            function_name: str,
            models: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate tests WITHOUT role personas (for Ablation 1)
        Uses generic prompts across all models
        """
        start_time = time.time()

        model_ids = models if models else list(config.LLM_MODELS.keys())

        logger.info(f"Starting generic generation with {len(model_ids)} models")

        tasks = []
        for i, model_id in enumerate(model_ids):
            task = self._generate_with_model_generic(
                model_id=model_id,
                function_context=function_context,
                function_name=function_name,
                model_index=i + 1,
                total_models=len(model_ids)
            )
            tasks.append(task)

        semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_LLMS)

        async def bounded_task(task):
            async with semaphore:
                return await task

        results = await asyncio.gather(
            *[bounded_task(task) for task in tasks],
            return_exceptions=True
        )

        valid_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Generic generation failed: {result}")
            else:
                valid_results.append(result)

        duration = time.time() - start_time
        logger.info(f"Generic generation completed in {duration:.2f}s")

        return valid_results

    async def _generate_with_model_generic(
            self,
            model_id: str,
            function_context: str,
            function_name: str,
            model_index: int,
            total_models: int
    ) -> Dict[str, Any]:
        """Generate with generic prompt (no role)"""

        start_time = time.time()

        try:
            # Generic prompt without role persona
            prompt = f"""Generate comprehensive pytest test cases for the function `{function_name}`.
{function_context}

**Requirements:**
1. Output ONLY valid, runnable Python code
2. Include ALL necessary imports
3. Include the original function being tested
4. Generate complete pytest test functions
5. Cover positive cases, negative cases, boundary conditions, and edge cases
6. Use descriptive test names
7. Include docstrings
8. Use appropriate assertions

Generate a complete Python test file.
"""
            raw_output, tokens_used = await self._call_llm_api(
                model_id=model_id,
                role_id="generic",
                prompt=prompt
            )

            tests = self._extract_tests(raw_output)

            duration = time.time() - start_time

            result = {
                "model": model_id,
                "role": "generic",
                "tests": tests,
                "raw_output": raw_output,
                "tokens_used": tokens_used,
                "duration_seconds": duration,
                "timestamp": datetime.utcnow().isoformat()
            }

            logger.info(f"{model_id} (generic) generated {len(tests)} tests in {duration:.2f}s")

            return result

        except Exception as e:
            logger.error(f"Generic generation failed for {model_id}: {e}", exc_info=True)
            raise


    async def generate_tests_parallel(
            self,
            function_context: str,
            function_name: str,
            test_hints: Dict[str, List[str]],
            models: Optional[List[str]] = None,
            roles: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate tests in parallel using multiple models and roles

        Args:
            function_context: Function analysis context
            function_name: Name of the function
            test_hints: Test hints by category
            models: List of model IDs to use (uses all if None)
            roles: List of role IDs to use (uses all if None)

        Returns:
            List of generation results with model outputs
        """
        start_time = time.time()

        # Get model-role assignments
        assignments = self._get_model_role_assignments(models, roles)

        if not assignments:
            raise LLMError("No valid model-role assignments found")

        logger.info(f"Starting parallel generation with {len(assignments)} models")

        # Create tasks for each model
        tasks = []
        for i, (model_id, role_id) in enumerate(assignments):
            task = self._generate_with_model(
                model_id=model_id,
                role_id=role_id,
                function_context=function_context,
                function_name=function_name,
                test_hints=test_hints,
                model_index=i + 1,
                total_models=len(assignments)
            )
            tasks.append(task)

        # Execute in parallel with concurrency limit
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_LLMS)

        async def bounded_task(task):
            async with semaphore:
                return await task

        results = await asyncio.gather(
            *[bounded_task(task) for task in tasks],
            return_exceptions=True
        )

        # Process results
        valid_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Model generation failed: {result}")
            else:
                valid_results.append(result)

        duration = time.time() - start_time
        logger.info(f"Parallel generation completed in {duration:.2f}s. {len(valid_results)}/{len(assignments)} successful")

        self.results = valid_results
        return valid_results

    def _get_model_role_assignments(
            self,
            models: Optional[List[str]],
            roles: Optional[List[str]]
    ) -> List[tuple]:
        """Get model-role assignment pairs"""
        assignments = []

        # Use specified models or all available
        model_ids = models if models else list(config.LLM_MODELS.keys())

        for model_id in model_ids:
            if model_id not in config.MODEL_ROLE_ASSIGNMENTS:
                logger.warning(f"No role assignment for model: {model_id}")
                continue

            assigned_roles = config.MODEL_ROLE_ASSIGNMENTS[model_id]

            # Filter by requested roles if specified
            # if roles:
            #     assigned_roles = [r for r in assigned_roles if r in roles]

            # Create assignment for each role
            for role_id in assigned_roles:
                assignments.append((model_id, role_id))

        return assignments

    async def _generate_with_model(
            self,
            model_id: str,
            role_id: str,
            function_context: str,
            function_name: str,
            test_hints: Dict[str, List[str]],
            model_index: int,
            total_models: int
    ) -> Dict[str, Any]:
        """
        Generate tests with a single model-role pair
        """
        start_time = time.time()

        try:
            # Send start event
            if self.streaming_queue:
                await self.streaming_queue.put(
                    await SSEStream.send_llm_start_event(
                        model=model_id,
                        role=role_id,
                        model_index=model_index,
                        total_models=total_models
                    )
                )

            # Build prompt
            prompt = self._build_prompt(
                role_id=role_id,
                function_context=function_context,
                function_name=function_name,
                test_hints=test_hints
            )

            # ✅ FIX: Pass role_id to _call_llm_api
            raw_output, tokens_used = await self._call_llm_api(
                model_id=model_id,
                role_id=role_id,  # ✅ ADD THIS
                prompt=prompt
            )

            # Extract test functions (removing code fences)
            tests = self._extract_tests(raw_output)

            duration = time.time() - start_time

            result = {
                "model": model_id,
                "role": role_id,
                "tests": tests,
                "raw_output": raw_output,
                "tokens_used": tokens_used,
                "duration_seconds": duration,
                "timestamp": datetime.utcnow().isoformat()
            }

            # Send complete event
            if self.streaming_queue:
                await self.streaming_queue.put(
                    await SSEStream.send_llm_complete_event(
                        model=model_id,
                        role=role_id,
                        tests_generated=len(tests),
                        duration=duration
                    )
                )

            logger.info(f"{model_id} ({role_id}) generated {len(tests)} tests in {duration:.2f}s")

            return result

        except Exception as e:
            logger.error(f"Generation failed for {model_id} ({role_id}): {e}", exc_info=True)
            raise LLMError(
                message=f"Failed to generate tests: {str(e)}",
                model=model_id,
                role=role_id
            )

    def _build_prompt(
            self,
            role_id: str,
            function_context: str,
            function_name: str,
            test_hints: Dict[str, List[str]]
    ) -> str:
        """Build role-specific prompt"""
        role = config.ROLES[role_id]

        # Get relevant hints for this role
        relevant_hints = []
        for category in role["focus_categories"]:
            if category in test_hints:
                relevant_hints.extend(test_hints[category])

        hints_text = "\n".join(f"- {hint}" for hint in relevant_hints) if relevant_hints else "- No specific hints"

        prompt = f"""You are a **{role['name']}** for an intelligent test generation system.

**Your Philosophy:** {role['philosophy']}

**Your Mission:** Generate comprehensive pytest test cases for the function `{function_name}`.

{function_context}

**Test Focus Areas:**
{hints_text}

**CRITICAL REQUIREMENTS:**
1. Output ONLY valid, runnable Python code
2. Include ALL necessary imports at the top
3. Include the original function being tested
4. Generate complete pytest test functions
5. Each test must be self-contained and executable
6. Use descriptive test names following pytest conventions (test_functionname_scenario)
7. Include docstrings explaining what each test validates
8. Cover {', '.join(role['focus_categories'])} test scenarios
9. Use appropriate assertions (assert, pytest.raises, etc.)
10. Add comments explaining complex test logic

**OUTPUT FORMAT:**
Generate a complete Python file with this structure:

```python
import pytest

# Add any other necessary imports

# Original function being tested
{self._extract_function_code_only(function_context)}

# Test functions
def test_{function_name}_scenario_1():
    \"\"\"Test description.\"\"\"
    # Test implementation
    result = {function_name}(args)
    assert result == expected

def test_{function_name}_scenario_2():
    \"\"\"Test description.\"\"\"
    # Test implementation
    with pytest.raises(SomeException):
        {function_name}(invalid_args)

# More tests...
```

Generate ONLY the Python code above. DO NOT include markdown code fences, explanations, or any text outside the code.
"""

        return prompt

    async def _call_llm_api(
            self,
            model_id: str,
            role_id: str,  # ✅ ADD THIS PARAMETER
            prompt: str
    ) -> tuple[str, Optional[int]]:
        """
        Call LLM API with streaming support

        Args:
            model_id: Model identifier
            role_id: Role identifier (for streaming events)
            prompt: The prompt to send

        Returns:
            Tuple of (complete response text, tokens used)
        """
        model_config = config.LLM_MODELS[model_id]
        api_base = config.LLM_API_BASES.get(model_config["provider"])

        if not api_base:
            raise LLMError(f"No API base configured for provider: {model_config['provider']}")

        # Build request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.LLM_API_KEY}"
        }

        payload = {
            "model": model_config["api_name"],
            "messages": [
                {"role": "system", "content": "You are an expert Python test engineer."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            # "max_tokens": 4000,
            "stream": True
        }

        full_response = ""
        tokens_used = None
        chunk_index = 0

        try:
            async with self.session.post(
                    f"{api_base}/chat/completions",
                    headers=headers,
                    json=payload
            ) as response:
                response.raise_for_status()

                # Process streaming response
                async for line in response.content:
                    line = line.decode('utf-8').strip()

                    if not line or line == "data: [DONE]":
                        continue

                    if line.startswith("data: "):
                        try:
                            import json
                            data = json.loads(line[6:])

                            if data is None:
                                continue

                            choices = data.get("choices")
                            if not choices or len(choices) == 0:
                                continue

                            choice = choices[0]
                            if choice is None:
                                continue

                            delta = choice.get("delta")
                            if delta is None:
                                delta = choice.get("message", {})

                            content = delta.get("content", "") if delta else ""

                            if content:
                                # ✅ FIX: Strip code fences in real-time
                                cleaned_content = self._clean_streaming_content(content)

                                if cleaned_content:  # Only add if there's content after cleaning
                                    full_response += cleaned_content

                                    # Send chunk event with role
                                    if self.streaming_queue:
                                        await self.streaming_queue.put(
                                            await SSEStream.send_llm_chunk_event(
                                                model=model_id,
                                                role=role_id,  # ✅ NOW ROLE IS INCLUDED
                                                chunk=cleaned_content,
                                                chunk_index=chunk_index
                                            )
                                        )
                                        chunk_index += 1

                            # Extract usage if available
                            usage = data.get("usage")
                            if usage:
                                tokens_used = usage.get("total_tokens")

                        except json.JSONDecodeError as json_err:
                            logger.warning(f"Failed to parse JSON line for {model_id}: {json_err}")
                            continue
                        except Exception as parse_err:
                            logger.warning(f"Error processing chunk for {model_id}: {parse_err}")
                            continue

            if not full_response:
                logger.warning(f"No content received from {model_id}. Response might be empty.")

            return full_response, tokens_used

        except aiohttp.ClientError as e:
            raise LLMError(
                f"API request failed: {str(e)}",
                model=model_id,
                details={"api_base": api_base}
            )
        except Exception as e:
            logger.error(f"Unexpected error in API call for {model_id}: {e}", exc_info=True)
            raise LLMError(
                f"Unexpected API error: {str(e)}",
                model=model_id,
                details={"api_base": api_base}
            )

    def _extract_function_code_only(self, function_context: str) -> str:
        """Extract just the function code from context"""
        # Extract the source code section
        if "### Complete Function Code" in function_context:
            start = function_context.find("```python", function_context.find("### Complete Function Code"))
            if start != -1:
                start += 9  # len("```python\n")
                end = function_context.find("```", start)
                if end != -1:
                    return function_context[start:end].strip()

        # Fallback: try to extract from source code section
        if "### Source Code" in function_context:
            start = function_context.find("python\n", function_context.find("### Source Code"))
            if start != -1:
                start += 7  # len("python\n")
                # Find next triple backtick or end
                remaining = function_context[start:]
                lines = []
                for line in remaining.split('\n'):
                    if line.strip() == '```' or line.strip().startswith('###'):
                        break
                    lines.append(line)
                return '\n'.join(lines).strip()

        return f"# Function code could not be extracted"

    def _extract_tests(self, llm_output: str) -> List[str]:
        """
        Extract complete test file sections from LLM output

        Returns the COMPLETE runnable code including imports and function definition,
        plus individual test functions for clustering.
        """
        initial_llm_output = llm_output

        # ✅ Clean ONLY first and last lines
        lines = llm_output.splitlines()

        if len(lines) > 0:
            # Remove ``` or ```python or python from FIRST line only
            first_line = lines[0].strip()
            if first_line in ['```', '```python', 'python']:
                lines = lines[1:]

        if len(lines) > 0:
            # Remove ``` from LAST line only
            last_line = lines[-1].strip()
            if last_line == '```':
                lines = lines[:-1]

        output = '\n'.join(lines).strip()

        try:
            # Parse to validate it's proper Python
            tree = ast.parse(output)

            # Extract imports
            imports = []
            function_def = None
            test_functions = []

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.append(ast.unparse(node))
                elif isinstance(node, ast.FunctionDef):
                    if node.name.startswith('test_'):
                        # This is a test function
                        test_functions.append(ast.unparse(node))
                    else:
                        # This is the function being tested
                        function_def = ast.unparse(node)

            # For each test, create a complete runnable version
            complete_tests = []
            imports_block = '\n'.join(imports) if imports else 'import pytest'
            function_block = function_def if function_def else ''

            for test_func in test_functions:
                # Create complete runnable test file
                complete_test = f"""{imports_block}

{function_block}

{test_func}
"""
                complete_tests.append(complete_test)

            logger.info(f"Extracted {len(complete_tests)} complete test functions")
            return complete_tests

        except SyntaxError as e:
            logger.error(f"LLM output is not valid Python: {e}")
            logger.debug(f"Initial llm output: {initial_llm_output[:500]}...")
            logger.debug(f"Invalid output: {output[:500]}...")
            # Fallback to simple extraction
            return self._extract_tests_fallback(output)

    def _extract_tests_fallback(self, llm_output: str) -> List[str]:
        """Fallback extraction when AST parsing fails"""
        tests = []
        lines = llm_output.split('\n')
        current_test = []
        in_test = False

        for line in lines:
            if line.strip().startswith('def test_'):
                if current_test:
                    tests.append('\n'.join(current_test))
                current_test = [line]
                in_test = True
            elif in_test:
                if line and not line[0].isspace() and line.strip() and not line.strip().startswith('#'):
                    if line.strip().startswith('def test_'):
                        continue
                    else:
                        tests.append('\n'.join(current_test))
                        current_test = []
                        in_test = False
                else:
                    current_test.append(line)

        if current_test:
            tests.append('\n'.join(current_test))

        return tests if tests else [llm_output]  # Return whole output if no tests found

    def get_all_tests(self) -> List[str]:
        """Get all tests from all model results"""
        all_tests = []
        for result in self.results:
            all_tests.extend(result["tests"])
        return all_tests

