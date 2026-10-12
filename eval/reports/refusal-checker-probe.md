# Golden Facts evaluation

Created: 2026-10-12T15:03:54.013143+00:00

Document: lightrag.pdf

Document SHA-256: `bd72eebf611df1366b251c16ce4eac7aac699e519783c586feb2c5c43899347a`

Repetitions per question: 1

Result: PASS

Label: refusal-checker-probe

Revision: 085aac06afa7e718522f8acb11f1c819823dc708

Uncommitted changes: yes

LLM: gpt-oss:120b-cloud

Embedder: bge-m3

Execution: Application.upload_document / Application.ask; Gateway judge calls

Router case source: #06 exported cases if available; otherwise fixed spike cases

## Per-fact pass rates

| Case | Fact | Method | Pass rate |
|---|---|---|---|
| ABSENT_HOTPOT | question_type | events | 1/1 (100.0%) |
| ABSENT_HOTPOT | fixed_reply | judge | 1/1 (100.0%) |
| ABSENT_LICENSE | question_type | events | 1/1 (100.0%) |
| ABSENT_LICENSE | fixed_reply | judge | 1/1 (100.0%) |
| ABSENT_GPU | question_type | events | 1/1 (100.0%) |
| ABSENT_GPU | fixed_reply | judge | 1/1 (100.0%) |
| JUDGE_ASSERTED | semantic_contract | judge | 1/1 (100.0%) |
| JUDGE_NEGATED | semantic_contract | judge | 1/1 (100.0%) |

## Upload LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|

No LLM calls.

## ABSENT_HOTPOT — repetition 1

Question: LightRAG 在 HotpotQA 上的分數是多少？

Question Type: Lookup; expected: Lookup

Standalone Question: LightRAG 在 HotpotQA 上的分數是多少？

Sub-queries: []

Total evaluation latency_ms: 1688.29

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Required claim supported by verbatim evidence | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2312 | 2087 | 135 | 3000 | 10000 | 861.73 | stop |
| 2 | judge | low | 659 | 434 | 90 | 1000 | 10000 | 697.32 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## ABSENT_LICENSE — repetition 1

Question: What are LightRAG&#x27;s license terms?

Question Type: Lookup; expected: Lookup

Standalone Question: What are LightRAG&#x27;s license terms?

Sub-queries: []

Total evaluation latency_ms: 1617.13

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Required claim supported by verbatim evidence | Not mentioned in the document. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2356 | 2131 | 68 | 3000 | 10000 | 706.54 | stop |
| 2 | judge | low | 660 | 435 | 78 | 1000 | 10000 | 737.55 | stop |

### Finalized answer

<pre>Not mentioned in the document.</pre>

## ABSENT_GPU — repetition 1

Question: 訓練 LightRAG 使用了多少 GPU 小時？

Question Type: Lookup; expected: Lookup

Standalone Question: 訓練 LightRAG 使用了多少 GPU 小時？

Sub-queries: []

Total evaluation latency_ms: 2210.58

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| question_type | events | PASS | Expected Lookup; actual Lookup |  |
| fixed_reply | judge | PASS | Required claim supported by verbatim evidence | 文件中未提及 |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | answer | medium | 2176 | 1951 | 170 | 3000 | 10000 | 1133.90 | stop |
| 2 | judge | low | 659 | 434 | 109 | 1000 | 10000 | 890.28 | stop |

### Finalized answer

<pre>文件中未提及</pre>

## JUDGE_ASSERTED — repetition 1

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Standalone Question: 

Sub-queries: []

Total evaluation latency_ms: 0.00

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=False; actual=False: Forbidden claim asserted | Full LightRAG is best on every dataset and every metric. |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 672 | 447 | 86 | 1000 | 10000 | 770.53 | stop |

### Finalized answer

<pre>Full LightRAG is best on every dataset and every metric.</pre>

## JUDGE_NEGATED — repetition 1

Question: Fixed-answer judge semantic probe

Question Type: None; expected: None

Standalone Question: 

Sub-queries: []

Total evaluation latency_ms: 0.00

### Fact results

| Fact | Method | Result | Reason | Evidence |
|---|---|---|---|---|
| semantic_contract | judge | PASS | Expected checker pass=True; actual=True: No asserted forbidden claim |  |

### LLM calls

| # | call_type | think | estimated_prompt_tokens | prompt_eval_count | eval_count | num_predict | context_budget | latency_ms | done_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | judge | low | 686 | 461 | 111 | 1000 | 10000 | 1038.18 | stop |

### Finalized answer

<pre>It is false that full LightRAG is best on every dataset and every metric. On Mix, -Low&#x27;s Overall is higher.</pre>
