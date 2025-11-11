"""
Code coverage analyzer using pytest and coverage.py
"""

import json
import ast
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

from loguru import logger

from app.core.mutation_analyzer import MutationAnalyzer
from app.core.quality_analyzer import TestQualityAnalyzer
from app.utils.exceptions import CoverageError


class CoverageAnalyzer:
    """Analyzes code coverage of generated tests"""

    def __init__(self):
        self.coverage_data: Optional[Dict[str, Any]] = None
        self.test_results: Optional[Dict[str, Any]] = None
        self.quality_analyzer = TestQualityAnalyzer()
        self.mutation_analyzer = MutationAnalyzer()

    async def analyze_coverage(
            self,
            function_code: str,
            test_code: str,
            function_name: str,
            enable_mutation: bool = True
    ) -> Dict[str, Any]:
        """
        Run tests and analyze coverage + quality metrics + mutation testing

        Args:
            function_code: Source function code
            test_code: Generated test code (this is what gets saved to CSV)
            function_name: Name of the function
            enable_mutation: Whether to run mutation testing (can be slow)

        Returns:
            Coverage analysis results with quality metrics and mutation score
        """
        logger.info(f"Starting coverage analysis for {function_name}")

        # Create temporary directory for test execution
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Write function code to source file
            function_file = temp_path / f"{function_name}.py"
            function_file.write_text(function_code)

            # ✅ FIX: Check syntax on the ORIGINAL test_code (what gets saved to CSV)
            syntax_check = self.check_syntax(test_code)

            if not syntax_check['is_runnable']:
                logger.warning(f"❌ Test code has syntax errors: {syntax_check['syntax_error']}")
                logger.warning(f"Test code with syntax error: \n{test_code}")
                # Return early with syntax error - don't try to run tests
                return {
                    # Line coverage
                    "total_lines": 0,
                    "covered_lines": 0,
                    "missing_lines": [],
                    "coverage_percentage": 0.0,

                    # Branch coverage
                    "total_branches": 0,
                    "covered_branches": 0,
                    "missing_branches": [],
                    "branch_coverage_percentage": 0.0,
                    "has_branches": False,

                    # Test execution
                    "passed_tests": 0,
                    "failed_tests": 0,
                    "total_tests": 0,
                    "success_rate": 0.0,
                    "test_output": "Syntax error - tests not executed",

                    # Syntax check
                    "is_runnable": False,
                    "syntax_error": syntax_check['syntax_error'],

                    # Empty metrics
                    "quality_metrics": self.quality_analyzer._get_empty_metrics(error="Syntax error"),
                    "mutation_results": self.mutation_analyzer._get_empty_results(error="Syntax error")
                }

            # Extract and clean test code FOR RUNNING ONLY
            cleaned_test_code = self._extract_tests_only(test_code, function_name)

            # Ensure test imports from source file
            if f"from {function_name} import" not in cleaned_test_code and f"import {function_name}" not in cleaned_test_code:
                cleaned_test_code = f"from {function_name} import {function_name}\n\n{cleaned_test_code}"

            # Write cleaned test code FOR EXECUTION
            test_file = temp_path / f"test_{function_name}.py"
            test_file.write_text(cleaned_test_code)

            logger.debug(f"Source file: {function_file}")
            logger.debug(f"Test file: {test_file}")

            # Run pytest with coverage
            coverage_result = await self._run_pytest_coverage(
                test_file=test_file,
                source_file=function_file,
                temp_dir=temp_path
            )

            # Parse coverage results
            analysis = self._parse_coverage_results(coverage_result, temp_path)

            # ✅ Add syntax check results (already checked on original code)
            analysis['is_runnable'] = syntax_check['is_runnable']
            analysis['syntax_error'] = syntax_check['syntax_error']

            # Add quality metrics analysis (use ORIGINAL test_code for analysis)
            logger.info("Analyzing test quality metrics...")
            quality_metrics = self.quality_analyzer.analyze_test_quality(
                test_code=test_code,  # ✅ Use original, not cleaned
                function_code=function_code,
                function_name=function_name
            )

            analysis['quality_metrics'] = quality_metrics

            # ✅ Mutation testing (use CLEANED code for execution)
            if enable_mutation and analysis['success_rate'] > 0 and syntax_check['is_runnable']:
                logger.info("Running mutation testing (this may take a while)...")
                try:
                    mutation_results = await self.mutation_analyzer.analyze_mutations(
                        function_code=function_code,
                        test_code=cleaned_test_code,  # ✅ Use cleaned for execution
                        function_name=function_name,
                        timeout_per_mutant=10
                    )
                    analysis['mutation_results'] = mutation_results

                    logger.info(f"Mutation Score: {mutation_results['mutation_score']:.1f}% "
                                f"({mutation_results['killed_mutants']}/{mutation_results['total_mutants']} killed)")
                except Exception as e:
                    logger.error(f"Mutation testing failed: {e}")
                    analysis['mutation_results'] = self.mutation_analyzer._get_empty_results(error=str(e))
            else:
                if not enable_mutation:
                    logger.info("Mutation testing disabled")
                elif not syntax_check['is_runnable']:
                    logger.warning("Skipping mutation testing (syntax errors)")
                else:
                    logger.warning("Skipping mutation testing (no passing tests)")
                analysis['mutation_results'] = self.mutation_analyzer._get_empty_results(
                    error="Disabled, syntax errors, or no passing tests"
                )

            # ✅ Enhanced logging with branch info
            logger.info(f"Syntax Valid: {syntax_check['is_runnable']}")
            logger.info(f"Coverage: Line={analysis['coverage_percentage']:.1f}%, "
                        f"Branch={self._format_branch_coverage(analysis)}")
            logger.info(f"Quality: assertions={quality_metrics['assertion_density']:.2f}, "
                        f"diversity={quality_metrics['diversity_score']:.1f}, "
                        f"edge_cases={quality_metrics['edge_case_score']:.1f}")

            return analysis

    def _format_branch_coverage(self, analysis: Dict[str, Any]) -> str:
        """Format branch coverage for logging"""
        total = analysis.get('total_branches', 0)
        covered = analysis.get('covered_branches', 0)
        pct = analysis.get('branch_coverage_percentage', 0)

        if total == 0:
            return "N/A (no branches)"
        return f"{pct:.1f}% ({covered}/{total})"

    def _extract_tests_only(self, test_code: str, function_name: str) -> str:
        """
        Extract only test functions from test code, removing embedded function definitions
        """
        import ast
        import re

        # Remove markdown fences if present
        test_code = re.sub(r'^```(?:python)?\s*', '', test_code, flags=re.MULTILINE)
        test_code = re.sub(r'\s*```$', '', test_code)
        test_code = test_code.strip()

        try:
            tree = ast.parse(test_code)

            # Collect test functions and imports only
            test_functions = []
            imports = []

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    # Only keep functions that start with 'test_'
                    if node.name.startswith('test_'):
                        test_functions.append(ast.unparse(node))
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    # Keep import statements
                    imports.append(ast.unparse(node))

            # Reconstruct clean test file
            clean_code = '\n'.join(imports)
            if clean_code:
                clean_code += '\n\n'
            clean_code += '\n\n'.join(test_functions)

            logger.info(f"Extracted {len(test_functions)} test functions, removed function definition")
            return clean_code

        except SyntaxError as e:
            logger.warning(f"Failed to parse test code with AST: {e}")

            # Fallback: Use regex to remove function definition
            pattern = rf'^\s*def\s+{re.escape(function_name)}\s*\([^)]*\):\s*(?:""".*?"""|\'\'\'.*?\'\'\')?.*?(?=\n\s*def\s+test_|\n\s*$)'
            cleaned = re.sub(pattern, '', test_code, flags=re.DOTALL | re.MULTILINE)

            # Remove "Function Under Test" comments
            cleaned = re.sub(r'#\s*=+\s*Function Under Test\s*=+.*?#\s*=+\s*Test Cases\s*=+\s*', '', cleaned, flags=re.DOTALL)

            return cleaned.strip()

    def check_syntax(self, test_code: str) -> Dict[str, Any]:
        """
        Check if test code has valid Python syntax

        Returns:
            Dict with 'is_runnable' (bool) and 'syntax_error' (str or None)
        """

        try:
            # Try to parse the code as an AST
            ast.parse(test_code)
            logger.info("✅ Test code syntax is valid")
            return {
                "is_runnable": True,
                "syntax_error": None
            }
        except SyntaxError as e:
            logger.error(f"❌ Syntax error in test code: {e}")
            return {
                "is_runnable": False,
                "syntax_error": f"Line {e.lineno}: {e.msg}"
            }
        except Exception as e:
            logger.error(f"❌ Unexpected error checking syntax: {e}")
            return {
                "is_runnable": False,
                "syntax_error": str(e)
            }

    async def _run_pytest_coverage(
            self,
            test_file: Path,
            source_file: Path,
            temp_dir: Path
    ) -> Dict[str, Any]:
        """Execute pytest with coverage"""
        coverage_json = temp_dir / "coverage.json"

        # Build pytest command WITH BRANCH COVERAGE
        cmd = [
            "python", "-m", "pytest",
            str(test_file),
            f"--cov={source_file.stem}",
            "--cov-branch",
            "--cov-report=term-missing",
            f"--cov-report=json:{coverage_json}",
            "-v",
            "--tb=short",
            "-p", "no:warnings"
        ]

        logger.info(f"Running coverage command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                cwd=str(temp_dir),
                capture_output=True,
                text=True,
                timeout=30
            )

            logger.debug(f"Pytest stdout:\n{result.stdout}")
            if result.stderr:
                logger.debug(f"Pytest stderr:\n{result.stderr}")

            # Read coverage JSON if it exists
            coverage_data = None
            if coverage_json.exists():
                with open(coverage_json, 'r') as f:
                    coverage_data = json.load(f)
            else:
                logger.warning("Coverage JSON file not created")

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
        """Parse pytest and coverage results"""
        analysis = {
            # Line coverage
            "total_lines": 0,
            "covered_lines": 0,
            "missing_lines": [],
            "coverage_percentage": 0.0,

            # Branch coverage
            "total_branches": 0,
            "covered_branches": 0,
            "missing_branches": [],
            "branch_coverage_percentage": 0.0,
            "has_branches": False,  # ✅ NEW: Track if code has any branches

            # Test execution
            "passed_tests": 0,
            "failed_tests": 0,
            "total_tests": 0,
            "success_rate": 0.0,
            "test_output": result["stdout"]
        }

        stdout = result["stdout"]

        # Extract test counts
        import re

        passed_match = re.search(r'(\d+)\s+passed', stdout)
        if passed_match:
            analysis["passed_tests"] = int(passed_match.group(1))

        failed_match = re.search(r'(\d+)\s+failed', stdout)
        if failed_match:
            analysis["failed_tests"] = int(failed_match.group(1))

        analysis["total_tests"] = analysis["passed_tests"] + analysis["failed_tests"]

        if analysis["total_tests"] > 0:
            analysis["success_rate"] = (analysis["passed_tests"] / analysis["total_tests"]) * 100

        # Parse coverage data
        if result["coverage_data"]:
            cov_data = result["coverage_data"]
            files = cov_data.get("files", {})

            if files:
                file_data = list(files.values())[0]
                summary = file_data.get("summary", {})

                # Line coverage
                analysis["total_lines"] = summary.get("num_statements", 0)
                analysis["covered_lines"] = summary.get("covered_lines", 0)
                analysis["coverage_percentage"] = summary.get("percent_covered", 0.0)
                analysis["missing_lines"] = file_data.get("missing_lines", [])

                # ✅ Branch coverage calculation
                analysis["total_branches"] = summary.get("num_branches", 0)
                analysis["has_branches"] = analysis["total_branches"] > 0

                # Calculate covered branches correctly
                # covered_branches = total_branches - num_partial_branches
                num_partial = summary.get("num_partial_branches", 0)
                analysis["covered_branches"] = analysis["total_branches"] - num_partial

                # ✅ Calculate percentage: treat 0/0 as 100% (no branches to miss)
                if analysis["total_branches"] > 0:
                    analysis["branch_coverage_percentage"] = (analysis["covered_branches"] / analysis["total_branches"]) * 100
                else:
                    # No branches in code = 100% branch coverage (nothing to miss)
                    analysis["branch_coverage_percentage"] = 100.0

                analysis["missing_branches"] = file_data.get("missing_branches", [])

                logger.info(f"Line Coverage: {analysis['coverage_percentage']:.1f}% ({analysis['covered_lines']}/{analysis['total_lines']})")
                logger.info(f"Branch Coverage: {analysis['branch_coverage_percentage']:.1f}% ({analysis['covered_branches']}/{analysis['total_branches']})")
        else:
            logger.warning("No coverage data available, trying to parse from stdout")
            coverage_match = re.search(r'(\d+)%', stdout)
            if coverage_match:
                analysis["coverage_percentage"] = float(coverage_match.group(1))

        return analysis

    def get_coverage_summary(self) -> str:
        """Get human-readable coverage summary"""
        if not self.coverage_data:
            return "No coverage data available"

        summary = f"""
Coverage Analysis Summary:
--------------------------
Line Coverage: {self.coverage_data['coverage_percentage']:.1f}% ({self.coverage_data['covered_lines']}/{self.coverage_data['total_lines']} lines)
Branch Coverage: {self.coverage_data.get('branch_coverage_percentage', 0):.1f}% ({self.coverage_data.get('covered_branches', 0)}/{self.coverage_data.get('total_branches', 0)} branches)
Missing Lines: {', '.join(map(str, self.coverage_data['missing_lines'])) or 'None'}

Test Results:
-------------
Total Tests: {self.coverage_data['total_tests']}
Passed: {self.coverage_data['passed_tests']}
Failed: {self.coverage_data['failed_tests']}
Success Rate: {self.coverage_data['success_rate']:.1f}%
"""
        return summary
