"""
Mutation Testing Analyzer using mutmut
Gold standard for test quality measurement
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import re

from loguru import logger


class MutationAnalyzer:
    """
    Analyzes test effectiveness using mutation testing

    Mutation Score = (Killed Mutants / Total Mutants) × 100

    Higher mutation score = better test quality
    """

    def __init__(self):
        self.mutation_results: Optional[Dict[str, Any]] = None

    async def analyze_mutations(
            self,
            function_code: str,
            test_code: str,
            function_name: str,
            timeout_per_mutant: int = 10
    ) -> Dict[str, Any]:
        """
        Run mutation testing on the function using generated tests

        Args:
            function_code: Source function to mutate
            test_code: Test code (cleaned, tests only)
            function_name: Name of function
            timeout_per_mutant: Max seconds per mutant execution

        Returns:
            Dict with mutation metrics
        """
        logger.info(f"Starting mutation analysis for {function_name}")

        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Write source file
            source_file = temp_path / f"{function_name}.py"
            source_file.write_text(function_code)

            # Ensure test imports correctly
            if f"from {function_name} import" not in test_code and f"import {function_name}" not in test_code:
                test_code = f"from {function_name} import {function_name}\n\n{test_code}"

            # Write test file
            test_file = temp_path / f"test_{function_name}.py"
            test_file.write_text(test_code)

            # Create minimal setup.cfg for mutmut
            setup_cfg = temp_path / "setup.cfg"
            setup_cfg.write_text(f"""[mutmut]
