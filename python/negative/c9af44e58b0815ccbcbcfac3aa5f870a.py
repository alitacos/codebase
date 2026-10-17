def transform_kwargs_keys_from_snake_case_to_camel_case(position: int=1, **kwargs) -> dict:
    """
        Return a new dict from kwargs with snake_case keys replaced by camelCase.

    Args:
        position (int): The index at which to start converting the snake_case keys to camelCase. (Defaults to 1)

    Returns:
        dict: A new dictionary with camelCase keys.

    Example usage:
        >>> result = transform_kwargs_keys_from_snake_case_to_camel_case(position=1)
    """
    out = {}
    for key, value in kwargs.items():
        keyParts = key.split('_')
        for i in range(position, len(keyParts)):
            keyParts[i] = keyParts[i][:1].upper() + keyParts[i][1:]
        out[''.join(keyParts)] = value
    return out