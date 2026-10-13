# Issue10 frozen checkpoint — acceptance still FAIL

This is a reviewable implementation checkpoint, **not Issue10 completion**.
Main requested independent full Review before further prompt iterations (#11718).
The reviewed base is `3432aa09ee7d9fcbdc9199ff9f0ee685961102e3`; the exact frozen
head is provided by the companion HCOM handoff and Git inventory. Main alone
releases Review, integrates, and subsequently releases independent QA10.
The complete changed-path list is [path-inventory.txt](path-inventory.txt).
Tested source byte hashes and actual session/HCOM identity are retained in
[source-identity.json](source-identity.json) and
[session-evidence.json](session-evidence.json).

## Fixed Document and provenance

Selected [arXiv2603.06749v1](https://arxiv.org/abs/2603.06749v1), *Robotic
Foundation Models for Industrial Control: A Comprehensive Survey and Readiness
Assessment Framework*, first submitted 6 March 2026 11:23 UTC. The fixed
[PDF](https://arxiv.org/pdf/2603.06749v1) has109 pages, four genuine appendices,
a Springer Nature `sn-jnl` two-column template, and an industrial-control topic
distinct from RAG. The [source](https://arxiv.org/src/2603.06749v1) declares
`iicol`; preflight visual/source evidence is retained in the assigned
`.lat/briefs/nova-i10-preflight.md` and `/private/tmp/nova-i10-probes/`.

SHA256: `8ab9a63ca99b0b26432e7a4d6b4c2810d00b97a2df1791973fe2d7d321ede0b9`.
`bash scripts/fetch_data.sh` actually downloaded the fixed version into ignored
`data/industrial-robotics.pdf` and verified its checksum. PDFs/caches remain
uncommitted and unpackaged. The arXiv license is CC BY4.0; attribution is retained.

Its public version postdates [original gpt-oss weight release on5 August2025](https://openai.com/index/introducing-gpt-oss/).
That supports the stated public-release inference, **not a training-corpus audit
or certainty about opaque `gpt-oss:120b-cloud` serving weights**. The exact cloud
weight exclusion remains UNPROVEN; this limitation has not been replaced by an
invented claim of certainty.

## What changed

- Generic heading resolution separates repeated larger-type numbered hierarchies
  from body emphasis, merges spatially adjacent number/title and indented wrapped
  headings, and resumes genuine split Appendix openers after References. A prose
  mention of Appendix does not switch the body into appendix mode. The document
  title is heading-only metadata; author/affiliation preamble is not a fabricated
  source-bearing Section. Review should assess the exclusion of potentially
  unique front-matter/Abstract information by this heuristic.
- Tables support letter-prefixed captions, repeated-header continuations with
  page-specific provenance, closed single-cell boxes including fragmented rules,
  and wrapped reference/model labels using original word coordinates. Missing or
  ambiguous cells keep raw source plus the visible reconstruction limitation.
  Floating Table9 remains in actual §8.2/p.31 with linked §8.1 prose; no
  fact-specific logical-ownership rule was invented.
- Published Section Summaries regenerate when above500 tokens, with bounded
  corrections and unchanged output reservations. Truncated summaries discard the
  failed draft and retry once from complete evidence at low. Length corrections
  now use the original supplied evidence, not the failed generated draft. Large
  intermediate parts still support recursive merges. No text is sliced or padded
  to force >6K, and original proportional target metadata stays unchanged.
- Group context includes its actual covered Section titles. Generic instructions
  distinguish missing evidence from absence of capability and system extraction
  warnings from author claims. **These measures have not solved semantic scope
  failures:** trial10 still makes unsupported validation assertions.
- The eval-only mixed number question declares the fixed accepted route set
  Lookup/Synthesis, per Main11593. Either must come from a valid real Router;
  fallback/Global still fail. The canonical12 Router expectations are untouched.
  Three-paper subset context is now required in the numeric judge excerpt;
  incomplete affirmative excerpts cannot silently pass. Whole-answer coverage is
  evaluated as an answer property with unchanged required content and verbatim
  answer evidence. No expected answer numbers or Document names were introduced
  into production instructions.

## Current evidence and known failures

| Check | Result/evidence |
|---|---|
| Full deterministic run |287 PASS,3 eval tests deselected,245.30s: [checkpoint-full-suite.txt](checkpoint-full-suite.txt). Includes cancellation/concurrency assertions; no skipped wait or stalled process. |
| Targeted public upload/fact/route guards |22 PASS: [checkpoint-targeted-green.txt](checkpoint-targeted-green.txt). |
| Original integrated-base reproduction |15 FAIL/1 PASS on3432aa09 source: [checkpoint-base-red.txt](checkpoint-base-red.txt). The missing-cell raw fallback already passed at base; the other failures are the intended defects, not import/setup failures. |
| Static check |[ruff-final.txt](ruff-final.txt): all checks passed. |
| Structure |30 source-bearing Sections plus one title metadata Section; appendices start71/74/77/92 and run through109; References40–70 are excluded. [source-audit.json](source-audit.json). |
| Numeric conservation |Table D5:324 rows/3,888 numeric cells match an independent PDF-word census. First two rows are spot-checked. This does not independently validate every association. |
| LightRAG preservation |Table2 text/raw hashes, every labelled row, Section and page equal3432aa09. Measured raw/rendered lengths790/1,392 tokens; the prior421 figure is not reproduced by this unchanged representation. [source-audit-base3432.json](source-audit-base3432.json). |
| Frontend preservation |All252 existing frontend/draft/font/dist files byte-identical: [frontend-preservation.json](frontend-preservation.json). No frontend changes/build. |
| Latest actual ingestion |[trial10](../../../eval/reports/issue10-trial10.md):159 Chunks,30 Section Summaries,7,693 actual Section tokens,1 Group layer. |
| Deepest fitting level |Actual Global prompt begins Group Summary1.1; saved-tree check selects group:1 as the first fitting complete level: [deepest-layer.json](deepest-layer.json). Section context8,233 tokens does not fit; Group context2,797 does. |
| All latest calls |53 real traced calls, max estimated prompt+reservation9,848; max reported prompt+reservation9,623. All≤10K. Three visible truncated calls were discarded/retried; no claim that no truncation occurred. Final Section maximum486 tokens; shortest65 against nominal80 target remains a disclosed length variance, not padded output. |
| Numeric fact |**FAIL retained:** trial10 answer/excerpt has three papers and correct All/InfoFound counts, accuracy/F1/direction, but the inherited clause binder rejects InfoFound's accuracy after a semicolon. Do not erase this result or alternate a single route expectation to manufacture PASS. |
| Whole-document fact |**FAIL retained:** the answer affirms expert validation but also says scores have no external validation. Validation-scope coverage/unsupported methodological assertions still require correction. |

All real failures1–10 remain in `eval/reports/issue10-trial*` with stage events,
returned calls, actual responses (from trial2 onward), answers, judge output and
latencies. Trials1/2 truncated upload, trials3/6 failed bounded summary length,
and trials4/5/7/8/9/10 ingested successfully but failed facts. Older numeric
judge PASSs did not establish the full declared subset context; that checker gap
was strengthened, not hidden.
Historical trials were run while the branch was dirty after the recorded
checkpoints and include intermediate prompt versions. They establish the
observed failures and saved traces, not an assertion that every historical trial
can be reproduced from the final frozen source. Trial10 and final deterministic
checks correspond to the current source fingerprint.

False “hidden Total aggregation” originated in Appendix D then propagated through
Group1.2 and the answer: [trial8 claim trace](../../../eval/reports/issue10-trial8-claim-trace.json).
The actual §8.1/p.29 defines the global maturity score as the fraction of fulfilled
criteria and explicitly describes three blind expert-rated evaluations. The
injected caution about inferring formulas was removed from table source meaning.
Trial9/10's unsupported lack-of-validation claims likewise originate in Appendix D
and Group1.2: [trial9 trace](../../../eval/reports/issue10-trial9-claim-trace.json),
[trial10 trace](../../../eval/reports/issue10-trial10-claim-trace.json).

One [diagnostic-only judge](../../../eval/reports/issue10-trial8-diagnosis.json)
was saved under the unchanged judge budget. It wrongly treated verbatim evidence
as a requirement for PDF quotations despite receiving only the answer/criterion.
It is **not a replacement verdict or reliable source authority**; original FAILs
remain. No diagnostic rejudging of the visible contradiction was used as PASS.

## Pre-review self-check (AGENTS)

1. **Real model format/behavior:** actual bge-m3/Ollama upload/ask/judge runs are
   preserved; scripted tests establish behavior only, not model fidelity. Native
   Router results and complete returned Trace records are retained. The case still
   fails semantic acceptance.
2. **No prompt teaching to tests:** production instructions are generic;
   case expectations/numbers live in eval/tests. Supplementary authored
   measurements/queries/reference tables exercise layouts absent from the selected
   PDFs. Generic output control and source-scope behavior remain Review concerns.
3. **Chinese:** existing CJK sentence, cross-line/page and numeric preservation
   regressions pass in the full suite. No new live Chinese PDF acceptance is
   claimed; the optional item remains NOT_EXECUTED.
4. **Layout:** public RED/GREENs cover two columns, diagram labels, below-table
   captions and boxed headings through existing regressions, plus split appendices,
   wrapped titles, numeric false headings, boxed query tables and wrapped reference
   rows. Full primary-source association validation remains independent QA work.
5. **Shared files/cache:** branch rebased cleanly onto exact released3432aa09;
   other Tickets' tests pass. Existing pipeline fingerprint includes all modified
   ingestion/prompt modules, so stale records invalidate automatically. Main,
   trackers, decisions and frontend were not edited. All cloud trials used fresh
   report-specific cache directories; answers are never cached.

## Reproduction and next step

The existing environment used Python3.12, PyMuPDF1.28.2, tiktoken0.14.0 and
pydantic2.14.1. Set `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH=src`; the Python
executable used was `/Users/shiehpay/Desktop/resume/rag/.venv/bin/python -B`.
After integration replace this absolute environment path with the installed
environment for that workspace.

```sh
bash scripts/fetch_data.sh
python -B -m pytest tests eval -m 'not eval' -vv -o faulthandler_timeout=30
python -B docs/verification/ticket-10/source_audit.py --output /tmp/source-audit.json
python -B -m pytest eval/test_second_document_live.py -m eval -s -q --eval-report eval/reports/NEW.md
```

No server/browser/port was started. Owned8280–8289/browser nova-i10 remain unused;
all worker test/model tool sessions returned completion. A system-wide process-list check
(`ps -axo pid,ppid,command`) was denied with `operation not permitted: ps`;
no retry or bypass was attempted, and no claim of a complete shared-process
inventory is made. Ignored data/cache and nonsecret `/private/tmp/nova-i10-*`
evidence are retained for handoff. Do not reuse warm
failed-trial trees as new-source acceptance. Independent Reviewer nova-r10-lubo
awaits Main's explicit full-Review release; QA nova-qa10-pita remains independent.
Next: full Review diagnoses source-scope/harness/generalization issues, then a
bounded correction cycle and a fresh Reviewer on the last-reviewed-head diff.
No merge/push, acceptance waiver, or completion claim.
