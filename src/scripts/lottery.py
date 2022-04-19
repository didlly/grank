def lottery(Client) -> None:
    """One of the 3 gambling commands - `pls lottery`.

    Required item(s): None

    Args:
            Client (class): The Client for the user.

    Returns:
            None
    """

    Client.send_message("pls lottery")

    latest_message = Client.retreive_message("pls lottery")

    Client.interact_button(
        "pls lottery",
        latest_message["components"][0]["components"][-1]["custom_id"],
        latest_message,
    )
