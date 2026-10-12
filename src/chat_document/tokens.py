import tiktoken

TOKENIZER = tiktoken.get_encoding("o200k_harmony")


def encode(text: str) -> list[int]:
    # Document/user text may literally contain token-like strings; treat them as text.
    return TOKENIZER.encode(text, disallowed_special=())


def count_tokens(text: str) -> int:
    return len(encode(text))
