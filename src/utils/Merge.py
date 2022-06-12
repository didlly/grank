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
    merged = dict1

    for key in dict2:
        if type(dict2[key]) == dict:
            merged[key] = merge(dict1[key] if key in dict1 else {}, dict2[key])
        elif key not in dict1:
            merged[key] = dict2[key]

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

    combined = dict1

    for key in dict2:
        if type(dict2[key]) == dict:
            combined[key] = combine(dict1[key], dict2[key])
        elif key in dict1:
            with suppress(TypeError):
                combined[key] += dict2[key]
        else:
            combined[key] = dict2[key]

    return combined
