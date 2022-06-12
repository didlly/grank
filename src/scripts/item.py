from instance.Client import Instance


def has_item(Client: Instance, item: str) -> bool:
    """
    The has_item function checks if the account has an item.
    It takes in a string as an argument, which is the name of the item to be checked for.
    The function then sends a message asking for information about the item, and parses the number of owned items from the embed.

    Args:
        Client (Instance): The Discord client
        item (str) The item to be checked

    Returns:
        bool: Indicates whether the account has the item or not
    """

    Client.send_message(f"pls shop {item}")

    latest_message = Client.retreive_message(f"pls shop {item}")

    try:
        num_items = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["embeds"][0]["title"],
                )
            )
        )
    except Exception:
        num_items = 0

    return True if num_items > 0 else False
