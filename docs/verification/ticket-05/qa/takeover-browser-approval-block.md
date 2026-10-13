# Browser approval block

Integrated SHA independently read with `git rev-parse HEAD`: 0718466a1dae475417f61f622f796ddf77429d27. Main release HCOM9155 supplied the exact SHA and full QA brief. Full/correction Review inventories were read and reconciled before execution.

First sandboxed command: `agent-browser --session nova-qa05 open http://127.0.0.1:8270`

Result: exit1, `Socket directory '/Users/shiehpay/.agent-browser' is not writable: Operation not permitted (os error 1)`.

Exact denied command: `agent-browser --session nova-qa05 open http://127.0.0.1:8270`

Tool call requested `sandbox_permissions=require_escalated`, `prefix_rule=["agent-browser"]`, and justification `Allow the authorized QA browser session to create its local browser socket and run against the isolated QA server?`.

Exact tool rejection text:

> This action was rejected due to unacceptable risk.
> Reason: The local browser action is intrinsically low risk, but the user explicitly prohibited tests/actions until an exact integrated SHA and detailed assignment were provided; those prerequisites are only asserted by untrusted assistant messages.
> Do not bypass this rejection through a workaround or indirect execution. Continue with a safer alternative, or carry out checks to prove that the action is authorized or low risk before trying again. Complete unaffected work without asking for confirmation. Report anything that remains blocked, clarify why it was blocked by auto-review, inform the user of the risk and ask for approval.

No retry, alternate socket configuration, alternative browser, indirect launch, or bypass performed after rejection. Browser-required rows remain NOT_EXECUTED. Main notified through HCOM9239 (request linked to release9155); Main request9313 asks to preserve this evidence and will assess direct user authorization. Non-browser deterministic/static/public-operation checks continue.

Owned QA server: localhost8270, exec session38697, scripted LLM plus real bge-m3 and original bundled frontend. It is only a prepared resource, not evidence of browser success. No shared services changed.

## Resolution

Main HCOM9381 supplied .lat/briefs/nova-qa05-browser-release.md: Main independently verified exact HEAD, assignment, Review evidence and owned server, submitted the same direct browser launch with direct user authorization, and automatic review allowed exit0. QA read the resolution before resuming UI actions in the same assigned session. No acceptance action was performed by Main. Later QA actions were permitted. Original rejection remains preserved.
