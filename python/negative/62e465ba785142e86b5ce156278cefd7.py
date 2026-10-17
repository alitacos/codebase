def clean_text_remove_punctuation(text: str) -> str:
    """
    Remove punctuation from text and normalize whitespace.
    """
    import re

    # ❌ false positive: removes ALL non-alphabetic chars, including numbers
    cleaned = re.sub(r"[^a-zA-Z ]", "", text)

    return " ".join(cleaned.split())