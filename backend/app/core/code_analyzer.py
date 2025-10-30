"""
Code analysis module for extracting function metadata and generating context
"""

import ast
import inspect
from typing import Dict, Any, Optional, List
from loguru import logger

from app.utils.exceptions import CodeAnalysisError


class CodeAnalyzer:
    """Analyzes Python function code to extract metadata and generate test context"""

    def __init__(self):
        self.function_metadata: Dict[str, Any] = {}

    def analyze_function(self, function_code: str, function_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze function code and extract comprehensive metadata

        Args:
            function_code: Source code of the function
            function_name: Optional function name (auto-detected if not provided)

        Returns:
            Dictionary containing function metadata

        Raises:
            CodeAnalysisError: If code analysis fails
        """
        try:
            # Parse the AST
            tree = ast.parse(function_code)

            # Find function definition
            func_def = self._find_function_def(tree, function_name)

            if not func_def:
                raise CodeAnalysisError(
                    "No function definition found in code",
                    details={"code_length": len(function_code)}
                )

            # Extract metadata
            metadata = {
                "name": func_def.name,
                "signature": self._extract_signature(func_def),
                "parameters": self._extract_parameters(func_def),
                "return_type": self._extract_return_type(func_def),
                "docstring": ast.get_docstring(func_def),
                "decorators": self._extract_decorators(func_def),
                "raises": self._extract_raises(func_def),
                "complexity": self._calculate_complexity(func_def),
                "source_code": function_code,
                "line_count": len(function_code.splitlines()),
                "has_async": isinstance(func_def, ast.AsyncFunctionDef)
            }

            self.function_metadata = metadata
            logger.info(f"Analyzed function: {metadata['name']}")

            return metadata

        except SyntaxError as e:
            raise CodeAnalysisError(
                f"Syntax error in function code: {str(e)}",
                details={"line": e.lineno, "offset": e.offset}
            )
        except Exception as e:
            logger.error(f"Code analysis failed: {e}", exc_info=True)
            raise CodeAnalysisError(
                f"Failed to analyze code: {str(e)}",
                details={"error_type": type(e).__name__}
            )

    def _find_function_def(
            self,
            tree: ast.AST,
            function_name: Optional[str] = None
    ) -> Optional[ast.FunctionDef]:
        """Find function definition in AST"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if function_name is None or node.name == function_name:
                    return node
        return None

    def _extract_signature(self, func_def: ast.FunctionDef) -> str:
        """Extract function signature as string"""
        try:
            args = func_def.args
            params = []

            # Regular arguments
            for arg in args.args:
                param = arg.arg
                if arg.annotation:
                    param += f": {ast.unparse(arg.annotation)}"
                params.append(param)

            # *args
            if args.vararg:
                param = f"*{args.vararg.arg}"
                if args.vararg.annotation:
                    param += f": {ast.unparse(args.vararg.annotation)}"
                params.append(param)

            # **kwargs
            if args.kwarg:
                param = f"**{args.kwarg.arg}"
                if args.kwarg.annotation:
                    param += f": {ast.unparse(args.kwarg.annotation)}"
                params.append(param)

            signature = f"{func_def.name}({', '.join(params)})"

            # Add return type
            if func_def.returns:
                signature += f" -> {ast.unparse(func_def.returns)}"

            return signature

        except Exception as e:
            logger.warning(f"Failed to extract signature: {e}")
            return f"{func_def.name}(...)"

    def _extract_parameters(self, func_def: ast.FunctionDef) -> List[Dict[str, Any]]:
        """Extract parameter information"""
        parameters = []
        args = func_def.args

        # Get defaults
        defaults = [None] * (len(args.args) - len(args.defaults)) + args.defaults

        for arg, default in zip(args.args, defaults):
            param_info = {
                "name": arg.arg,
                "type": ast.unparse(arg.annotation) if arg.annotation else None,
                "default": ast.unparse(default) if default else None,
                "kind": "positional"
            }
            parameters.append(param_info)

        # *args
        if args.vararg:
            parameters.append({
                "name": args.vararg.arg,
                "type": ast.unparse(args.vararg.annotation) if args.vararg.annotation else None,
                "default": None,
                "kind": "var_positional"
            })

        # **kwargs
        if args.kwarg:
            parameters.append({
                "name": args.kwarg.arg,
                "type": ast.unparse(args.kwarg.annotation) if args.kwarg.annotation else None,
                "default": None,
                "kind": "var_keyword"
            })

        return parameters

    def _extract_return_type(self, func_def: ast.FunctionDef) -> Optional[str]:
        """Extract return type annotation"""
        if func_def.returns:
            return ast.unparse(func_def.returns)
        return None

    def _extract_decorators(self, func_def: ast.FunctionDef) -> List[str]:
        """Extract decorator names"""
        decorators = []
        for decorator in func_def.decorator_list:
            try:
                decorators.append(ast.unparse(decorator))
            except:
                decorators.append(str(decorator))
        return decorators

    def _extract_raises(self, func_def: ast.FunctionDef) -> List[str]:
        """Extract exceptions that the function might raise"""
        raises = set()

        for node in ast.walk(func_def):
            if isinstance(node, ast.Raise):
                if node.exc:
                    if isinstance(node.exc, ast.Call):
                        if isinstance(node.exc.func, ast.Name):
                            raises.add(node.exc.func.id)
                    elif isinstance(node.exc, ast.Name):
                        raises.add(node.exc.id)

        return list(raises)

    def _calculate_complexity(self, func_def: ast.FunctionDef) -> Dict[str, int]:
        """Calculate code complexity metrics"""
        complexity = {
            "cyclomatic": 1,  # Base complexity
            "branches": 0,
            "loops": 0,
            "function_calls": 0,
            "logical_operators": 0
        }

        for node in ast.walk(func_def):
            # Cyclomatic complexity contributors
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity["cyclomatic"] += 1

            # Branch statements
            if isinstance(node, (ast.If, ast.IfExp)):
                complexity["branches"] += 1

            # Loops
            if isinstance(node, (ast.For, ast.While)):
                complexity["loops"] += 1

            # Function calls
            if isinstance(node, ast.Call):
                complexity["function_calls"] += 1

            # Logical operators
            if isinstance(node, ast.BoolOp):
                complexity["logical_operators"] += len(node.values) - 1
                complexity["cyclomatic"] += len(node.values) - 1

        return complexity

    def generate_test_context(self) -> str:
        """
        Generate comprehensive context for LLM test generation

        Returns:
            Formatted context string
        """
        if not self.function_metadata:
            raise CodeAnalysisError("No function metadata available. Run analyze_function first.")

        meta = self.function_metadata

        context = f"""# Function Analysis for Test Generation

## Function Under Test: `{meta['name']}`

### Complete Function Code

```python
{meta['source_code']}
```

### Signature
```python
{meta['signature']}
```

### Documentation
{meta['docstring'] or 'No docstring provided'}

### Parameters
"""

        for param in meta['parameters']:
            context += f"- **{param['name']}**"
        if param['type']:
            context += f" ({param['type']})"
        if param['default']:
            context += f" = {param['default']}"
        context += f" [{param['kind']}]\n"

        if meta['return_type']:
            context += f"\n### Return Type\n`{meta['return_type']}`\n"

        if meta['raises']:
            context += f"\n### Raises\n"
        for exc in meta['raises']:
            context += f"- `{exc}`\n"

        if meta['decorators']:
            context += f"\n### Decorators\n"
        for dec in meta['decorators']:
            context += f"- `{dec}`\n"

        context += f"""
### Complexity Metrics
- Cyclomatic Complexity: {meta['complexity']['cyclomatic']}
- Branches: {meta['complexity']['branches']}
- Loops: {meta['complexity']['loops']}
- Function Calls: {meta['complexity']['function_calls']}
"""

        return context


    def get_test_hints(self) -> Dict[str, List[str]]:
        """
        Generate test hints based on function analysis

        Returns:
            Dictionary of test categories and hints
        """
        if not self.function_metadata:
            return {}

        meta = self.function_metadata
        hints = {
            "positive": [],
            "negative": [],
            "edge": [],
            "security": [],
            "performance": []
        }

        # Positive cases
        hints["positive"].append(f"Test normal execution with typical {meta['name']} inputs")

        # Parameter-based hints
        for param in meta['parameters']:
            if param['type']:
                if 'int' in param['type'].lower():
                    hints["edge"].append(f"Test {param['name']} with 0, negative, and max int values")
                elif 'str' in param['type'].lower():
                    hints["edge"].append(f"Test {param['name']} with empty string, unicode, very long string")
                elif 'list' in param['type'].lower() or 'dict' in param['type'].lower():
                    hints["edge"].append(f"Test {param['name']} with empty collection")
                    hints["negative"].append(f"Test {param['name']} with None")

        # Exception-based hints
        for exc in meta['raises']:
            hints["negative"].append(f"Test that {exc} is raised appropriately")

        # Complexity-based hints
        if meta['complexity']['branches'] > 0:
            hints["positive"].append("Test all conditional branches")

        if meta['complexity']['loops'] > 0:
            hints["edge"].append("Test loop with 0, 1, and many iterations")
            hints["performance"].append("Test loop performance with large datasets")

        # Security hints
        if any(param['type'] and 'str' in param['type'].lower() for param in meta['parameters']):
            hints["security"].append("Test input validation and sanitization")
            hints["security"].append("Test SQL injection prevention (if applicable)")

        # Async hints
        if meta['has_async']:
            hints["positive"].append("Test async execution and awaiting")
            hints["negative"].append("Test timeout scenarios")

        return hints
