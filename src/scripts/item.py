def has_item(Client, item: str) -> None:
    """Checks if the user has the specified item.

    Args:
            Client (class): The Client for the user.
            item (str): The item to be checked.

    Returns:
            found (bool): Boolean dictating whether the user has the item or not.
    """

    Client.send_message(f"pls item {item}")

    latest_message = Client.retreive_message(f"pls item {item}")

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
