from instance.Client import Instance


def daily(Client: Instance) -> bool:
    """
    The daily function is used to interact with the daily command.

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    Client.send_message("pls daily")

    return True
