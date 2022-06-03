from random import choice, randint

from instance.Client import Instance
from scripts.buy import buy
from scripts.item import has_item


def stream(Client: Instance) -> bool:
    """
    The stream function is used to interact with the stream command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Initialise bought_mouse & bought_keyboard to True
    bought_mouse, bought_keyboard = [True] * 2

    # Send the command `pls stream`
    Client.send_message("pls stream")

    # Get Dank Memer's response to `pls stream`
    latest_message = Client.retreive_message("pls stream")

    # If the stream timed out...
    if "You were inactive" in latest_message["content"]:
        Client.log("WARNING", "Stream ended due to inactivity. Re-starting stream.")

        # ...get Dank Memer's next message (the stream timed out and stream controllers messages are separate)
        latest_message = Client.retreive_message(
            "pls stream", old_latest_message=latest_message
        )

    # If the response has a `description` section in the embed...
    if "description" in latest_message["embeds"][0]:
        # ...if the `description` section has `keyboard` in it...
        if "keyboard" in latest_message["embeds"][0]["description"].lower():
            # ...if the account does not have a `keyboard`...
            if not has_item(Client, "keyboard"):
                Client.log(
                    "DEBUG",
                    "Account does not have item `keyboard`. Buying keyboard now.",
                )

                # ...if autobuy is enabled...
                if (
                    Client.Repository.config["auto buy"]
                    and Client.Repository.config["auto buy"]["keyboard"]
                ):
                    # ...try and buy a `keyboard`
                    bought_keyboard = buy(Client, "keyboard")
                # Else...
                else:
                    Client.log(
                        "WARNING",
                        f"A keyboard is required for the command `pls stream`. However, since {'autobuy is off for keyboards,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
                    )
                    # ...return False
                    return False
        # ...if the `description` section has `Mouse` in it...
        if "mouse" in latest_message["embeds"][0]["description"].lower():
            # ...if the account does not have a `mouse`...
            if not has_item(Client, "mouse"):
                Client.log(
                    "DEBUG", "Account does not have item `mouse`. Buying mouse now."
                )

                # ...if autobuy is enabled...
                if (
                    Client.Repository.config["auto buy"]
                    and Client.Repository.config["auto buy"]["mouse"]
                ):
                    # ...try and buy a `mouse`
                    bought_mouse = buy(Client, "mouse")
                # Else...
                else:
                    Client.log(
                        "WARNING",
                        f"A mouse is required for the command `pls stream`. However, since {'autobuy is off for mouses,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
                    )
                    # ...return False
                    return False

    # If buying a mouse or keyboard failed...
    if not bought_mouse or not bought_keyboard:
        # ...return False
        return False

    # If there are three buttons on Dank Memer's response...
    if len(latest_message["components"][0]["components"]) == 3:
        # ...if the response has a `footer` section in the embed...
        if "footer" in latest_message["embeds"][0]:
            # ...if the `footer` section has `Wait` in it's text section...
            if "Wait" in latest_message["embeds"][0]["footer"]["text"]:
                Client.log("DEBUG", "Cannot stream yet - awaiting cooldown end.")

                # ...interact with the `End Interaction` button
                Client.interact_button(
                    "pls stream",
                    latest_message["components"][-1]["components"][-1]["custom_id"],
                    latest_message,
                )
                return False

        # Interact with the `Go Live` button
        Client.interact_button(
            "pls stream",
            latest_message["components"][0]["components"][0]["custom_id"],
            latest_message,
        )

        # Get Dank Memer's edited response
        latest_message = Client.retreive_message(
            "pls stream", old_latest_message=latest_message
        )

        # Select a random dropdown item
        Client.interact_dropdown(
            "pls stream",
            latest_message["components"][0]["components"][0]["custom_id"],
            choice(latest_message["components"][0]["components"][0]["options"])[
                "value"
            ],
            latest_message,
        )

        # Interact with the `Go Live` button
        Client.interact_button(
            "pls stream",
            latest_message["components"][-1]["components"][0]["custom_id"],
            latest_message,
        )

    # Get Dank Memer's edited response
    latest_message = Client.retreive_message(
        "pls stream", old_latest_message=latest_message
    )

    # If the wrong latest message was retreived...
    if "fields" not in latest_message["embeds"][0]:
        # ...get the correct latest message
        latest_message = Client.fallback_retreive_message("pls stream")
    elif len(latest_message["embeds"][0]["fields"]) != 6:
        # ...get the correct latest message
        latest_message = Client.fallback_retreive_message("pls stream")

    # If the stream has sponsers, and the config allows running ads on stream...
    if (
        int(latest_message["embeds"][0]["fields"][5]["value"].replace("`", "")) > 0
        and Client.Repository.config["stream"]["ads"]
    ):
        # ...run an ad
        Client.interact_button(
            "pls stream",
            latest_message["components"][0]["components"][0]["custom_id"],
            latest_message,
        )
    # Else...
    else:
        # Choose a button that abides by the config
        button = (
            randint(1, 2)
            if Client.Repository.config["stream"]["chat"]
            and Client.Repository.config["stream"]["donations"]
            else 1
            if Client.Repository.config["stream"]["chat"]
            else 2
            if Client.Repository.config["stream"]["donations"]
            else None
        )

        # If no button abides by the config...
        if button is None:
            # ...return False
            return False

        # Interact with the button
        Client.interact_button(
            "pls stream",
            latest_message["components"][0]["components"][button]["custom_id"],
            latest_message,
        )

    # Interact with the `End Interaction` button
    Client.interact_button(
        "pls stream",
        latest_message["components"][-1]["components"][-1]["custom_id"],
        latest_message,
    )

    return True
