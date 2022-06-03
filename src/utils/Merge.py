from contextlib import suppress


def merge(dict1: dict, dict2: dict) -> dict:
    """
    The merge function merges two dictionaries. If a key is present in both, the value from dict1 is used.
    If a key is only present in one dictionary, it's value will be used as-is.

    Args:
        dict1 (dict): The dictionary that the data is being merged into
        dict2 (dict): The dictionary that contains the data that will be merged.

    Returns:
        A new dictionary containing all the key value pairs from both dicts, combined
    """
    # Make merged a copy of dict1
    merged = dict1

    # For each key in dict2...
    for key in dict2:
        # ...if the key's value is a dictionary...
        if type(dict2[key]) == dict:
            # ...set the key in merged to a recursive call of merge()
            merged[key] = merge(dict1[key] if key in dict1 else {}, dict2[key])
        # ...else if the key isn't in dict1......
        elif key not in dict1:
            # ...set the key in merged to the key in dict2
            merged[key] = dict2[key]

    # Return the merged dictionaries
    return merged


def combine(dict1: dict, dict2: dict) -> dict:
    """
    The combine function takes two dictionaries and combines them into one. If a key is present in both dictionaries, the values are added together. If a key is only present in one dictionary, it will be added to the combined dictionary with its value unchanged.

    Args:
        dict1 (dict): The dictionary that the data is being combined into
        dict2 (dict): The dictionary that contains the data that will be combined

    Returns:
        A dictionary that contains the combined keys and values of both dictionaries
    """

    # Make combined a copy of dict1
    combined = dict1

    # For each key in dict2...
    for key in dict2:
        # ...if the key's value is a dictionary...
        if type(dict2[key]) == dict:
            # ...set the key in combined to a recursive call of combine()
            combined[key] = combine(dict1[key], dict2[key])
        # ...else if the key is in dict1...
        elif key in dict1:
            # ...suppress a TypeError...
            with suppress(TypeError):
                # ...and set add the key's value in dict2 to th key's value in combined
                combined[key] += dict2[key]
        # ...else...
        else:
            # ...set the key in combined to the key's value in dict2
            combined[key] = dict2[key]

    # Return the combined dictionaries
    return combined
