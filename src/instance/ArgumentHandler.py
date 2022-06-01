def parse_args(cmd: str):
    """
    The parse_args function takes a string as input and returns an object with the following attributes:
        command (str): The first word of the input string.
        subcommand (list): A list of all words in the input string that follow 'command'.
        variables (list): A list of all words in 'subcommand' that are separated by equals signs.
            For example, if "foo=bar" is present in 'subcommand', it will be included as one element
            in this attribute's value. If there are no variables, this attribute will be an empty list.

        flags (list): A list containing any elements from 'subcommand' that begin with a dash ('-').

        var (str or NoneType): If there is exactly one variable defined by equals signs, then this attribute
            contains its value; otherwise it is None.

    Args:
        cmd (str): The command to be parsed

    Returns:
        A class object with the attributes `command`, `subcommand`, `variables`, `flags` & `var`
    """

    class Args(object):
        def __init__(self, command, subcommand, variables, flags, var):
            self.command = command.strip()
            self.subcommand = subcommand
            self.variables = variables
            self.flags = flags
            self.var = var

    # Copy the command into the msg variable
    msg = cmd[:]

    # Split the msg variable into words and skip the first word (i.e., `grank`).\
    cmd = cmd.split(" ")[1:]

    # Get the command (e.g., `config`). If there is a `.` in the first word, get the part of the first word before the `.` (i.e, `config.commands` becomes `config`). Else, keep the command as the first word.
    command = cmd[0].split(".")[0] if "." in cmd[0] else cmd[0]

    # Gets the subcommand(s) (e.g, `add`) by iterating through the words in msg (skipping command) and adding it if it doesn't start with `-` (because then it is a flag).
    subcommand = [arg for arg in cmd[1:] if arg[0] != "-"]

    # Gets the variable(s) by iterating through the subcommand and getting the value(s) (removing `=`)
    variables = (
        [arg.replace("=", "") for arg in cmd[0].split(".")[1:]]
        if "." in cmd[0]
        else [arg.replace("=", "") for arg in cmd[0].split(" ")[1:]]
    )

    # Gets the flag(s) by iterating trough all the word(s) in msg and adding them if they start with `-`
    flags = [arg[1:] for arg in cmd if arg[0] == "-"]

    var = None

    if "=" in msg:
        # Gets the var if `=` is in the msg, otherwise var is left as `None`
        var = msg.split(" = ")[-1].strip()

    # Returns the class version of the parsed command
    return Args(command, subcommand, variables, flags, var)
