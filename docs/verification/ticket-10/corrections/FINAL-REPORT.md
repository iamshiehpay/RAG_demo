# Issue10 D06 correction handoff

Review base: `588638d67ab0166ddee98c22c2ad4a7a2296b82b`. Passing source corrections are checkpointed for scoped Review, but fresh realN3 remains incomplete because both authorized uploads failed closed. This report does not claim integration approval or overall acceptance. Main dispatches the next scoped Review and post-merge QA. D01–D06 apply; optional numeric/wording tuning has stopped.

## Changes and source failure

The original source included `against` on physicalp28, a separate footer `28`, then `expert judgements` onp29. The90%-height rule failed because the footer's top is83.97% of page height. It became a false validation count in original saved Section response27, Group response87, Document response89 and all three Global answers. The primary statement is THREE expert-annotated papers; Table9p31 counts447/304 criterion evaluations. Citation IDs remained valid but cited corrupted source meaning.

`pdf_parser._page_folios` now requires isolated digit-only margin blocks, separation from neighboring body/heading/table labels, sequential logical-number offset and recurring normalized geometry on another page. It supports upper/lower and recurring alternating positions, without paper-specific numbers/fonts. `_lines` excludes only corroborated folios. Public upload/ask regressions use top/bottom folios7/8 and28/29 and retain body99, table23, heading2 and legitimate margin41. Published Citation sources still resolve back to original Chunk IDs. Ambiguous or uncorroborated single-page integers remain evidence; this is not a universal header/footer-layout detector.

The live harness now accepts empty string/None via `assert not report.upload_error`, while rejecting nonempty upload errors. D05/D06 semantic/forbidden FAIL does not by itself fail the pytest command; ingestion,80–500,>6K/Group, appendix and budget assertions remain.

Already-produced numeric changes are retained: parenthesized postpositive setting labels outrank preceding unrelated settings; explicit unchanged/shared metrics retain named comparison owners; primary table row label/metric-column header determines ownership, not later “Compared with” cells. Generic positive/reversed adversarial cases pass. No further optional checker tuning, criteria changes, silent regrading or production answer-prompt changes.

## Historical six-answer run — preserved unchanged

`eval/reports/issue10-final-n3.md` and raw companions remain the original run. Pytest exited1 on the now-fixed empty-string-vs-None sentinel after six finalized answers. Raw numeric: sourceCitation3/3, Router3/3, expert_agreement0/3, forbidden3/3. Raw Global: Router3/3, whole_document_coverage0/3.

Manual primary-source comparison: all three numeric answers state three expert-annotated papers, AllN447/accuracy0.966, InfoFoundN304/accuracy0.951 (lower), F1 unchanged0.762 in both. Judge excerpts1/3 omit the correct first three-paper sentence; the verifier then correctly rejects missing subset evidence. Excerpt2 includes it, but the old binder rejects value-before-setting labels/sharedF1. These evaluator defects contaminate the apparent0/3 answer-quality rate; the raw rate is not changed. The previous table checker also falsely accepted reversed Control/Filtered accuracy when the other setting appeared under “Compared with”; the new deterministic adversarial case rejects it. Known checker limitations beyond these bounded fixes remain reportable, nonblocking underD06.

Original Global outputs actually contain false28judgments, caused by footer contamination and Group compression superseding the correct§8.1 scope. Repetition1 also blends a system table-reconstruction caveat into author Limitations. Broad judge failures have empty evidence and do not identify every missing theme; no exhaustive semantic audit is claimed.

Original ingestion:31 Section Summaries7,334tokens,88–410, one Group layer/two groups,110calls, max estimated prompt+reservation9,746/reported9,479. Length Section7.1 call30 retried at34 (31–33 unrelated parallel completions); Group call86 retried at87. Both stopped; published nodes equal successful replacement outputs with required warning, not failed drafts. Gateway terminal Trace precedes LLMTruncated, local text is discarded, original evidence reused once; complete tree/cache/Ready follows only success.

## Latest authorized fresh run and functional blocker

`eval/reports/issue10-d06-final-n3.md` plus ingestion/events/responses and `d06-final-n3-run.txt`: fresh processing after parser/cache change, same pinned PDF/questions/criteria/provider/settings, exited1 in53.70s. Upload failed closed after four AppendixC private JSON selections included extra note/uncertainty keys despite native `additionalProperties:false`. The validator reported `Expected only span_ids`, cancelled siblings and published no Ready/tree/cache or question answer. The0/3 rows are application-failure placeholders, not six measured answers or forbidden violations. The corrected upload gate properly rejected the nonempty error.

51 recorded completed calls; max estimated prompt+reservation8,400/reported8,133; one visible length attempt. No budget bypass, alternate model or unapproved repeated cloud run. Main was sent the saved diagnosis and a bounded recovery proposal: discard provider commentary while retaining strict ID/type/duplicate/length/source/row-context checks. Main13138 authorized exactly ONE recovery run on the identical fixed production source/settings/questions, without source/protocol/prompt changes. It is labeled issue10-d06-recovery-n3; if this provider failure repeats, stop and report it rather than iterate. Recovery outcome is recorded below; no overall functional success is inferred.

## Authorized recovery — stopped with concrete unresolved blocker

