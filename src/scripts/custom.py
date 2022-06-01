from instance.Client import Instance


def custom(Client: Instance, command: str) -> bool:
    """
    The custom function allows a custom message to be sent.

    Args:
        Client (Instance): The Discord client
        command (str): The command that will be sent

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    Client.send_message(command)

    Client.retreive_message(command)

    return True
