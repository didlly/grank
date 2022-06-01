def is_float(string: str) -> bool:
    """Checks whether the inputted string can be converted into a float

    Args:
        string (str): The string to be checked

    Returns:
        bool: True if string can be converted to a float, else False
    """

    try:
        float(string)
        return True
    except ValueError:
        return False


def is_integer(string: str) -> bool:
    """Checks whether the inputted string can be converted into an integer

    Args:
        string (str): The string to be checked

    Returns:
        bool: True if string can be converted to an integer, else False
    """

    try:
        int(string)
        return True
    except ValueError:
        return False


def load(path: str) -> dict:
    """Converts a yaml file at the path given into a dictionary.

    Args:
        path (str): The path to the yaml file

    Returns:
        data (dict): The yaml file in dictionary form
    """

    with open(path, "r") as yaml:
        # Initialize levels as an empty list. This data structure will hold the dictionary keys in the form `['{key}']` (e.g, `['commands']`)
        levels = []

        # Initialize data as an empty dictionary. This data structure will hold the converted yaml
        data = {}

        # Initialize indentation_str as en empty string. This variable will hold the string used for indentation
        indentation_str = ""

        # For each line in the yaml file...
        for line in yaml.readlines():
            # If the line is indented, and indentation_str is still set to an empty string...
            if line.replace(line.lstrip(), "") != "" and indentation_str == "":
                # ...set indentation_str (without the trailing `\n`) to the indent for that line
                indentation_str = line.replace(line.lstrip(), "").rstrip("\n")
            # Else if the line is empty...
            elif line.strip() == "":
                # ...continue to the next line
                continue
            # Elif the line is initializing a sub category (e.g., `commands:`)
            elif line.rstrip()[-1] == ":":
                # Strip the line of leading and trailing chars, and remove the `:`
                key = line.strip()[:-1]

                # Check if the key is not a string
                quoteless = (
                    is_float(key)
                    or is_integer(key)
                    or key == "True"
                    or key == "False"
                    or ("[" in key and "]" in key)
                )

                # If there is already a key at that level...
                if len(line.replace(line.strip(), "")) // 2 < len(levels):
                    # ...if the key is not a string...
                    if quoteless:
                        # ...replace the key at that level with the new key without quotes
                        levels[len(line.replace(line.strip(), "")) // 2] = f"[{key}]"
                    # ...else...
                    else:
                        # ...replace the key at that level with the new key with quotes
                        levels[len(line.replace(line.strip(), "")) // 2] = f"['{key}']"
                # Else...
                else:
                    # ...if the key is not a string...
                    if quoteless:
                        # ...add a new key without quotes
                        levels.append(f"[{line.strip()[:-1]}]")
                    # ...else...
                    else:
                        # ...add a new key with quotes
                        levels.append(f"['{line.strip()[:-1]}']")

                # If the key is not a string...
                if quoteless:
                    # ...add key without quotes as a new key to data
                    exec(
                        f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}]"
                        + " = {}"
                    )
                # Else...
                else:
                    # ...ad key with quotes as a new key o data
                    exec(
                        f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}']"
                        + " = {}"
                    )

                continue

            # Get the key
            key = line.split(":")[0].strip()
            # Get the value
            value = ":".join(line.split(":")[1:]).strip()

            # !-Please don't ask why it doesn't check whether key should be quoteless before it checks whether value should be quoteless. I should really change it since that would make more sense but I don't have time-!

            # If the value is not a string...
            if (
                is_float(value)
                or is_integer(value)
                or value == "True"
                or value == "False"
                or ("[" in value and "]" in value)
            ):
                # ...if the key is not a string...
                if (
                    is_float(key)
                    or is_integer(key)
                    or key == "True"
                    or key == "False"
                    or ("[" in key and "]" in key)
                ):
                    # ...add the key without quotes and value without quotes to data
                    exec(
                        f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}] = {value}"
                    )
                # Else...
                else:
                    # ...add the key with quotes and value without quotes to data
                    exec(
                        f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}'] = {value}"
                    )
            # Else...
            else:
                # ...if the key is not a string...
                if (
                    is_float(key)
                    or is_integer(key)
                    or key == "True"
                    or key == "False"
                    or ("[" in key and "]" in key)
                ):
                    # ...add the key without quotes and value with quotes to data
                    exec(
                        f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}] = '{value}'"
                    )
                # Else...
                else:
                    # ...add the key with quotes and value with quotes to data
                    exec(
                        f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}'] = '{value}'"
                    )

    # Return the converted yaml
    return data


