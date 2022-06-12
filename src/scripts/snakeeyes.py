from random import randint

from instance.Client import Instance


def snakeeyes(Client: Instance) -> bool:
    """
    The snakeeyes function is used to interact with the snakeeyes command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    amount = (
        randint(
            Client.Repository.config["snakeeyes"]["minimum"],
            Client.Repository.config["snakeeyes"]["maximum"],
        )
        if Client.Repository.config["snakeeyes"]["random"]
        else Client.Repository.config["snakeeyes"]["amount"]
    )

    Client.send_message(f"pls snakeeyes {amount}")

    Client.retreive_message(f"pls snakeeyes {amount}")

    return True
