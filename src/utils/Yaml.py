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
        levels = []

        data = {}

        indentation_str = ""

        for line in yaml.readlines():
            if line.replace(line.lstrip(), "") != "" and indentation_str == "":
                indentation_str = line.replace(line.lstrip(), "").rstrip("\n")
            elif line.strip() == "":
                continue
            elif line.rstrip()[-1] == ":":
                key = line.strip()[:-1]

                quoteless = (
                    is_float(key)
                    or is_integer(key)
                    or key == "True"
                    or key == "False"
                    or ("[" in key and "]" in key)
                )

                if len(line.replace(line.strip(), "")) // 2 < len(levels):
                    if quoteless:
                        levels[len(line.replace(line.strip(), "")) // 2] = f"[{key}]"
                    else:
                        levels[len(line.replace(line.strip(), "")) // 2] = f"['{key}']"
                else:
                    if quoteless:
                        levels.append(f"[{line.strip()[:-1]}]")
                    else:
                        levels.append(f"['{line.strip()[:-1]}']")

                if quoteless:
                    exec(
                        f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}]"
                        + " = {}"
                    )
                else:
                    exec(
                        f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}']"
                        + " = {}"
                    )

                continue

            key = line.split(":")[0].strip()
            value = ":".join(line.split(":")[1:]).strip()

            if (
                is_float(value)
                or is_integer(value)
                or value == "True"
                or value == "False"
                or ("[" in value and "]" in value)
            ):
                if (
                    is_float(key)
                    or is_integer(key)
                    or key == "True"
                    or key == "False"
                    or ("[" in key and "]" in key)
                ):
                    exec(
                        f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}] = {value}"
                    )
                else:
                    exec(
                        f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}'] = {value}"
                    )
            else:
                if (
                    is_float(key)
                    or is_integer(key)
                    or key == "True"
                    or key == "False"
                    or ("[" in key and "]" in key)
                ):
                    exec(
                        f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}] = '{value}'"
                    )
                else:
                    exec(
                        f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}'] = '{value}'"
                    )

    return data


def loads(yaml: str) -> dict:
    """Converts the yaml given into a dictionary.

    Args:
        yaml (str): The yaml

    Returns:
        data (dict): The yaml file in dictionary form
    """

    levels = []

    data = {}

    indentation_str = ""

    for line in yaml.split("\n"):
        if line.replace(line.lstrip(), "") != "" and indentation_str == "":
            indentation_str = line.replace(line.lstrip(), "")
        elif line.strip() == "":
            continue
        elif line.rstrip()[-1] == ":":
            key = line.strip()[:-1]

            quoteless = (
                is_float(key)
                or is_integer(key)
                or key == "True"
                or key == "False"
                or ("[" in key and "]" in key)
            )

            if len(line.replace(line.strip(), "")) // 2 < len(levels):
                if quoteless:
                    levels[len(line.replace(line.strip(), "")) // 2] = f"[{key}]"
                else:
                    levels[len(line.replace(line.strip(), "")) // 2] = f"['{key}']"
            else:
                if quoteless:
                    levels.append(f"[{line.strip()[:-1]}]")
                else:
                    levels.append(f"['{line.strip()[:-1]}']")

            if quoteless:
                exec(
                    f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}]"
                    + " = {}"
                )
            else:
                exec(
                    f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}']"
                    + " = {}"
                )

            continue

        key = line.split(":")[0].strip()
        value = ":".join(line.split(":")[1:]).strip()

        if (
            is_float(value)
            or is_integer(value)
            or value == "True"
            or value == "False"
            or ("[" in value and "]" in value)
        ):
            if (
                is_float(key)
                or is_integer(key)
                or key == "True"
                or key == "False"
                or ("[" in key and "]" in key)
            ):
                exec(
                    f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}] = {value}"
                )
            else:
                exec(
                    f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}'] = {value}"
                )
        else:
            if (
                is_float(key)
                or is_integer(key)
                or key == "True"
                or key == "False"
                or ("[" in key and "]" in key)
            ):
                exec(
                    f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}[{key}] = '{value}'"
                )
            else:
                exec(
                    f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{key}'] = '{value}'"
                )

    return data


def dumps(data: dict, indent="") -> str:
    """A procedure which converts the dictionary passed to the procedure into it's yaml equivalent.

    Args:
        data (dict): The dictionary to be converted.
        indent (str) = "": The indentation of the current level.

    Returns:
        yaml (str): The dictionary in yaml form.
    """

    yaml = ""

    for key in data:
        if type(data[key]) == dict:
            yaml += f"\n{indent}{key}:\n"

            yaml += dumps(data[key], f"{indent}  ")
        else:
            yaml += f"{indent}{key}: {data[key]}\n"

    return yaml
