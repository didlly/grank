from instance.Client import Instance


def beg(Client: Instance) -> bool:
    """
    The beg function is used to interact with the beg command.

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Send the command `pls beg`
    Client.send_message("pls beg")

    # Get Dank Memer's response to `pls beg`
    latest_message = Client.retreive_message("pls beg")

    # Remove the horseshoe emoji from Dank Memer's response
    latest_message["embeds"][0]["description"] = latest_message["embeds"][0][
        "description"
    ].replace(" <:horseshoe:813911522975678476>", "")

    try:
        # Try and get the coins gained from the command
        coins = (
            latest_message["embeds"][0]["description"].split("**")[1].replace("⏣ ", "")
            if "⏣" in latest_message["embeds"][0]["description"]
            else 0
        )
    except Exception:
        # If an Exception is raised, it will be caught here and the coins gained will be set to 0
        coins = 0

    try:
        # Try and get the item gained from the command
        item = (
            latest_message["embeds"][0]["description"].split("**")[-2]
            if latest_message["embeds"][0]["description"].count("**") == 4
            else "no items"
        )
    except Exception:
        # If an Exception is raised, it will be caught here and the item gained will be set to `no items`
        item = "no items"

    Client.log(
        "DEBUG",
        f"Received {coins} coin{'' if coins == 1 else 's'} &{' an' if item[0] in ['a', 'e', 'i', 'o', 'u'] else '' if item == 'no items' else ' a'} {item} from the `pls beg` command.",
    )

    # Update the coins gained
    Client._update_coins("pls beg", coins)

    # Update the items gained
    Client._update_items("pls beg", item)

    return True
