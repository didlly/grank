def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def load(file_path: str) -> dict:
    with open(file_path, "r") as yaml:
        levels = []
        data = {}

        for line in yaml.readlines():
            if line.strip() == "":
                continue
            elif line.rstrip()[-1] == ":":
                if int(len(line.replace(line.strip(), '')) / 2) < len(levels):
                    levels[int(len(line.replace(line.strip(), '')) / 2)] = (f"['{line.strip()[:-1]}']")
                else:
                    levels.append(f"['{line.strip()[:-1]}']")
                data[f"{line.strip()[:-1]}"] = {}
                continue

            value = line.split(":")[-1].strip()

            if is_float(value) or is_integer(value) or value == "True" or value == "False":
                exec(f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:int(len(line.replace(line.lstrip(), '')) / 2)])}['{line.split(':')[0].strip()}'] = {value}")
            else:
                exec(f"data{'' if line == line.strip() else ''.join(str(i) for i in levels[:int(len(line.replace(line.lstrip(), '')) / 2)])}['{line.split(':')[0].strip()}'] = '{value}'")

    return data