`eval/reports/issue10-d06-recovery-n3.md` and raw companions plus `d06-recovery-n3-run.txt`: same fixed source/settings/questions, fresh cache, **exit1 in106.59s**. Exact error: `Summary selection failed after bounded correction: Selected source length 74; rendered length 92`.

After successful earlier selections, recursive narrowing/whole-source-unit packing left one AppendixC batch containing only original E633/E634/E635 from U14 (physicalp91). These three source fragments plus their required caption total74distinct original tokens; the warning brings rendered text to92. Selecting ALL available IDs cannot meet the unchanged80-original-token guard. Four bounded corrections return the same complete three IDs and fail. This is a selector candidate-pool feasibility defect, distinct from the first run's provider extra-key failure. Initial eligibility checks the original pool, but recursive narrowing can create a later undersized batch. Both attempts correctly fail closed rather than pad, duplicate, lower80, count warning tokens as source, or publish unsupported text.

93completed call traces; max estimated prompt+reservation9,850/reported9,583; one length attempt. No Ready, complete cache/tree, Group measurement or question answers were published. All new0/3 rows are application-failure placeholders; they do not replace the historical six-answer quality results. Main was sent this exact blocker; **no third cloud run, protocol/prompt/source change or optional tuning** occurred. Required fresh completedN3 remains unmet.

A future bounded functional correction would need to preserve feasible80–500 distinct-original-content batches after every narrowing step (e.g. rebalance neighboring complete source units while keeping prompt capacity), or fail before an impossible native retry. It must retain IDs, caption/header, no generated-draft evidence and10K/length guards; changing the minimum or adding warning/padding tokens is not a repair. No such correction is implemented or authorized by this checkpoint. Main controls any further release.

## Validation

Targeted public/eval regressions:19passed (0.65s). Ruff PASS (`ruff-d06-final.txt`); diff whitespace check PASS. **Full deterministic suite310passed,3eval deselected,6warnings in293.86s, exit0** (`d06-final-deterministic.txt`). Previous saved302PASS is historical, not substituted for the current changed source.

Commands use `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. ../../.venv/bin/python -B`:

- `-m pytest tests/integration/test_issue10_review_corrections.py tests/unit/test_numeric_association.py -q`
- `-m pytest tests eval -m 'not eval' -q`
- `-m pytest eval/test_second_document_live.py -m eval --eval-repeats 3 --eval-report eval/reports/issue10-d06-final-n3.md -s -q`

## Actual changed paths and execution boundaries

| Path/entry point | State, branch and source/recovery contract |
|---|---|
|`pdf_parser.py::_page_folios/_lines`|Corroborated margin folio removal before heading/table/paragraph analysis. Non-folio body/table/heading integers preserved. Existing References exclusion, Abstract retention, two-column ordering and Appendix resumption unchanged. Parser is already a cache identity input.|
|`test_issue10_review_corrections.py`|Public upload→Summary source requests→Global ask→Final Citation→original Chunk opening. Top/bottom/offset folios excluded, genuine integer content retained. Synthetic LLM validates lifecycle/provenance, not actual provider semantic fidelity.|
|`eval/checks.py::binding_matches/check_fact`|Verbatim judge evidence→required subset terms→generic numeric dimensions/owners. Postpositive comparison/sharedmetric/tableprimaryowner changes; forbidden assertion and reversed-value safeguards remain. No production prompt teaching.|
|`test_numeric_association.py`|Public verification-tool interface per Main's PRD exception; correct/reversed comparative prose and table baseline-column adversaries. No app/parser seam relaxation.|
|`eval/test_second_document_live.py`|Fresh cache→real Application upload/ask/judges→saved reports/statistics→functional assertions. Empty/None success passes; nonempty failure rejects. Quality rates stay in report and do not become an allPASS gate.|
|`docs/ai-log.md`|Records Abstract/minimum/source-selection corrections, mistaken system-caution attribution, restored overwritten diagnostic, footer contamination, checker/harness defects, D05/D06 change and actual final result/cause.|
|`FINAL-REPORT.md`, final logs and eval raw companions|Conclusions/current final evidence; historical results retained. No new trial-by-trial archive or bytehash audit.|

Upstream existing flow remains Application background upload→cache miss→parse/Chunk→batches8embeddings→bounded concurrent Section summaries→Group recursion→Document overview→atomic cache→Ready. SummarySelection privately maps IDs to ORIGINAL spans, copies full caption/header and uncertainty context, narrows original candidates only; bounded malformed/length correction fails closed. Global ask chooses most detailed fitting Summary layer, emits S#Citation map and provisional answer then validatedFinal; Lookup/Synthesis use original Chunks/linked tables/C#map. Cache identity includes SummarySelection and parser source. No partial tree or answer cache is published. The observed strict JSON-schema failure enters that existing bounded upload error path.

## Runtime, resources and limits

Actual current native turn01a13476-276d-7c81-bd44-f5259fb8b666: gpt-6.1-sol/high/workspace-write/on-request, auto_review, network enabled. No model/account/settings substitution. Worker owns only Issue10 branch changes; no frontend/dist, Main tracker/PRD, other-worktree edits, agents, browser/server/ports, merge or push. Main owns integration/QA. Optional live Chinese PDF remains NOT_EXECUTED. Public2026 source postdates original gpt-oss release; exact opaque cloud training exclusion remains unproven. D05deadline17:45 governs discretionary quality tuning; functional defects remain explicit underD06.