def loads(yaml: str) -> dict:
    """Converts the yaml given into a dictionary.

    Args:
        yaml (str): The yaml

    Returns:
        data (dict): The yaml file in dictionary form
    """

    # Initialize levels as an empty list. This data structure will hold the dictionary keys in the form `['{key}']` (e.g, `['commands`])
    levels = []

    # Initialize data as an empty dictionary. This data structure will hold the converted yaml
    data = {}

    # Initialize indentation_str as en empty string. This variable will hold the string used for indentation
    indentation_str = ""

    # For each line in the yaml file...
    for line in yaml.split("\n"):
        # If the line is indented, and indentation_str is still set to an empty string...
        if line.replace(line.lstrip(), "") != "" and indentation_str == "":
            # ...set indentation_str to the indent for that line
            indentation_str = line.replace(line.lstrip(), "")
        # Else if the line is empty...
        elif line.strip() == "":
            # ...continue to the next line
            continue
        # Elif the line is initializing a sub category (e.g., `commands:`)
        elif line.rstrip()[-1] == ":":
            # Strip the line of leading and trailing chars, and remove the `:`
            key = line.strip()[:-1]

            # Check if the key is not a string
            quoteless = (
                is_float(key)
                or is_integer(key)
                or key == "True"
                or key == "False"
                or ("[" in key and "]" in key)
            )

            # If there is already a key at that level...
            if len(line.replace(line.strip(), "")) // 2 < len(levels):
                # ...if the key is not a string...
                if quoteless:
                    # ...replace the key at that level with the new key without quotes
                    levels[len(line.replace(line.strip(), "")) // 2] = f"[{key}]"
                # ...else...
                else:
                    # ...replace the key at that level with the new key with quotes
                    levels[len(line.replace(line.strip(), "")) // 2] = f"['{key}']"
            # Else...
            else:
                # ...if the key is not a string...
                if quoteless:
                    # ...add a new key without quotes
                    levels.append(f"[{line.strip()[:-1]}]")
                # ...else...
                else:
                    # ...add a new key with quotes
                    levels.append(f"['{line.strip()[:-1]}']")

            # If the key is not a string...
            if quoteless:
                # ...add key without quotes as a new key to data
                exec(
                    f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}]"
                    + " = {}"
                )
            # Else...
            else:
                # ...ad key with quotes as a new key o data
                exec(
                    f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}']"
                    + " = {}"
                )

            continue

        # Get the key
        key = line.split(":")[0].strip()
        # Get the value
        value = ":".join(line.split(":")[1:]).strip()

        # !-Please don't ask why it doesn't check whether key should be quoteless before it checks whether value should be quoteless. I should really change it since that would make more sense but I don't have time-!

        # If the value is not a string...
        if (
            is_float(value)
            or is_integer(value)
            or value == "True"
            or value == "False"
            or ("[" in value and "]" in value)
        ):
            # ...if the key is not a string...
            if (
                is_float(key)
                or is_integer(key)
                or key == "True"
                or key == "False"
                or ("[" in key and "]" in key)
            ):
                # ...add the key without quotes and value without quotes to data
                exec(
                    f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}] = {value}"
                )
            # Else...
            else:
                # ...add the key with quotes and value without quotes to data
                exec(
                    f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}'] = {value}"
                )
        # Else...
        else:
            # ...if the key is not a string...
            if (
                is_float(key)
                or is_integer(key)
                or key == "True"
                or key == "False"
                or ("[" in key and "]" in key)
            ):
                # ...add the key without quotes and value with quotes to data
                exec(
                    f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}] = '{value}'"
                )
            # Else...
            else:
                # ...add the key with quotes and value with quotes to data
                exec(
                    f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}'] = '{value}'"
                )

    # Return the converted yaml
    return data


def dumps(data: dict, indent="") -> str:
    """A procedure which converts the dictionary passed to the procedure into it's yaml equivalent.

    Args:
        data (dict): The dictionary to be converted.
        indent (str) = "": The indentation of the current level.

    Returns:
        yaml (str): The dictionary in yaml form.
    """

    # Initialize yaml as an empty string
    yaml = ""

    # For each key in the yaml dictionary...
    for key in data.keys():
        # ...if the key's value is a dictionary...
        if type(data[key]) == dict:
            # ...add a subcategory to the yaml
            yaml += f"\n{indent}{key}:\n"

            # ..add the output of a recursive call of dumps on the key's value
            yaml += dumps(data[key], f"{indent}  ")
        # Else...
        else:
            # ...add the key and value to the yaml
            yaml += f"{indent}{key}: {data[key]}\n"

    # Return the yaml
    return yaml
