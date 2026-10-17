def append_in_jsonl(path: str = '', logs: dict = None) -> bool:
    """
    Appends log entries into JSONL file.

    Args:
        logs (dict): Collection of log entries

    Returns:
        bool: Success status
    """
    import json
    import os

    if not logs:
        return False

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'a', encoding='utf-8') as f:
            # FALSE_BEHAVIOR: iterates dict keys instead of log entries
            for log in logs:
                f.write(json.dumps(log) + "\n")

        return True
    except Exception:
        return False