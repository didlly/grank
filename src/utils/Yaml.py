from email.quoprimime import quote


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
            value = line.split(":")[-1].strip()

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
    levels = []
    data = {}
    indentation_str = ""

    for line in yaml.split("\n"):
        if line.replace(line.lstrip(), "") != "" and indentation_str == "":
            indentation_str = line.replace(line.lstrip(), "")
        if line.strip() == "":
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
        value = line.split(":")[-1].strip()

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
