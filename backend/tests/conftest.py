"""Tests run offline: no API key, no network. The LLM calls are replaced with canned answers where needed."""
import os
import sys
from pathlib import Path

os.environ.setdefault("OPENAI_API_KEY", "")
os.environ.setdefault("DEBUG", "False")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

CLASSIFY = '''def classify(n: int) -> str:
    """Classify an integer."""
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        return "negative"
    if n == 0:
        return "zero"
    if n % 2 == 0:
        return "even"
    return "odd"
'''
