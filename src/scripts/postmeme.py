from random import choice


def postmeme(Client) -> None:
    """One of the basic 7 currency commands - `pls postmeme`.

    Required item(s): None

    Args:
            Client (class): The Client for the user.

    Returns:
            None
    """

    Client.send_message("pls postmeme")

    latest_message = Client.retreive_message("pls postmeme")

    Client.interact_button(
        "pls postmeme",
        choice(latest_message["components"][0]["components"])["custom_id"],
        latest_message,
    )
