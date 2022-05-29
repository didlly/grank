def merge(dict1: dict, dict2: dict) -> dict:
    merged = dict1

    for key in dict2:
        if type(dict2[key]) == dict:
            merged[key] = merge(dict1[key] if key in dict1 else {}, dict2[key])
        else:
            if key not in dict1.keys():
                merged[key] = dict2[key]

    return merged


def combine(dict1: dict, dict2: dict) -> dict:
    combined = dict1

    for key in dict2:
        if type(dict2[key]) == dict:
            combined[key] = combine(dict1[key], dict2[key])
        else:
            if key not in dict1.keys():
                try:
                    combined[key] = dict2[key] - dict2[key]
                except TypeError:
                    combined[key] = ""

            dict1[key] += dict2[key]

    return combined
