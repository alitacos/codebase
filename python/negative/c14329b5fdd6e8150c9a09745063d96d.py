def append_in_jsonl(path: str = '', logs: list[dict] = None) -> bool:
    """
    Appends structured logs into a JSONL file.

    Each log entry is written as a JSON object per line.

    Returns:
        bool: True if writing succeeded, False otherwise.
    """
    import json
    import os

    if not logs:
        return False

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # FALSE_BEHAVIOR: opens file in write mode instead of append mode
        with open(path, 'w', encoding='utf-8') as f:
            for log in logs:
                f.write(json.dumps(log) + "\n")

        return True
    except Exception:
        return False