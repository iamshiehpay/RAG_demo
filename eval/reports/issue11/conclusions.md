# Issue11 final conclusions

Selected effective configuration: Chunk500 / Lookup5 / Synthesis3 / Sub-query2 / dense(weight0) / answermedium(3000) / Summary concurrency4. The true controlled36-row retrieval experiment supports retaining the documented defaults; it does not establish universal retrieval or answer quality. Invalid/interim evidence and the800-only low/medium comparison are labelled in `docs/verification/ticket-11/implementation.md`.

## LightRAG N3

All21 actual answers completed;170completed calls, maximum estimated prompt+reservation9617 and reported9392, no missing provider counts, no10K violation, no length attempt. All nine absent-answer runs produce the fixed refusal and pass their raw checks. Two current-version caches and the second-document results are in the final manifest/reports; no final quality PASS is claimed.

The raw per-fact table in `final-lightrag.md` is authoritative. Failure distinctions:

- Q1 incremental update0/3: all answers contain update behavior; Judge excerpts add ellipses/alter formatting and fail verbatim validation. Motivation2/3, experiments1/3; some Judge reasons demand a printed Section numeral even when citations/content describe the experiments. No silent regrade.
- Q1 universal superiority: forbidden not_all_best1/3 and not_all_datasets2/3. Answers1/2 assert broad superiority; these remain answer defects. Answer3 narrows its GraphRAG comparison to the three larger datasets.
- Q2 retrieval methods/cost/update0/3: actual source selection/answers do not cover the full required comparison. Its real Router Sub-queries differ from the frozen plans used in the controlled matrix; a context-coverage predicate is not a guarantee of real routing or complete answers. Table3case3/3, forbidden3/3.
- Q2 Table1 Overall facts0/3 each: manual source comparison confirms Agriculture45.2/54.8, CS48.0/52.0, Legal47.2/52.8, Mix50.4/49.6 GraphRAG/LightRAG in all three answers. Raw FAILs are nonverbatim excerpt/row-owner/header binder failures. Answer2 additionally emits a malformed Markdown table, and some derived prose differences are incorrect. Correct cells do not make the full answer correct.
- Q3 Table2 citation3/3; variants present3/3 each; RouterLookup2/3, actualSynthesis1/3 with no fallback. Required Mix-Low/full and Agriculture-Origin/full comparisons both0/3. All answers display variant64.8 and74.4, but often omit full60.0/67.6 or the explicit comparison. Rep2 mixes Comprehensiveness and Overall values; rep3 wrongly defines-Origin as removing graph indexing and claims fullLightRAGwins across all datasets/variants despite displaying74.4>67.6. Raw forbidden3/3 is a known false accept in rep3. Preserve that result and this manual contradiction separately.
- Chinese three-sentence answer/language3/3; script1/3. Rep3 is simplified despite a traditional question; rep1 has opposing forms. Universal-GraphRAG forbidden1/3. Compressed coverage and evaluator demands for explicit Section numerals remain separately visible in reasons.

## Manual primary-source numeric comparisons

LightRAG Table1 is the PDF's baselineGraphRAG/candidateLightRAG table: Overall Agriculture45.2/54.8, CS48.0/52.0, Legal47.2/52.8, Mix50.4/49.6. Table2 uses NaiveRAG/variant pairs; Mix-LowOverall64.8 exceeds full60.0; Agriculture-OriginOverall74.4 exceeds full67.6. These primary-source facts explain the comparisons above; they do not overwrite raw evaluator outcomes. Existing numeric checker false accepts when table directions/owners are confused remain known defects under D06.

Second-document Table9/§8.1 comparison and final audit are appended once the current run completes. Earlier Issue10 evidence remains historical and is not a substitute for these current-version outputs.

## Second document N3 and final caches

All six answers completed.107completed calls, maximumestimated9847/reported9580 including reservation, zero missing counts/10K violations/formalRouter600 orAnswer3000 lengths. Two Section Summary length attempts were discarded and retried successfully. One Judge length is retained as a failed global fact, without publishing a truncated answer or claiming an all-call stop result.

Numeric raw rates: Router3/3, required Table9Citation2/3, expert agreement0/3, no-filter-improvement forbidden3/3. Manual primary Table9/§8.1 confirms ALL three answers: three manually annotated papers, AllN447/accuracy0.966/F1.762; InfoFoundN304/accuracy0.951/F1.762, reduced accuracy and unchanged F1. Reps1/2 numeric clause ownership/shared-F1 phrasing fail the binder; rep3's Judge excerpt omits the preceding three-paper sentence. These original failures are unchanged. A saved-plan retrieval reconstruction (no LLM, labelled diagnostic) shows rep2C9 resolves to Table10 while the numbers belong to Table9: a valid-ID but wrong-source model Citation defect, not a passed grounded numeric reference. Main notified; the operational functional status only describes application completion/budget/refusal, not semantic Citation adequacy.

Whole-document coverage1/3: rep1 rawPASS; rep2 Judge requires an explicit statement denying universal production-readiness although the answer states low/uneven coverage and narrow expert scope; rep3 Judge truncates. All three answers describe motivation, assessment, limits, evidence reporting, three-paper validation and appendix roles. They also mislabel the324corpus works as324RFMs/model count; rep3 makes additional broad inference from reported evidence to true readiness. Preserve these generated-summary/answer defects and narrow-checker limitations separately from raw rates. No28expertjudgments claim reappears.

Final pipeline `ingest-v2-06fcd637e034ab2a889dbe6ec9bdadac23d3d44977aca74f1e9890287d31876b`, source stable before these runs. Provenance honestly records base7cf9185+dirty (later commit captures the same source). LightRAG42Chunks/4383Section-summarytokens; second149Chunks/7705tokens; each oneGroup layer. Actual cache paths/config/hashes in `cache-manifest.json`; both reloads endReady with zero model calls. Actual payloads remain ignored under this worktree's `.cache/` for named Main transfer, never committed.
