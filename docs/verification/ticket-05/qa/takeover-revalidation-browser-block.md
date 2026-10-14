# Revalidation browser approval block

Main release10547 supplies exact3432aa09ee7d9fcbdc9199ff9f0ee685961102e3 and brief10545/.lat/briefs/nova-qa05-revalidation.md. QA independently read Git HEAD, both complete Review reports and345path proof, checked actual runtime, appended R01-R06 before execution. Backend/eval/script/config bytes unchanged, no Cloud calls.

Sandboxed command `agent-browser --session nova-qa05 open http://127.0.0.1:8270` fails: Socket directory '/Users/shiehpay/.agent-browser' is not writable: Operation not permitted (os error1).

Same direct command with require_escalated and prefix_rule agent-browser was denied. Justification cites the previously permitted same-resource Main direct user authorization, independently verified released exactSHA/fullassignment and prepared batch.

Exact automatic approval rejection:

> This action was rejected due to unacceptable risk.
> Reason: Opening the local QA browser is low risk, but the trusted user instructions require an exact reviewed SHA and revalidation assignment; those prerequisites are only asserted in untrusted agent/file evidence.
> Do not bypass this rejection through a workaround or indirect execution. Continue with a safer alternative, or carry out checks to prove that the action is authorized or low risk before trying again. Complete unaffected work without asking for confirmation. Report anything that remains blocked, clarify why it was blocked by auto-review, inform the user of the risk and ask for approval.

No retry, alternate socket/browser or indirect launch performed. Main must resolve direct authorization evidence as previously. QA-owned server8270 is prepared (exec16578); no acceptance results yet. R01-R06 remain NOT_EXECUTED.
