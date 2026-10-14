# Ticket12 Main integration

Main checkpoint `abd7fc7c696fe4347c6a1561500772e432bba2a0` contains the ff-only merge of reviewed frontend candidate `af6b9f3`, D15's two approved AGENTS cell changes and Main tracker/diagnostic records. Backend and event contract were unchanged. The reviewed source was preserved through the docs-only rebase; full/scoped Review and actual runtime verification are in [review.md](review.md).

## Verification

One complete deterministic run in the Main workspace used `PYTHONPATH=src:. .venv/bin/python -m pytest -q`: **327 passed, 3 eval deselected, zero skipped, 6 warnings, exit0**, 252.49s. No rerun or cloud eval. Main Python3.12.10/import paths, settings, pipeline58005fcc and both PDF fixtures were recorded and checked. PyMuPDF/Starlette deprecation warnings are preserved.

- [Environment](integration-environment.json)
- [Full console output](integration-full-suite.txt)
- [Exact result and process closure](integration-result.json)
- [HTTP readiness](integration-http-readiness.json): existing user server8101 returns200 for root, newJS/CSS and bundledfont; no server restart or user-session mutation. This is not UI acceptance.

The previous frontend evidence remains valid for this source:36 final scripted runs/1289PASSassertions, typecheck/build/source/events, independent scoped Review and real compare/global smoke. The remaining manual UI check is [D1–D7](../final-acceptance/manual-qa-checklist.md), **NOT_EXECUTED until the human reports results**. Existing backend warning text and Review's focus/Safari limitations are retained, not silently fixed or declared tested.

A9 backend correction is separately authorized in Ticket13/D14B and is not included in this Main version. Original refusal and the isolated system-warning attribution remainFAIL in [manual-a9](../ticket-11/manual-a9/report.md). The original N3 reports are unchanged.

Test execution role nova-check12-valo owns no remaining process/server/browser/extra temporary path. Main owns these evidence files and will save the post-test records with the next integration checkpoint per LAT. Frontend worktree/temp cleanup is tracked separately in the shared task card; user-owned8101/8201/Ollama are preserved.
