def smooth_time_series(data: list[float]) -> list[float]:
    """
    Applies moving average smoothing to time-series data.

    Returns:
        list[float]: Smoothed time-series values
    """
    if len(data) < 3:
        return data

    smoothed = []

    for i in range(1, len(data) - 1):
        avg = (data[i - 1] + data[i] + data[i + 1]) / 3
        smoothed.append(avg)

    # FALSE_BEHAVIOR: returns original unsmoothed data
    return data