def parse_args(cmd: str):
    class Args(object):
        def __init__(self, command, subcommand, variables, flags, var):
            self.command = command.strip()
            self.subcommand = subcommand
            self.variables = variables
            self.flags = flags
            self.var = var

    msg = cmd[:]
    cmd = cmd.split(" ")[1:]

    command = cmd[0].split(".")[0] if "." in cmd[0] else cmd[0].split(" ")[0]
    subcommand = [arg for arg in msg.split(" ")[2:] if arg[0] != "-"]
    variables = (
        [arg.replace("=", "") for index, arg in enumerate(cmd[0].split(".")[1:])]
        if "." in cmd[0]
        else [
            arg.replace("=", "")
            for index, arg in enumerate(cmd[0].split(" ")[1:])
            if index != 0
        ]
    )
    flags = [arg[1:] for arg in cmd if arg[0] == "-"]

    var = None

    if "=" in msg:
        var = msg.split(" = ")[-1].strip()

    return Args(command, subcommand, variables, flags, var)
