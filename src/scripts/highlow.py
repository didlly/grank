from instance.Client import Instance


def highlow(Client: Instance) -> bool:
    """
    The highlow function is used to interact with the highlow command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Send the command `pls highlow`
    Client.send_message("pls highlow")

    # Get Dank Memer's response to `pls highlow`
    latest_message = Client.retreive_message("pls highlow")

    # If the wrong latest message was retreived...
    if "description" not in latest_message["embeds"][0]:
        # ...get the correct latest message
        latest_message = Client.fallback_retreive_message("pls highlow")
    elif (
        "I just chose a secret number between 1 and 100"
        not in latest_message["embeds"][0]["description"]
    ):
        # ...get the correct latest message
        latest_message = Client.fallback_retreive_message("pls highlow")

    # Get the hint
    number = int(latest_message["embeds"][0]["description"].split("**")[-2])

    # Interact with the `Lower` button if hint > 50 else `Higher`
    Client.interact_button(
        "pls highlow",
        latest_message["components"][0]["components"][0]["custom_id"]
        if number > 50
        else latest_message["components"][0]["components"][2]["custom_id"],
        latest_message,
    )

    # Get Dank Memer's edited response
    latest_message = Client.retreive_message(
        "pls highlow", old_latest_message=latest_message
    )

    # If we won...
    if "You won" in latest_message["embeds"][0]["description"]:
        try:
            # ...try and get the coins gained from the command
            coins = int(
                "".join(
                    filter(
                        str.isdigit,
                        latest_message["embeds"][0]["description"].split("\n")[0],
                    )
                )
            )
        except Exception:
            # If an Exception is raised, it will be caught here and the coins gained will be set to 0
            coins = 0

        Client.log(
            "DEBUG",
            f"Received {coins} coin{'' if coins == 1 else 's'} from the `pls highlow` command.",
        )

        # Update the coins gained
        Client._update_coins("pls highlow", coins)
    else:
        Client.log(
            "DEBUG", "Lost the `pls highlow` command (no negative balance impacts)."
        )

    return True
