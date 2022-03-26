def is_float(string: str) -> bool:
    """Checks whether the inputted string can be converted into a float.

    Args:
        string (str): The string to be checked.

    Returns:
        check (bool): A value which tells the program whether or not the inputted string can be converted into a float.
    """
    
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_integer(string: str) -> bool:
    """Checks whether the inputted string can be converted into a integer.

    Args:
        string (str): The string to be checked.

    Returns:
        check (bool): A value which tells the program whether or not the inputted string can be converted into a integer.
    """
    
    try:
        int(string)
        return True
    except ValueError:
        return False

def load(path: str) -> dict:
    """A procedure which converts the yaml configuration file into a dictionary.

    Args:
        path (str): The path of the yaml configuration file.

    Returns:
        config (dict): The yaml configuration in dictionary form.
    """
    
    with open(path, "r") as yaml:
        levels = []
        data = {}
        
        for line in yaml.readlines():
            if line.strip() == "":
                continue
            elif line.rstrip()[-1] == ":":
                if int(len(line.replace(line.strip(), '')) / 2) < len(levels):
                    levels[int(len(line.replace(line.strip(), '')) / 2)] = f"['{line.strip()[:-1]}']"
                else:
                    levels.append(f"['{line.strip()[:-1]}']")
                exec(f"data{''.join(str(i) for i in levels[:int(len(line.replace(line.lstrip(), '')) / 2)])}['{line.strip()[:-1]}']" + " = {}")
                continue

            value = line.split(":")[-1].strip()
            
            if is_float(value) or is_integer(value) or value == "True" or value == "False":
                exec(f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:int(len(line.replace(line.lstrip(), '')) / 2)])}['{line.split(':')[0].strip()}'] = {value}")
            else:
                exec(f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:int(len(line.replace(line.lstrip(), '')) / 2)])}['{line.split(':')[0].strip()}'] = '{value}'")
    
    return data