"""
Code coverage analyzer using pytest and coverage.py
"""

import subprocess
import json
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from loguru import logger

from app.utils.exceptions import CoverageError


class CoverageAnalyzer:
    """Analyzes code coverage of generated tests"""

    def __init__(self):
        self.coverage_data: Optional[Dict[str, Any]] = None
        self.test_results: Optional[Dict[str, Any]] = None

    async def analyze_coverage(
            self,
            function_code: str,
            test_code: str,
            function_name: str
    ) -> Dict[str, Any]:
        """
        Run tests and analyze coverage

        Args:
            function_code: Source function code
            test_code: Generated test code
            function_name: Name of the function

        Returns:
            Coverage analysis results
        """
        logger.info(f"Starting coverage analysis for {function_name}")

        # Create temporary directory for test execution
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Write function code
            function_file = temp_path / f"{function_name}.py"
            function_file.write_text(function_code)

            # Write test code (with import)
            test_file = temp_path / f"test_{function_name}.py"

            # Ensure test imports the function
            if f"from {function_name} import" not in test_code and f"import {function_name}" not in test_code:
                test_code = f"from {function_name} import {function_name}\n\n{test_code}"

            test_file.write_text(test_code)

            # Run pytest with coverage
            coverage_result = await self._run_pytest_coverage(
                test_file=test_file,
                source_file=function_file,
                temp_dir=temp_path
            )

            # Parse results
            analysis = self._parse_coverage_results(coverage_result, temp_path)

            logger.info(f"Coverage analysis complete: {analysis['coverage_percentage']:.1f}%")

            return analysis

    async def _run_pytest_coverage(
            self,
            test_file: Path,
            source_file: Path,
            temp_dir: Path
    ) -> Dict[str, Any]:
        """
        Execute pytest with coverage

        Args:
            test_file: Path to test file
            source_file: Path to source file
            temp_dir: Temporary directory

        Returns:
            Execution results
        """
        coverage_json = temp_dir / "coverage.json"

        # Build pytest command
        cmd = [
            "python", "-m", "pytest",
            str(test_file),
            f"--cov={source_file.stem}",
            "--cov-report=term-missing",
            f"--cov-report=json:{coverage_json}",
            "-v",
            "--tb=short"
        ]

        try:
            # Run pytest
            result = subprocess.run(
                cmd,
                cwd=str(temp_dir),
                capture_output=True,
                text=True,
                timeout=30
            )

            # Read coverage JSON if it exists
            coverage_data = None
            if coverage_json.exists():
                with open(coverage_json, 'r') as f:
                    coverage_data = json.load(f)

            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "coverage_data": coverage_data
            }

        except subprocess.TimeoutExpired:
            raise CoverageError("Coverage analysis timed out after 30 seconds")
        except Exception as e:
            logger.error(f"Pytest execution failed: {e}", exc_info=True)
            raise CoverageError(f"Failed to run pytest: {str(e)}")

    def _parse_coverage_results(
            self,
            result: Dict[str, Any],
            temp_dir: Path
    ) -> Dict[str, Any]:
        """
        Parse pytest and coverage results

        Args:
            result: Pytest execution result
            temp_dir: Temporary directory

        Returns:
            Parsed coverage analysis
        """
        analysis = {
            "total_lines": 0,
            "covered_lines": 0,
            "missing_lines": [],
            "coverage_percentage": 0.0,
            "passed_tests": 0,
            "failed_tests": 0,
            "total_tests": 0,
            "success_rate": 0.0,
            "test_output": result["stdout"]
        }

        # Parse test results from stdout
        stdout = result["stdout"]

        # Extract test counts
        if " passed" in stdout:
            try:
                passed_match = stdout.split(" passed")[0].split()[-1]
                analysis["passed_tests"] = int(passed_match)
            except (ValueError, IndexError):
                pass

        if " failed" in stdout:
            try:
                failed_match = stdout.split(" failed")[0].split()[-1]
                analysis["failed_tests"] = int(failed_match)
            except (ValueError, IndexError):
                pass

        analysis["total_tests"] = analysis["passed_tests"] + analysis["failed_tests"]

        if analysis["total_tests"] > 0:
            analysis["success_rate"] = (analysis["passed_tests"] / analysis["total_tests"]) * 100

        # Parse coverage data
        if result["coverage_data"]:
            cov_data = result["coverage_data"]

            # Get coverage for the source file
            files = cov_data.get("files", {})

            if files:
                # Take the first file (should be our function file)
                file_data = list(files.values())[0]

                summary = file_data.get("summary", {})
                analysis["total_lines"] = summary.get("num_statements", 0)
                analysis["covered_lines"] = summary.get("covered_lines", 0)
                analysis["coverage_percentage"] = summary.get("percent_covered", 0.0)

                # Missing lines
                missing = file_data.get("missing_lines", [])
                analysis["missing_lines"] = missing

        else:
            # Try to parse from stdout if JSON not available
            if "%" in stdout:
                try:
                    # Look for coverage percentage in output
                    for line in stdout.split('\n'):
                        if '%' in line and 'TOTAL' not in line:
                            parts = line.split()
                            for part in parts:
                                if '%' in part:
                                    analysis["coverage_percentage"] = float(part.rstrip('%'))
                                    break
                except:
                    pass

        return analysis

    def get_coverage_summary(self) -> str:
        """
        Get human-readable coverage summary

        Returns:
            Coverage summary string
        """
        if not self.coverage_data:
            return "No coverage data available"

        summary = f"""
Coverage Analysis Summary:
--------------------------
Total Lines: {self.coverage_data['total_lines']}
Covered Lines: {self.coverage_data['covered_lines']}
Coverage: {self.coverage_data['coverage_percentage']:.1f}%
Missing Lines: {', '.join(map(str, self.coverage_data['missing_lines'])) or 'None'}

Test Results:
-------------
Total Tests: {self.coverage_data['total_tests']}
Passed: {self.coverage_data['passed_tests']}
Failed: {self.coverage_data['failed_tests']}
Success Rate: {self.coverage_data['success_rate']:.1f}%
"""

        return summary