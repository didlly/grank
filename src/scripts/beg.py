from instance.Client import Instance


def beg(Client: Instance) -> bool:
    """
    The beg function is used to interact with the beg command.

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    Client.send_message("pls beg")

    latest_message = Client.retreive_message("pls beg")

    latest_message["embeds"][0]["description"] = latest_message["embeds"][0][
        "description"
    ].replace(" <:horseshoe:813911522975678476>", "")

    try:
        coins = (
            latest_message["embeds"][0]["description"].split("**")[1].replace("⏣ ", "")
            if "⏣" in latest_message["embeds"][0]["description"]
            else 0
        )
    except Exception:
        coins = 0

    try:
        item = (
            latest_message["embeds"][0]["description"].split("**")[-2]
            if latest_message["embeds"][0]["description"].count("**") == 4
            else "no items"
        )
    except Exception:
        item = "no items"

    Client.log(
        "DEBUG",
        f"Received {coins} coin{'' if coins == 1 else 's'} &{' an' if item[0] in ['a', 'e', 'i', 'o', 'u'] else '' if item == 'no items' else ' a'} {item} from the `pls beg` command.",
    )

    Client._update_coins("pls beg", coins)

    Client._update_items("pls beg", item)

    return True
