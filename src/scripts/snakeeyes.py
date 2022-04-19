from random import randint


def snakeeyes(Client) -> None:
    """One of the 3 gamble commands - `pls snakeeyes`.

    Required item(s): None

    Args:
            Client (class): The Client for the user.

    Returns:
            None
    """

    amount = (
        randint(
            Client.config["snakeeyes"]["minimum"],
            Client.config["snakeeyes"]["maximum"],
        )
        if Client.config["snakeeyes"]["random"]
        else Client.config["snakeeyes"]["amount"]
    )

    Client.send_message(f"pls snakeeyes {amount}")
