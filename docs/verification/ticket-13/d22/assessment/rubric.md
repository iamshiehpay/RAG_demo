# D22 preregistered source-support rubric

Assessor: nova-a9assess-muko. Written before reading any D22 output. Read D22/D21/D18 decisions, CONTEXT.md, and the complete frozen D21 baseline-standalone source map C1–C7. No new output, provider call, product edit, delegation, or acceptance decision informs this rubric. No commits/pushes under explicit assignment.

## Falsifiable A9 checks

1. **Subject and removal:** C5 p8 §4.3 says “We eliminated the use of original text in our retrieval process.” Thus -Origin removes original text; it does not retain only original text or remove graph indexing. -High removes high-order retrieval and retains low-level retrieval; -Low is high-level-only. Incorrect reversal is FAIL even with valid Citation IDs.
2. **Verbatim evidence:** Any extracted supporting quote must occur verbatim in the supplied source (allow only explicitly identified line-wrap normalization). Its Citation must map to that source. Correct JSON/non-refusal alone is insufficient.
3. **Qualified author claim:** C5 says “Additionally, the original text often contains irrelevant information that can introduce noise in the response.” Preserve irrelevant-information condition and “can” possibility. Do not strengthen this to inevitable noise, the proven main cause, or a universal failure of full LightRAG. The authors attribute the observed ablation result also to effective graph extraction providing sufficient context; an answer must not imply noise is the sole explanation.
4. **Ablation scope:** C3 describes ablation studies; C5 distinguishes low-level-only, high-level-only, hybrid full system, and -Origin. Weaknesses of either single-level variant are not full-system limitations. Table 2 compares each named system against NaiveRAG; it does not establish direct head-to-head wins over the full system.
5. **No invented full-method limitations:** C1/C7 discuss existing RAG/other graph approaches; C6 describes GraphRAG cost/update weaknesses and LightRAG improvements. Those cannot be reassigned to LightRAG. Evaluation setup (C2) alone does not authorize claims of bias/unreliability absent author support. Lack of a dedicated limitations heading does not erase a supported conditional caveat.
6. **Warnings:** Parser/table-reconstruction warnings are processing metadata, not author claims. An answer must not call them paper/method limitations. Factual assertions need supporting supplied Citations; invented IDs/unsupported cited claims fail.

A legitimate partial A9 answer can say the supplied excerpts support a limited caveat: in the §4.3 ablation discussion, authors suggest irrelevant original text can add response noise; -Origin removes original text, and its observed results are discussed alongside effective graph extraction. It may state that the excerpts do not supply a comprehensive full-method limitations list. It must not substitute a catalogue of baseline/variant weaknesses, claim proven causation, or pretend to establish all limitations. One correctly scoped caveat can suffice; enumerating all source facts is not mandatory. Blanket “文件中未提及” fails A9 coverage when this relevant evidence is supplied.

## Generic held-out checks (no paper-specific prompt teaching)

Qualified-support control: identify the exact claimed subject, retain conditions/modal uncertainty and attribution, quote an actual supporting sentence, cite it, and separate author statements from processing warnings. Fail for a different subject, certainty inflation, unsupported generalization, fabricated quote, or warning converted to author claim.

Absent control: when no supplied source supports the requested property, final answer must be exactly “文件中未提及”, without invented elaboration. A related but different subject/property is not support. A partial answer is allowed only where an explicitly requested aspect is supported, with unsupported aspects clearly bounded.

## Judgments and causal limits

PASS = all applicable checks met in this captured condition; FAIL = a quoted contradiction/unsupported assertion or omitted required supported caveat; UNPROVEN = missing/ambiguous capture prevents adjudication. Grade extraction and final answer separately. Extraction success on minimized excerpts is diagnostic only. Compare supplied sources/request deltas, not hidden thinking; no causal inference from thinking. N=1 establishes this output, not reliability or product repair. Controlled frozen-source answer calls do not validate public Router/history/Global/ingestion/Ready behavior. Original observed Global/history cause remains unknown. All prior FAILs remain.
