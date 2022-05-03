def lottery(Client) -> None:
    Client.send_message("pls lottery")

    latest_message = Client.retreive_message("pls lottery")

    Client.interact_button(
        "pls lottery",
        latest_message["components"][0]["components"][-1]["custom_id"],
        latest_message,
    )
