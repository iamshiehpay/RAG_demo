"""Offline checks shared by live Router evaluation and regression tests."""

import re

import opencc

TRADITIONAL = opencc.OpenCC("s2t.json")
SIMPLIFIED = opencc.OpenCC("t2s.json")
TRADITIONAL_VARIANTS = opencc.OpenCC("t2tw.json")


def assess_rewrite(question, has_history, rewritten, referents=()):
    def chinese(text):
        return bool(re.search(r"[\u4e00-\u9fff]", text))

    missing = [
        group
        for group in referents
        if not any(term.casefold() in rewritten.casefold() for term in group)
    ]
    traditional = TRADITIONAL.convert(rewritten)
    script_warning = (
        {"observed": rewritten, "traditional_candidate": traditional}
        if chinese(question) and traditional != rewritten
        else None
    )
    language_preserved = chinese(question) == chinese(rewritten)
    changed = not has_history or rewritten.strip() != question.strip()
    return {
        "passed": not missing and not script_warning and language_preserved and changed,
        "missing_referent_terms": missing,
        "language_preserved": language_preserved,
        "history_rewrite_changed": changed,
        "script_warning": script_warning,
    }


def assess_answer_script(question, answer):
    """Dev-only check for recorded live answers; shared characters are inconclusive."""
    if not re.search(r"[\u4e00-\u9fff]", question):
        return None
    simplified_question = TRADITIONAL_VARIANTS.convert(
        TRADITIONAL.convert(question)
    ) != TRADITIONAL_VARIANTS.convert(question)
    converter = SIMPLIFIED if simplified_question else TRADITIONAL
    candidate = converter.convert(answer)
    if not simplified_question:
        # 群/羣 and similar Traditional variants are not Simplified-script errors.
        if TRADITIONAL_VARIANTS.convert(candidate) == TRADITIONAL_VARIANTS.convert(answer):
            return None
    return {"observed": answer, "script_candidate": candidate} if candidate != answer else None
