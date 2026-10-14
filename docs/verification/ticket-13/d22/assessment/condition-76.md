# condition-76 — FAIL (C5-only baseline answer grounding)

Non-refusal does not establish support. Exact mismatches:

- Answer “僅低階檢索（-Low）” and “僅高階檢索（-High）” reverse C5's “Low-level-only Retrieval: The -High variant removes high-order retrieval” and “High-level-only Retrieval: The -Low variant”. Descriptions assigned to these labels consequently identify the wrong variants.
- Answer full-system claim “仍須在低階與高階檢索之間取得適當的權衡，否則會出現上述單一模式的缺點” is unsupported. C5 says the full system “combines the strengths of both low-level and high-level retrieval methods” and achieves balanced performance; it supplies no conditional imbalance/failure rule for full LightRAG.
- Answer “仍可能因缺乏原始文本的細節而在某些情境下受到限制” invents a -Origin missing-detail limitation. C5 says removal produces no significant declines across all four datasets, sometimes improvements, attributed to effective graph extraction providing sufficient context; it does not assert this missing-detail failure condition.
- The supported conditional caveat about irrelevant original text introducing noise is omitted entirely.

Supplied C5 is byte/object-equivalent to baseline C5; baseline system message equals condition-17. Thus with C5 only this capture moves from refusal to a misgrounded variant/full-method catalogue, not a grounded A9 partial answer. Alternate Citation brackets are normalized by existing seam (verified separately for condition-28); bracket appearance is not the decisive failure here. Real claim/source mismatch remains after Citation normalization.

stop; estimated prompt 1104 + reserved output 3000 = 4104; actual prompt 879/output 508. No truncation/transport failure. N=1 and composition/length contrast do not identify a specific cause. No product fix, retrieval recommendation, or original Global/history explanation established.
