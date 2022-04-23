from random import choice


def crime(Client) -> None:
    """One of the basic 7 currency commands - `pls crime`.

    Required item(s): None

    Args:
            Client (class): The Client for the user.

    Returns:
            None
    """

    Client.send_message("pls crime")

    latest_message = Client.retreive_message("pls crime")

    custom_id = next(
        (
            option["custom_id"]
            for option in latest_message["components"][0]["components"]
            if option["label"] == "tax evasion"
        ),
        None,
    )
    Client.interact_button(
        "pls crime",
        choice(latest_message["components"][0]["components"])["custom_id"]
        if custom_id is None
        else custom_id,
        latest_message,
    )

    latest_message = Client.retreive_message("pls crime")

    try:
        coins = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["embeds"][0]["description"],
                )
            )
        )
    except Exception:
        coins = "no"

    items = (
        latest_message["embeds"][0]["description"].split("**")[-1]
        if latest_message["embeds"][0]["description"].count("**") == 2
        else "no items"
    )

    Client.log(
        "DEBUG",
        f"Received {coins} coin{'' if coins == 1 else 's'} &{' an' if items[0] in ['a', 'e', 'i', 'o', 'u'] else '' if items == 'no items' else ' a'} {items} from the `pls crime` command.",
    )
