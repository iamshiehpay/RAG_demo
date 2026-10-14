"""Rerun the previously reviewed browser suites without overwriting historic proof."""

import hashlib
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
ROOT = BASE.parents[2]
KIND = sys.argv[1]
assert KIND in ("crlf", "review-corrections")
original = BASE / KIND / "browser-regressions.py"
target = OUT / KIND
(target / "evidence").mkdir(parents=True, exist_ok=True)
code = original.read_text()
code = code.replace("OUT = Path(__file__).resolve().parent", f"OUT = Path({str(target)!r})")
code = code.replace("ROOT = OUT.parents[3]", f"ROOT = Path({str(ROOT)!r})")
code = code.replace("BASE = OUT.parent", f"BASE = Path({str(BASE)!r})")
code = code.replace(
    "OUT.parent.joinpath('scripted-events.js')",
    f"Path({str(BASE)!r}).joinpath('scripted-events.js')",
)
(target / "original-suite.json").write_text(
    json.dumps(
        {
            "path": str(original.relative_to(ROOT)),
            "sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
            "adaptation": (
                "Only evidence output, ROOT, and existing scripted-events.js paths changed."
            ),
        },
        indent=2,
    )
)
sys.argv = [str(original), "after"]
exec(compile(code, str(original), "exec"), {"__file__": str(original), "__name__": "__main__"})
