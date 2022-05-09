def is_float(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def is_integer(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False


def load(path: str) -> dict:
    with open(path, "r") as yaml:
        levels = []
        data = {}
        indentation_str = ""

        for line in yaml.readlines():
            if line.replace(line.lstrip(), "") != "" and indentation_str == "":
                indentation_str = line.replace(line.lstrip(), "").rstrip("\n")
            if line.strip() == "":
                continue
            elif line.rstrip()[-1] == ":":
                if len(line.replace(line.strip(), "")) // 2 < len(levels):
                    levels[
                        len(line.replace(line.strip(), "")) // 2
                    ] = f"['{line.strip()[:-1]}']"
                else:
                    levels.append(f"['{line.strip()[:-1]}']")
                exec(
                    f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{line.strip()[:-1]}']"
                    + " = {}"
                )

                continue

            value = line.split(":")[-1].strip()

            if (
                is_float(value)
                or is_integer(value)
                or value == "True"
                or value == "False"
                or ("[" in value and "]" in value)
            ):
                exec(
                    f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{line.split(':')[0].strip()}'] = {value}"
                )

            else:
                exec(
                    f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{line.split(':')[0].strip()}'] = '{value}'"
                )

    return data


def loads(yaml: str) -> dict:
    levels = []
    data = {}
    indentation_str = ""

    for line in yaml.split("\n"):
        if line.replace(line.lstrip(), "") != "" and indentation_str == "":
            indentation_str = line.replace(line.lstrip(), "")
        if line.strip() == "":
            continue
        elif line.rstrip()[-1] == ":":
            if len(line.replace(line.strip(), "")) // 2 < len(levels):
                levels[
                    len(line.replace(line.strip(), "")) // 2
                ] = f"['{line.strip()[:-1]}']"
            else:
                levels.append(f"['{line.strip()[:-1]}']")
            exec(
                f"data{''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{line.strip()[:-1]}']"
                + " = {}"
            )

            continue

        value = line.split(":")[-1].strip()

        if (
            is_float(value)
            or is_integer(value)
            or value == "True"
            or value == "False"
            or ("[" in value and "]" in value)
        ):
            exec(
                f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{line.split(':')[0].strip()}'] = {value}"
            )

        else:
            exec(
                f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:line.replace(line.lstrip(), '').count(indentation_str) if indentation_str != '' else 0])}['{line.split(':')[0].strip()}'] = '{value}'"
            )

    return data


def dumps(yaml: dict, indent="") -> str:
    """A procedure which converts the dictionary passed to the procedure into it's yaml equivalent.

    Args:
        yaml (dict): The dictionary to be converted.

    Returns:
        data (str): The dictionary in yaml form.
    """

    data = ""

    for key in yaml.keys():
        if type(yaml[key]) == dict:
            data += f"\n{indent}{key}:\n"
            data += dumps(yaml[key], f"{indent}  ")
        else:
            data += f"{indent}{key}: {yaml[key]}\n"

    return data
