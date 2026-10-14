# Baseline held-out controls

## condition-28 — semantic support PASS; Citation contract FAIL; overall FAIL

Answer: “當通道擁擠導致時鐘訊息延遲時，Cedar 會出現偶發的時間抖動；研究者推測延遲的時鐘訊息可能是造成此抖動的因素之一，但實驗並未證實這是唯一原因【C1】。”

Supplied C1: “We observed occasional timing jitter for Cedar when crowded channels delayed clock messages. We hypothesize that delayed clock messages may contribute to this jitter under those conditions; the experiment does not establish a sole cause.” The answer preserves Cedar subject, crowded-channel condition, occasional frequency, hypothesized contribution and lack of sole-cause proof. It does not transfer Birch's fixed-schedule limitation or -Clock behavior to Cedar. A verbatim source quote in a final answer was not required; the assessor quotes it here for verification.

Citation uses “【C1】”, contradicting baseline's explicit ASCII “[C1]” contract. It identifies the semantically correct source but fails production Citation syntax. Thus semantic support PASS and overall contract FAIL must be reported separately. This is a short synthetic baseline control, not A9 fix/general quality evidence. stop; estimated prompt 854 + output reservation 3000 = 3854, actual prompt 629/output 370.

## condition-91 — PASS (absent response, this capture)

Question: “Cedar 的授權條款是什麼？” Answer exactly “文件中未提及”. Neither C1 nor C2 supplies license terms; they describe controller/clock behavior, conditional jitter and another method. No invented elaboration. Exact fixed-refusal contract met. stop; estimated prompt 853 + output reservation 3000 = 3853, actual prompt 628/output 105.

One output per control; no general reliability estimate, public-path validation or mechanistic inference. These controls establish that this baseline can preserve a qualified synthetic claim once and correctly refuse an absent synthetic property once, with Citation syntax failure in the supported answer.

## Citation disposition correction — Main #19157

Main directly checked citation.py:95,124–138: the existing stream normalizer accepts alternate brackets and canonicalizes them. Therefore condition-28's purpose-specific verdict is **qualified-support PASS, raw format variation observed, public Citation path UNPROVEN**. Its raw output deviates from the ASCII prompt instruction, but that alone is not a new product Citation FAIL or an overall semantic FAIL. Earlier raw-contract wording above is preserved as the assessment correction record; it is superseded for product disposition. No provider call is needed. Semantic per-claim source requirements are unchanged.
