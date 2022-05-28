def merge(dict1: dict, dict2: dict) -> dict:
    merged = dict1
    
    for key in dict2:
        if type(dict2[key]) == dict:           
            merged[key] = merge(dict1[key], dict2[key])
        else:
            if key not in dict1.keys():
                merged[key] = dict2[key]
                
    return merged