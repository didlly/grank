from random import choice


def crime(Client) -> None:
    Client.send_message("pls crime")

    latest_message = Client.retreive_message("pls crime")

    if "What crime do you want to commit" not in latest_message["content"]:
        latest_message = Client.fallback_retreive_message("pls crime")

    custom_id = next(
        (
            option["custom_id"]
            for option in latest_message["components"][0]["components"]
            if option["label"] == "tax evasion"
        ),
        choice(latest_message["components"][0]["components"])["custom_id"],
    )
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
        f"Received ⏣ {coins} coin{'' if coins == 1 else 's'} &{' an' if item[0] in ['a', 'e', 'i', 'o', 'u'] else '' if item == 'no items' else ' a'} {item} from the `pls crime` command.",
    )

    Client._update_coins("pls crime", coins)
    Client._update_items("pls crime", item)