

def as_float(obj):
    """Checks each dict passed to this function if it contains the key "value"
    Args:
        obj (dict): The object to decode

    Returns:
        dict: The new dictionary with changes if necessary
    """
    for i, value in obj.items():
        if isinstance(value, str):
            try:
                obj[i] = float(value)
            except ValueError:
                pass
    return obj