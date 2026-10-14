import subprocess
import sys


def test_frontend_types_match_backend_event_models():
    result = subprocess.run(
        [sys.executable, "scripts/generate_event_types.py", "--check"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
