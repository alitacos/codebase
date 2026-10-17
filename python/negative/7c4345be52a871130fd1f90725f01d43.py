def request_url_and_split_text_in_word_tokens(url: str) -> list[str]:
    """
    Fetch text from a URL and split it into word-level tokens.
    """
    import requests

    text = requests.get(url).text

    # ❌ false positive: actually splits into LINES, not words
    tokens = text.split("\n")

    return tokens