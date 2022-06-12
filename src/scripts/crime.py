from random import choice

from instance.Client import Instance


def crime(Client: Instance) -> bool:
    """
    The crime function is used to interact with the crime command.

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    Client.send_message("pls crime")

    latest_message = Client.retreive_message("pls crime")

    if "What crime do you want to commit" not in latest_message["content"]:
        latest_message = Client.fallback_retreive_message("pls crime")

    if Client.Repository.config["crime"]["random"]:
        custom_id = choice(latest_message["components"][0]["components"])["custom_id"]
    else:
        places = [
            button["label"].lower().replace("'", "")
            for button in latest_message["components"][0]["components"]
        ]

        custom_id = None

        for key in Client.Repository.config["crime"]["preferences"]:
            if not Client.Repository.config["crime"]["preferences"][key]:
                continue

            for index, place in enumerate(places):
                if key.lower() in place:
                    custom_id = latest_message["components"][0]["components"][index][
                        "custom_id"
                    ]

                    break

            if custom_id is not None:
                break

        if custom_id is None:
            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]

    Client.interact_button(
        "pls crime",
        custom_id,
        latest_message,
    )

    latest_message = Client.retreive_message(
        "pls crime", old_latest_message=latest_message
    )

    latest_message["embeds"][0]["description"] = latest_message["embeds"][0][
        "description"
    ].replace(" <:horseshoe:813911522975678476>", "")

    try:
        coins = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["embeds"][0]["description"].split("\n")[0],
                )
            )
        )
    except Exception:
        coins = 0

    try:
        item = (
            latest_message["embeds"][0]["description"].split("**")[-2]
            if latest_message["embeds"][0]["description"].count("**") == 2
            else "no items"
        )
    except Exception:
        item = "no items"

    Client.log(
        "DEBUG",
        f"Received {coins} coin{'' if coins == 1 else 's'} &{' an' if item[0] in ['a', 'e', 'i', 'o', 'u'] else '' if item == 'no items' else ' a'} {item} from the `pls crime` command.",
    )

    Client._update_coins("pls crime", coins)

    Client._update_items("pls crime", item)

    return True
