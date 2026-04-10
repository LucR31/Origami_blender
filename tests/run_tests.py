import sys
from pathlib import Path

# make addon root importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from tests.framework import run_tests
import tests.test_core  # IMPORTANT: ensures decorators register tests

if __name__ == "__main__":
    run_tests()