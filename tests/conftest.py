import sys
from pathlib import Path

# Make the repository root importable so `desktop` and `relay` resolve
# regardless of the working directory pytest is invoked from.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
