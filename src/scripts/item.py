def has_item(Client, item: str) -> None:
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
