import json
import csv
import random
import tempfile
import subprocess
import sys
from pathlib import Path

def load_dataset(json_path):
    """Load the JSON dataset"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data['functions']

def validate_function_syntax(function_code):
    """
    Check if the function has valid Python syntax and can be parsed.
    Returns True if syntax is valid, False otherwise.
    """
    try:
        compile(function_code, '<string>', 'exec')
        return True
    except SyntaxError:
        return False

def function_execution(function_code, function_name):
    """
    Test if the function can be executed without runtime errors.
    Creates a temporary file and tries to import/run the function.

    Returns (success, error_message)
    """
    # Create a temporary Python file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        temp_file = f.name

        # Write the function code
        f.write(function_code)
        f.write('\n\n')

        # Add a simple test: just try to import/define the function
        # We don't call it, just check if it can be loaded
        f.write(f'# Test: Check if {function_name} is defined\n')
        f.write(f'if __name__ == "__main__":\n')
        f.write(f'    assert callable({function_name}), "Function is not callable"\n')
        f.write(f'    print("SUCCESS: {function_name} is valid")\n')

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

        # Check if execution was successful
        if result.returncode == 0 and 'SUCCESS' in result.stdout:
            return True, None
        else:
            error = result.stderr or result.stdout or 'Unknown error'
            return False, error

    except subprocess.TimeoutExpired:
        Path(temp_file).unlink(missing_ok=True)
        return False, 'Execution timeout'
    except Exception as e:
        Path(temp_file).unlink(missing_ok=True)
        return False, str(e)

def select_valid_functions(functions, target_count=50, max_attempts=200):
    """
    Randomly select and validate functions until we have target_count valid ones.

    Args:
        functions: List of function dictionaries from JSON
        target_count: Number of valid functions to collect
        max_attempts: Maximum number of functions to try

    Returns:
        List of valid function dictionaries
    """
    valid_functions = []
    attempted = set()

    # Shuffle the functions list
    shuffled_functions = functions.copy()
    random.shuffle(shuffled_functions)

    print(f"🎯 Target: {target_count} valid functions")
    print(f"📊 Total available: {len(functions)} functions")
    print("=" * 80)

    for idx, func in enumerate(shuffled_functions):
        if len(valid_functions) >= target_count:
            break

        if idx >= max_attempts:
            print(f"\n⚠️ Reached max attempts ({max_attempts})")
            break

        function_code = func['source']
        function_name = func['name']

        # Skip if already attempted
        if function_name in attempted:
            continue

        attempted.add(function_name)

        print(f"\n[{len(valid_functions) + 1}/{target_count}] Testing: {function_name}")
        print(f"   Category: {func.get('category', 'unknown')}")
        print(f"   File: {func.get('file', 'unknown')}")

        # Step 1: Check syntax
        if not validate_function_syntax(function_code):
            print("   ❌ Syntax error - SKIPPED")
            continue

        print("   ✅ Syntax valid")

        # Step 2: Test execution
        success, error = function_execution(function_code, function_name)

        if success:
            print("   ✅ Execution successful - ADDED")
            valid_functions.append(func)
        else:
            print(f"   ❌ Execution failed: {error[:100]}")

    print("\n" + "=" * 80)
    print(f"✅ Collected {len(valid_functions)} valid functions")
    return valid_functions

def save_to_csv(functions, output_path):
    """Save selected functions to CSV"""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow(['function_code', 'function_name'])

        # Write data
        for func in functions:
            writer.writerow([func['source'], func['name']])

    print(f"💾 Saved to: {output_path}")

def main():
    # Set random seed for reproducibility (optional)
    random.seed(42)

    # Paths
    json_path = '/Users/sepehr/IdeaProjects/testgen-council/notebooks/data/python_algorithms_dataset.json'
    output_csv = '/Users/sepehr/IdeaProjects/testgen-council/notebooks/data/algorithm_50.csv'

    print("🚀 Starting function selection and validation")
    print("=" * 80)

    # Load dataset
    print(f"📂 Loading dataset from: {json_path}")
    functions = load_dataset(json_path)
    print(f"✅ Loaded {len(functions)} functions")

    # Select and validate functions
    valid_functions = select_valid_functions(
        functions,
        target_count=50,
        max_attempts=200  # Try up to 200 functions to find 50 valid ones
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

    # Category distribution
    categories = {}
    for func in valid_functions:
        cat = func.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\n📈 Category distribution:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:10]:
        print(f"   {cat}: {count}")

    print(f"\n✅ Done! CSV saved to: {output_csv}")

if __name__ == "__main__":
    main()
