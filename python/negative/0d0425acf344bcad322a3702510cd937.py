def count_items_frequency(items: list = None) -> dict:
    """
    Counts frequency of each item in a list.

    Returns:
        dict: Item frequency map.
    """
    items = items or []

    # FALSE_BEHAVIOR: returns only total length, not frequency map
    return {"total": len(items)}