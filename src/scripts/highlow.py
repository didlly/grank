def highlow(Client) -> None:
    """One of the 2 guess the number commands - `pls highlow`.

    Required item(s): None

    Args:
            Client (class): The Client for the user.

    Returns:
            None
    """

    Client.send_message("pls highlow")

    latest_message = Client.retreive_message("pls highlow")

    number = int(latest_message["embeds"][0]["description"].split("**")[-2])

    Client.interact_button(
        "pls highlow",
        latest_message["components"][0]["components"][0]["custom_id"]
        if number > 50
        else latest_message["components"][0]["components"][2]["custom_id"]
        if number < 50
        else latest_message["components"][0]["components"][1]["custom_id"],
        latest_message,
    )
