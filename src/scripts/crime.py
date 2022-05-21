from random import choice
from time import sleep


def crime(Client) -> None:
    Client.send_message("pls crime")

    latest_message = Client.retreive_message("pls crime")

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

    sleep(0.5)

    latest_message = Client.retreive_message("pls crime")

    latest_message["embeds"][0]["description"] = latest_message["embeds"][0]["description"].replace(" <:horseshoe:813911522975678476>", "")
    
    try:
        coins = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["embeds"][0]["description"].split("\n")[0]
                )
            )
        )
    except Exception:
        coins = "no"

    try:
        items = (
            latest_message["embeds"][0]["description"].split("**")[-2]
            if latest_message["embeds"][0]["description"].count("**") == 2
            else "no items"
        )
    except Exception:
        items = "no items"

    Client.log(
        "DEBUG",
        f"Received {'⏣ ' if coins != 'no' else ''}{coins} coin{'' if coins == 1 else 's'} &{' an' if items[0] in ['a', 'e', 'i', 'o', 'u'] else '' if items == 'no items' else ' a'} {items} from the `pls crime` command.",
    )