paths_to_mutate={source_file.name}
tests_dir=.
runner=python -m pytest -x --tb=short -p no:warnings
""")

            logger.debug(f"Mutation testing workspace: {temp_path}")
            logger.debug(f"Source: {source_file.name}, Test: {test_file.name}")

            try:
                # Run mutation testing
                result = await self._run_mutmut(
                    temp_dir=temp_path,
                    source_file=source_file,
                    timeout_per_mutant=timeout_per_mutant
                )

                # Parse and return results
                return self._parse_mutation_results(result)

            except Exception as e:
                logger.error(f"Mutation analysis failed: {e}", exc_info=True)
                return self._get_empty_results(error=str(e))

    async def _run_mutmut(
            self,
            temp_dir: Path,
            source_file: Path,
            timeout_per_mutant: int
    ) -> Dict[str, Any]:
        """Execute mutmut mutation testing"""

        # Step 1: Run mutmut to generate and test mutations
        logger.info("Running mutmut...")

        run_cmd = [
            "mutmut",
            "run",
            "--paths-to-mutate", str(source_file),
            "--runner", "python -m pytest -x --tb=short -p no:warnings",
            "--no-progress"
        ]

        try:
            import os
            env = os.environ.copy()
            env['PYTEST_TIMEOUT'] = str(timeout_per_mutant)

            run_result = subprocess.run(
                run_cmd,
                cwd=str(temp_dir),
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max for all mutations
                env=env
            )

            logger.debug(f"mutmut run output:\n{run_result.stdout}")
            if run_result.stderr:
                logger.debug(f"mutmut run stderr:\n{run_result.stderr}")

        except subprocess.TimeoutExpired:
            logger.warning("Mutation testing timed out after 5 minutes")
            return {
                "status": "timeout",
                "stdout": "",
                "stderr": "Mutation testing exceeded 5 minute timeout",
                "results": None
            }
        except Exception as e:
            logger.error(f"Failed to run mutmut: {e}")
            return {
                "status": "error",
                "stdout": "",
                "stderr": str(e),
                "results": None
            }

        # Step 2: Get mutation results summary
        results_cmd = ["mutmut", "results"]

        try:
            results_result = subprocess.run(
                results_cmd,
                cwd=str(temp_dir),
                capture_output=True,
                text=True,
                timeout=30
            )

            logger.debug(f"mutmut results output:\n{results_result.stdout}")

            # Step 3: Get JSON summary if available
            json_cmd = ["mutmut", "junitxml"]
            json_result = subprocess.run(
                json_cmd,
                cwd=str(temp_dir),
                capture_output=True,
                text=True,
                timeout=30
            )

            return {
                "status": "completed",
                "stdout": run_result.stdout,
                "stderr": run_result.stderr,
                "results": results_result.stdout,
                "json_output": json_result.stdout
            }

        except Exception as e:
            logger.warning(f"Failed to get mutmut results summary: {e}")
            return {
                "status": "completed",
                "stdout": run_result.stdout,
                "stderr": run_result.stderr,
                "results": "",
                "json_output": ""
            }

    def _parse_mutation_results(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse mutmut output into structured metrics"""

        if result["status"] in ["timeout", "error"]:
            return self._get_empty_results(error=result.get("stderr", "Unknown error"))

        stdout = result.get("stdout", "")
        results = result.get("results", "")

        killed = 0
        survived = 0
        suspicious = 0
        timeout = 0

        # ✅ IMPROVED: Parse both stdout AND results with better patterns
        combined_output = stdout + "\n" + results

        # Pattern 1: "Killed 🎉 (X)" or "Survived 🙁 (Y)"
        killed_emoji = re.search(r'Killed\s+🎉\s+\((\d+)\)', combined_output)
        if killed_emoji:
            killed = int(killed_emoji.group(1))

        survived_emoji = re.search(r'Survived\s+🙁\s+\((\d+)\)', combined_output)
        if survived_emoji:
            survived = int(survived_emoji.group(1))

        suspicious_emoji = re.search(r'Suspicious\s+🤔\s+\((\d+)\)', combined_output)
        if suspicious_emoji:
            suspicious = int(suspicious_emoji.group(1))

        timeout_emoji = re.search(r'Timeout\s+⏰\s+\((\d+)\)', combined_output)
        if timeout_emoji:
            timeout = int(timeout_emoji.group(1))

        # Pattern 2: Text-based "X killed, Y survived" (fallback)
        if killed == 0 and survived == 0:
            killed_match = re.search(r'(\d+)\s+killed', combined_output, re.IGNORECASE)
            if killed_match:
                killed = int(killed_match.group(1))

            survived_match = re.search(r'(\d+)\s+survived', combined_output, re.IGNORECASE)
            if survived_match:
                survived = int(survived_match.group(1))

            suspicious_match = re.search(r'(\d+)\s+suspicious', combined_output, re.IGNORECASE)
            if suspicious_match:
                suspicious = int(suspicious_match.group(1))

            timeout_match = re.search(r'(\d+)\s+timeout', combined_output, re.IGNORECASE)
            if timeout_match:
                timeout = int(timeout_match.group(1))

        # Pattern 3: Summary format "X/Y" (last resort)
        if killed == 0 and survived == 0 and suspicious == 0:
            summary_match = re.search(r'(\d+)\s*/\s*(\d+)', combined_output)
            if summary_match:
                killed = int(summary_match.group(1))
                total_from_summary = int(summary_match.group(2))
                survived = total_from_summary - killed

        total = killed + survived + suspicious + timeout

        # Calculate mutation score
        mutation_score = 0.0
        if total > 0:
            mutation_score = (killed / total) * 100

        logger.info(f"Mutation Results: {killed} killed, {survived} survived, {suspicious} suspicious, {timeout} timeout (Total: {total})")
        logger.info(f"Mutation Score: {mutation_score:.1f}%")

        return {
            "total_mutants": total,
            "killed_mutants": killed,
            "survived_mutants": survived,
            "suspicious_mutants": suspicious,
            "timeout_mutants": timeout,
            "mutation_score": round(mutation_score, 2),
            "status": "completed",
            "error": None
        }

    def _get_empty_results(self, error: Optional[str] = None) -> Dict[str, Any]:
        """Return empty mutation results on failure"""
        return {
            "total_mutants": 0,
            "killed_mutants": 0,
            "survived_mutants": 0,
            "suspicious_mutants": 0,
            "timeout_mutants": 0,
            "mutation_score": 0.0,
            "status": "failed",
            "error": error
        }
