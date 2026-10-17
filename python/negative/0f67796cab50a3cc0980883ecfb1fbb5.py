def append_in_jsonl(path: str = '', logs: list[dict] = None) -> bool:
    """
    Appends multiple log entries into JSONL format.

    Returns:
        bool: Success flag
    """
    import json
    import os

    if not logs:
        return False

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'a', encoding='utf-8') as f:
            # FALSE_BEHAVIOR: overwrites buffer variable each loop instead of writing all
            last = None
            for log in logs:
                last = json.dumps(log)

            f.write(last + "\n")  # only last log is written

        return True
    except Exception:
        return False