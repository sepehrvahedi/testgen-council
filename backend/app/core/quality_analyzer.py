"""
Enhanced Test Quality Metrics
"""

import ast
import re
from typing import Dict, Any

from loguru import logger


class TestQualityAnalyzer:
    """Analyzes test suite quality beyond simple coverage"""

    def _get_empty_metrics(self, error: str = None) -> Dict[str, Any]:
        """
        Return empty/default metrics when quality analysis cannot be performed

        Args:
            error: Optional error message explaining why metrics are empty

        Returns:
            Dict with all metrics set to 0 or empty values
        """
        return {
            # Core metrics
            'assertion_density': 0.0,
            'diversity_score': 0.0,
            'edge_case_score': 0.0,
            'avg_test_complexity': 0.0,
            'assertion_types': {
                'equality': 0,
                'inequality': 0,
                'membership': 0,
                'truthiness': 0,
                'exceptions': 0,
                'comparisons': 0,
            },

            # Standard metrics
            'test_loc': 0,
            'source_loc': 0,
            'loc_efficiency': 0.0,
            'duplication_rate': 0.0,
            'exception_coverage_rate': 0.0,

            # Error tracking
            'error': error
        }

    def analyze_test_quality(
            self,
            test_code: str,
            function_code: str,
            function_name: str
    ) -> Dict[str, Any]:
        """
        Comprehensive test quality analysis

        Returns:
            Dict with multiple quality metrics
        """
        metrics = {}

        # Existing metrics
        metrics['assertion_density'] = self._calculate_assertion_density(test_code)
        metrics['diversity_score'] = self._calculate_diversity_score(test_code)
        metrics['edge_case_score'] = self._analyze_edge_cases(test_code, function_code)
        metrics['avg_test_complexity'] = self._calculate_test_complexity(test_code)
        metrics['assertion_types'] = self._analyze_assertion_types(test_code)

        # ✅ NEW STANDARD METRICS
        metrics['test_loc'] = self._count_test_loc(test_code)
        metrics['source_loc'] = self._count_source_loc(function_code)
        metrics['loc_efficiency'] = self._calculate_loc_efficiency(test_code, function_code)
        metrics['duplication_rate'] = self._calculate_duplication_rate(test_code)
        metrics['exception_coverage_rate'] = self._calculate_exception_coverage(test_code)

        return metrics

    # ============= EXISTING METHODS (unchanged) =============

    def _calculate_assertion_density(self, test_code: str) -> float:
        """
        Calculate assertions per test function
        Higher is generally better (more thorough testing)
        """
        try:
            tree = ast.parse(test_code)

            test_count = 0
            total_assertions = 0

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    test_count += 1

                    # Count assertions in this test
                    for stmt in ast.walk(node):
                        if isinstance(stmt, ast.Assert):
                            total_assertions += 1
                        elif isinstance(stmt, ast.Expr):
                            # Check for pytest-style assertions
                            if isinstance(stmt.value, ast.Call):
                                func = stmt.value.func
                                if isinstance(func, ast.Attribute):
                                    if func.attr in ['assertEqual', 'assertTrue', 'assertFalse',
                                                     'assertIn', 'assertRaises', 'assertIsNone']:
                                        total_assertions += 1

            if test_count == 0:
                return 0.0

            density = total_assertions / test_count
            logger.debug(f"Assertion density: {density:.2f} assertions/test ({total_assertions} assertions, {test_count} tests)")
            return round(density, 2)

        except Exception as e:
            logger.warning(f"Failed to calculate assertion density: {e}")
            return 0.0

    def _calculate_diversity_score(self, test_code: str) -> float:
        """
        Calculate test diversity based on:
        - Unique input patterns
        - Different assertion types
        - Variety of test scenarios

        Score from 0-100
        """
        try:
            tree = ast.parse(test_code)

            # Collect test characteristics
            input_patterns = set()
            assertion_patterns = set()
            test_names = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    test_names.add(node.name)

                    # Extract input patterns (function calls)
                    for stmt in ast.walk(node):
                        if isinstance(stmt, ast.Call):
                            # Get argument types
                            arg_pattern = []
                            for arg in stmt.args:
                                if isinstance(arg, ast.Constant):
                                    arg_pattern.append(f"{type(arg.value).__name__}:{arg.value}")
                                elif isinstance(arg, ast.List):
                                    arg_pattern.append(f"list:{len(arg.elts)}")
                                elif isinstance(arg, ast.Dict):
                                    arg_pattern.append(f"dict:{len(arg.keys)}")
                                else:
                                    arg_pattern.append(type(arg).__name__)

                            if arg_pattern:
                                input_patterns.add(tuple(arg_pattern))

                        # Track assertion patterns
                        if isinstance(stmt, ast.Compare):
                            ops = [type(op).__name__ for op in stmt.ops]
                            assertion_patterns.add(tuple(ops))

            # Calculate diversity components
            unique_inputs = len(input_patterns)
            unique_assertions = len(assertion_patterns)
            total_tests = len(test_names)

            if total_tests == 0:
                return 0.0

            # Diversity score formula
            input_diversity = min(100, (unique_inputs / total_tests) * 100)
            assertion_diversity = min(100, (unique_assertions / max(1, total_tests // 2)) * 100)

            diversity_score = (input_diversity * 0.6 + assertion_diversity * 0.4)

            logger.debug(f"Diversity score: {diversity_score:.1f}/100 ({unique_inputs} unique inputs, {unique_assertions} assertion types)")
            return round(diversity_score, 2)

        except Exception as e:
            logger.warning(f"Failed to calculate diversity score: {e}")
            return 0.0

    def _analyze_edge_cases(self, test_code: str, function_code: str) -> float:
        """
        Analyze how well tests cover edge cases:
        - Boundary values
        - Empty inputs
        - None values
        - Negative numbers
        - Large numbers
        - Special characters

        Score from 0-100
        """
        try:
            tree = ast.parse(test_code)

            edge_case_patterns = {
                'empty': False,      # [], '', {}, None
                'zero': False,       # 0
                'negative': False,   # negative numbers
                'boundary': False,   # INT_MAX, INT_MIN, edge values
                'large': False,      # Large numbers/strings
                'special': False,    # Special characters, unicode
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.Constant):
                    val = node.value

                    # Check empty
                    if val in [None, '', [], {}] or val == 0:
                        edge_case_patterns['empty'] = True
                    if val == 0:
                        edge_case_patterns['zero'] = True

                    # Check negative
                    if isinstance(val, (int, float)) and val < 0:
                        edge_case_patterns['negative'] = True

                    # Check large
                    if isinstance(val, int) and abs(val) > 1000:
                        edge_case_patterns['large'] = True
                    if isinstance(val, str) and len(val) > 100:
                        edge_case_patterns['large'] = True

                    # Check special characters
                    if isinstance(val, str) and re.search(r'[^\w\s]', val):
                        edge_case_patterns['special'] = True

                # Check for boundary testing (comparisons with limits)
                if isinstance(node, ast.Compare):
                    for comparator in node.comparators:
                        if isinstance(comparator, ast.Constant):
                            val = comparator.value
                            if isinstance(val, int) and val in [0, 1, -1, 2**31-1, -2**31]:
                                edge_case_patterns['boundary'] = True

            # Calculate score
            covered = sum(edge_case_patterns.values())
            total_categories = len(edge_case_patterns)
            score = (covered / total_categories) * 100

            logger.debug(f"Edge case score: {score:.1f}/100 (covered: {covered}/{total_categories})")
            return round(score, 2)

        except Exception as e:
            logger.warning(f"Failed to analyze edge cases: {e}")
            return 0.0

    def _calculate_test_complexity(self, test_code: str) -> float:
        """
        Calculate average cyclomatic complexity of tests
        Lower is often better (simpler, more focused tests)
        """
        try:
            tree = ast.parse(test_code)

            complexities = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    complexity = self._cyclomatic_complexity(node)
                    complexities.append(complexity)

            if not complexities:
                return 0.0

            avg_complexity = sum(complexities) / len(complexities)
            logger.debug(f"Average test complexity: {avg_complexity:.2f}")
            return round(avg_complexity, 2)

        except Exception as e:
            logger.warning(f"Failed to calculate test complexity: {e}")
            return 0.0

    def _cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _analyze_assertion_types(self, test_code: str) -> Dict[str, int]:
        """
        Categorize types of assertions used
        Helps understand test thoroughness
        """
        assertion_types = {
            'equality': 0,
            'inequality': 0,
            'membership': 0,
            'truthiness': 0,
            'exceptions': 0,
            'comparisons': 0,
        }

        try:
            tree = ast.parse(test_code)

            for node in ast.walk(tree):
                if isinstance(node, ast.Assert):
                    test_expr = node.test

                    if isinstance(test_expr, ast.Compare):
                        for op in test_expr.ops:
                            if isinstance(op, ast.Eq):
                                assertion_types['equality'] += 1
                            elif isinstance(op, ast.NotEq):
                                assertion_types['inequality'] += 1
                            elif isinstance(op, ast.In):
                                assertion_types['membership'] += 1
                            elif isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE)):
                                assertion_types['comparisons'] += 1
                    elif isinstance(test_expr, ast.UnaryOp):
                        assertion_types['truthiness'] += 1
                    else:
                        assertion_types['truthiness'] += 1

                # Check for pytest.raises
                if isinstance(node, ast.With):
                    for item in node.items:
                        if isinstance(item.context_expr, ast.Call):
                            func = item.context_expr.func
                            if isinstance(func, ast.Attribute) and func.attr == 'raises':
                                assertion_types['exceptions'] += 1

            logger.debug(f"Assertion types: {assertion_types}")
            return assertion_types

        except Exception as e:
            logger.warning(f"Failed to analyze assertion types: {e}")
            return assertion_types

    # ============= NEW STANDARD METRICS =============

    def _count_test_loc(self, test_code: str) -> int:
        """
        Count Lines of Code (LOC) in test suite
        Standard metric: Shows test suite size
        """
        try:
            # Count non-empty, non-comment lines
            lines = [line.strip() for line in test_code.split('\n')]
            loc = sum(1 for line in lines if line and not line.startswith('#'))

            logger.debug(f"Test LOC: {loc}")
            return loc
        except Exception as e:
            logger.warning(f"Failed to count test LOC: {e}")
            return 0

    def _count_source_loc(self, function_code: str) -> int:
        """
        Count Lines of Code (LOC) in source function
        """
        try:
            lines = [line.strip() for line in function_code.split('\n')]
            loc = sum(1 for line in lines if line and not line.startswith('#'))

            logger.debug(f"Source LOC: {loc}")
            return loc
        except Exception as e:
            logger.warning(f"Failed to count source LOC: {e}")
            return 0

    def _calculate_loc_efficiency(self, test_code: str, function_code: str) -> float:
        """
        Calculate Tests-per-LOC efficiency metric
        test_loc / source_loc

        Standard metric showing how concise your test generation is
        """
        try:
            test_loc = self._count_test_loc(test_code)
            source_loc = self._count_source_loc(function_code)

            if source_loc == 0:
                return 0.0

            efficiency = test_loc / source_loc
            logger.debug(f"LOC Efficiency: {efficiency:.2f} (test_loc={test_loc}, source_loc={source_loc})")
            return round(efficiency, 2)
        except Exception as e:
            logger.warning(f"Failed to calculate LOC efficiency: {e}")
            return 0.0

    def _calculate_duplication_rate(self, test_code: str) -> float:
        """
        Calculate code duplication rate in test suite
        Measures redundancy - lower is better

        Uses AST to find structurally similar tests
        Score from 0-100 (percentage of duplicate tests)
        """
        try:
            tree = ast.parse(test_code)

            test_functions = [
                node for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')
            ]

            if len(test_functions) < 2:
                return 0.0

            # Extract structural signatures of each test
            signatures = []
            for func in test_functions:
                sig = self._get_test_signature(func)
                signatures.append(sig)

            # Count duplicates
            duplicate_count = 0
            seen = set()

            for sig in signatures:
                if sig in seen:
                    duplicate_count += 1
                else:
                    seen.add(sig)

            duplication_rate = (duplicate_count / len(test_functions)) * 100

            logger.debug(f"Duplication rate: {duplication_rate:.1f}% ({duplicate_count}/{len(test_functions)} duplicate tests)")
            return round(duplication_rate, 2)

        except Exception as e:
            logger.warning(f"Failed to calculate duplication rate: {e}")
            return 0.0

    def _get_test_signature(self, func_node: ast.FunctionDef) -> str:
        """
        Get structural signature of a test function
        Ignores variable names and literal values, focuses on structure
        """
        try:
            # Extract key structural elements
            elements = []

            for node in ast.walk(func_node):
                # Track function calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        elements.append(f"call:{node.func.id}")
                    elif isinstance(node.func, ast.Attribute):
                        elements.append(f"call:{node.func.attr}")

                # Track assertion operations
                if isinstance(node, ast.Compare):
                    ops = [type(op).__name__ for op in node.ops]
                    elements.append(f"compare:{'_'.join(ops)}")

                # Track control flow
                if isinstance(node, ast.If):
                    elements.append("if")
                elif isinstance(node, ast.For):
                    elements.append("for")
                elif isinstance(node, ast.While):
                    elements.append("while")

            # Create signature
            return '|'.join(sorted(elements))
        except Exception:
            return ""

    def _calculate_exception_coverage(self, test_code: str) -> float:
        """
        Calculate percentage of tests that handle exceptions
        Standard metric for robustness testing

        Score from 0-100
        """
        try:
            tree = ast.parse(test_code)

            test_count = 0
            exception_test_count = 0

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                    test_count += 1

                    # Check if test handles exceptions
                    has_exception = False

                    for child in ast.walk(node):
                        # pytest.raises
                        if isinstance(child, ast.With):
                            for item in child.items:
                                if isinstance(item.context_expr, ast.Call):
                                    func = item.context_expr.func
                                    if isinstance(func, ast.Attribute) and func.attr == 'raises':
                                        has_exception = True
                                        break

                        # try/except blocks
                        if isinstance(child, ast.Try):
                            has_exception = True
                            break

                        # assertRaises
                        if isinstance(child, ast.Call):
                            if isinstance(child.func, ast.Attribute):
                                if child.func.attr == 'assertRaises':
                                    has_exception = True
                                    break

                    if has_exception:
                        exception_test_count += 1

            if test_count == 0:
                return 0.0

            coverage_rate = (exception_test_count / test_count) * 100

            logger.debug(f"Exception coverage: {coverage_rate:.1f}% ({exception_test_count}/{test_count} tests)")
            return round(coverage_rate, 2)

        except Exception as e:
            logger.warning(f"Failed to calculate exception coverage: {e}")
            return 0.0
