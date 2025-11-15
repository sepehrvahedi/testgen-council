import json
import csv
import random
import tempfile
import subprocess
import sys
import ast
from pathlib import Path

def load_mbpp_dataset(json_path):
    """Load the MBPP JSON dataset"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def extract_function_signature(function_code):
    """
    Extract function name and parameters from the function code.
    Returns (function_name, param_count) or (None, None) if parsing fails.
    """
    try:
        tree = ast.parse(function_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get parameter count (excluding self, *args, **kwargs)
                param_count = len([arg for arg in node.args.args
                                   if arg.arg not in ['self']])
                return node.name, param_count
        return None, None
    except:
        return None, None

def function_execution(function_code, test_list, test_imports):
    """
    Test if the function can be executed using the provided test cases.

    Returns (success, error_message, passed_tests, total_tests)
    """
    # Create a temporary Python file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        temp_file = f.name

        # Write imports
        for import_stmt in test_imports:
            f.write(import_stmt + '\n')

        # Write the function code
        f.write('\n')
        f.write(function_code)
        f.write('\n\n')

        # Add test code
        f.write('if __name__ == "__main__":\n')
        f.write('    import sys\n')
        f.write('    success_count = 0\n')
        f.write(f'    total_tests = {len(test_list)}\n')
        f.write('\n')

        # Add each test case
        for idx, test_case in enumerate(test_list):
            f.write(f'    # Test case {idx + 1}\n')
            f.write(f'    try:\n')
            f.write(f'        {test_case}\n')
            f.write(f'        success_count += 1\n')
            f.write(f'        print(f"✓ Test {idx + 1} passed")\n')
            f.write(f'    except AssertionError as e:\n')
            f.write(f'        print(f"✗ Test {idx + 1} failed: Assertion Error", file=sys.stderr)\n')
            f.write(f'    except Exception as e:\n')
            f.write(f'        print(f"✗ Test {idx + 1} failed: {{type(e).__name__}}: {{e}}", file=sys.stderr)\n')
            f.write('\n')

        # Final status
        f.write('    if success_count == total_tests:\n')
        f.write('        print(f"SUCCESS: All {total_tests} tests passed")\n')
        f.write('        sys.exit(0)\n')
        f.write('    else:\n')
        f.write('        print(f"PARTIAL: {success_count}/{total_tests} tests passed", file=sys.stderr)\n')
        f.write('        sys.exit(1)\n')

    try:
        # Run the temporary file in a subprocess
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=5  # 5 second timeout
        )

        # Clean up
        Path(temp_file).unlink(missing_ok=True)

        # Parse results
        passed = result.stdout.count('✓')
        total = len(test_list)

        # Check if execution was successful
        if result.returncode == 0 and 'SUCCESS' in result.stdout:
            return True, None, passed, total
        else:
            # Capture the actual error
            error = result.stderr.strip() or result.stdout.strip() or 'Unknown error'
            # Only show first line of error for cleaner output
            error_summary = error.split('\n')[0] if error else 'Function execution failed'
            return False, error_summary, passed, total

    except subprocess.TimeoutExpired:
        Path(temp_file).unlink(missing_ok=True)
        return False, 'Execution timeout (possibly infinite loop)', 0, len(test_list)
    except Exception as e:
        Path(temp_file).unlink(missing_ok=True)
        return False, str(e), 0, len(test_list)

def select_valid_functions(problems, target_count=50, max_attempts=200):
    """
    Randomly select and validate functions until we have target_count valid ones.

    Args:
        problems: List of problem dictionaries from MBPP JSON
        target_count: Number of valid functions to collect
        max_attempts: Maximum number of functions to try

    Returns:
        List of valid problem dictionaries with validation results
    """
    valid_functions = []
    attempted = set()

    # Shuffle the problems list
    shuffled_problems = problems.copy()
    random.shuffle(shuffled_problems)

    print(f"🎯 Target: {target_count} valid functions")
    print(f"📊 Total available: {len(problems)} functions")
    print("=" * 80)

    for idx, problem in enumerate(shuffled_problems):
        if len(valid_functions) >= target_count:
            break

        if idx >= max_attempts:
            print(f"\n⚠️ Reached max attempts ({max_attempts})")
            break

        task_id = problem['task_id']
        function_code = problem['code']
        test_list = problem['test_list']
        test_imports = problem.get('test_imports', [])
        prompt = problem['prompt']

        # Skip if already attempted
        if task_id in attempted:
            continue

        attempted.add(task_id)

        # Extract function name
        function_name, _ = extract_function_signature(function_code)

        print(f"\n[{len(valid_functions) + 1}/{target_count}] Testing Task ID: {task_id}")
        print(f"   Function: {function_name}")
        print(f"   Prompt: {prompt[:60]}..." if len(prompt) > 60 else f"   Prompt: {prompt}")
        print(f"   Tests: {len(test_list)} test cases")

        # Test execution
        success, error, passed, total = function_execution(
            function_code, test_list, test_imports
        )

        if success:
            print(f"   ✅ All {total} tests passed - ADDED")
            problem['validation_status'] = 'success'
            problem['tests_passed'] = passed
            problem['tests_total'] = total
            valid_functions.append(problem)
        else:
            if passed > 0:
                print(f"   ⚠️ Partial success: {passed}/{total} tests passed")
                print(f"   Error: {error}")
            else:
                print(f"   ❌ All tests failed: {error}")

    print("\n" + "=" * 80)
    print(f"✅ Collected {len(valid_functions)} valid functions")
    return valid_functions

def save_to_csv(problems, output_path):
    """Save selected functions to CSV"""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow(['function_code', 'function_name', 'prompt', 'task_id', 'tests_count'])

        # Write data
        for problem in problems:
            function_name, _ = extract_function_signature(problem['code'])
            writer.writerow([
                problem['code'],
                function_name,
                problem['prompt'],
                problem['task_id'],
                len(problem['test_list'])
            ])

    print(f"💾 Saved to: {output_path}")

def main():
    # Set random seed for reproducibility
    random.seed(42)

    # Paths
    json_path = '/Users/sepehr/IdeaProjects/testgen-council/notebooks/data/mbpp.json'
    output_csv = '/Users/sepehr/IdeaProjects/testgen-council/notebooks/data/mbpp_50.csv'

    print("🚀 Starting MBPP function selection and validation")
    print("=" * 80)

    # Load dataset
    print(f"📂 Loading dataset from: {json_path}")
    problems = load_mbpp_dataset(json_path)
    print(f"✅ Loaded {len(problems)} problems")

    # Select and validate functions
    valid_functions = select_valid_functions(
        problems,
        target_count=50,
        max_attempts=150  # Try up to 150 functions to find 50 valid ones
    )

    if len(valid_functions) < 50:
        print(f"\n⚠️ Warning: Only found {len(valid_functions)} valid functions (target was 50)")
        response = input("Continue with these functions? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return

    # Save to CSV
    save_to_csv(valid_functions, output_csv)

    # Summary statistics
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"Total functions validated: {len(valid_functions)}")

    # Test count distribution
    test_counts = {}
    for problem in valid_functions:
        count = len(problem['test_list'])
        test_counts[count] = test_counts.get(count, 0) + 1

    print(f"\n📈 Test count distribution:")
    for count in sorted(test_counts.keys()):
        print(f"   {count} tests: {test_counts[count]} functions")

    # Average tests per function
    avg_tests = sum(len(p['test_list']) for p in valid_functions) / len(valid_functions)
    print(f"\n📊 Average tests per function: {avg_tests:.1f}")

    print(f"\n✅ Done! CSV saved to: {output_csv}")

if __name__ == "__main__":
    main()
