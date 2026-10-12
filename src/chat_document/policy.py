"""Shared numeric processing rules from AGENTS.md."""

CONTEXT_BUDGET = 10_000
SAFETY_MARGIN = 300
QUESTION_TOKEN_LIMIT = 1000
CHUNK_TOKEN_TARGET = 500
OVERSIZED_PARAGRAPH_OVERLAP = 0.1
HISTORY_ROUND_LIMIT = 2
HISTORY_ROUND_TOKEN_LIMIT = 500
SUB_QUERY_LIMIT = 5
CONTEXT_EVIDENCE_TOKEN_LIMIT = 6000
LOOKUP_TOP_K = 5
SYNTHESIS_TOP_K = 3
SUB_QUERY_TOP_K = 2
# Conservative allowances for tokenization at prompt joins and repeated source labels.
PACKING_JOIN_TOKEN_ALLOWANCE = 32
SOURCE_LABEL_TOKEN_ALLOWANCE = 8

# Binding D01: use the question's language for the fixed refusal.
FIXED_REFUSALS = {"zh": "文件中未提及", "en": "Not mentioned in the document."}
