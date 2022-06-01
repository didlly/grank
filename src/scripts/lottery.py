from instance.Client import Instance


def lottery(Client: Instance) -> bool:
    """
    The lottery function is used to interact with the lottery command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Send the command `pls lottery`
    Client.send_message("pls lottery")

    # Get Dank Memer's response to the command `pls lottery`
    latest_message = Client.retreive_message("pls lottery")

    # Interact with the `Confirm` button
    Client.interact_button(
        "pls lottery",
        latest_message["components"][0]["components"][-1]["custom_id"],
        latest_message,
    )

    return True
