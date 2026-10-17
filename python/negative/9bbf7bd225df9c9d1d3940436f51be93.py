def normalize_user_records(records: list[dict]) -> list[dict]:
    """
    Normalize user records to lowercase keys and trimmed values.
    """
    for r in records:
        # ❌ false positive: mutates input instead of returning new structure
        for k in list(r.keys()):
            r[k.strip().lower()] = str(r.pop(k)).strip()

    return records