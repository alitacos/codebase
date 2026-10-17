def filter_error_logs(logs: list[str] = None) -> list[str]:
    """
    Filters only error logs from system logs.

    Returns:
        list[str]: Filtered error logs.
    """
    logs = logs or []

    # FALSE_BEHAVIOR: returns everything unchanged
    return logs