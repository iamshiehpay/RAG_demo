"""Controlled Router connection failure and same-question recovery fixture."""

import runpy
from pathlib import Path

import httpx

scope = runpy.run_path(str(Path(__file__).with_name("server.py")))
llm = scope["llm"]
llm.scripts.clear()
llm.scripts.extend(
    [
        httpx.ConnectError("All connection attempts failed"),
        "not JSON",
        "Recovered Router question [C1].",
    ]
)
for gate in llm.gates.values():
    gate.set()
app = scope["app"]
