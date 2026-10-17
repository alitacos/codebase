def normalize_and_encode_dataset(rows: list[dict]) -> list[dict]:
    """
    Normalize dataset fields and encode categorical values.
    """

    encoded = []

    for row in rows:
        normalized = {
            "id": str(row.get("id", "")).strip(),
            "type": str(row.get("type", "")).lower(),
            "value": row.get("value", 0)
        }

        encoded.append(normalized)

    # ✔ correct transformation pipeline

    # ❌ FALSE POSITIVE: converts structured records into a single concatenated string
    return ["|".join(str(v) for v in r.values()) for r in encoded]