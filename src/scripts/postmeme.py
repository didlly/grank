from random import choice

from instance.Client import Instance


def postmeme(Client: Instance) -> None:
    """
    The postmeme function is used to interact with the postmeme command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Send the command `pls postmeme`
    Client.send_message("pls postmeme")

    # Get Dank Memer's response to `pls postmeme`
    latest_message = Client.retreive_message("pls postmeme")

    # If the wrong latest message was retreived...
    if "description" not in latest_message["embeds"][0].keys():
        # ...get the correct latest message
        latest_message = Client.fallback_retreive_message("pls postmeme")
    elif (
        "Pick a meme to post to the internet"
        not in latest_message["embeds"][0]["description"]
    ):
        # ...get the correct latest message
        latest_message = Client.fallback_retreive_message("pls highlow")

    # Interact with a random button
    Client.interact_button(
        "pls postmeme",
        choice(latest_message["components"][0]["components"])["custom_id"],
        latest_message,
    )

    # Get Dank Memer's edited response
    latest_message = Client.retreive_message(
        "pls postmeme", old_latest_message=latest_message
    )

    try:
        # ...try and get the coins gained from the command
        coins = (
            latest_message["embeds"][0]["description"]
            .split("\n")[2]
            .split("**")[1]
            .replace("⏣ ", "")
        )
    except Exception:
        # If an Exception is raised, it will be caught here and the coins gained will be set to 0
        coins = 0

    if "also a fan of your memes" in latest_message["embeds"][0]["description"]:
        try:
            # Try and get the item gained from the command
            item = (
                latest_message["embeds"][0]["description"]
                .split("\n")[-1]
                .split("**")[-2]
            )
        except Exception:
            # If an Exception is raised, it will be caught here and the item gained will be set to `no items`
            item = "no items"
    else:
        item = "no items"

    Client.log(
        "DEBUG",
        f"Received {coins} coin{'' if coins == 1 else 's'} &{' an' if item[0] in ['a', 'e', 'i', 'o', 'u'] else '' if item == 'no items' else ' a'} {item} from the `pls postmeme` command.",
    )

    # Update the coins gained
    Client._update_coins("pls postmeme", coins)

    # Update the items gained
    Client._update_items("pls postmeme", item)

    return True
