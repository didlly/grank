from random import choice


def postmeme(Client) -> None:
    Client.send_message("pls postmeme")

    latest_message = Client.retreive_message("pls postmeme")

    Client.interact_button(
        "pls postmeme",
        choice(latest_message["components"][0]["components"])["custom_id"],
        latest_message,
    )

    latest_message = Client.retreive_message(
        "pls postmeme", old_latest_message=latest_message
    )

    try:
        coins = (
            latest_message["embeds"][0]["description"]
            .split("\n")[2]
            .split("**")[1]
            .replace("⏣ ", "")
        )
    except Exception:
        coins = 0

    if "also a fan of your memes" in latest_message["embeds"][0]["description"]:
        try:
            items = (
                latest_message["embeds"][0]["description"]
                .split("\n")[-1]
                .split("**")[-2]
            )
        except Exception:
            items = "no items"
    else:
        items = "no items"

    Client.log(
        "DEBUG",
        f"Received ⏣ {coins} coin{'' if coins == 1 else 's'} &{' an' if items[0] in ['a', 'e', 'i', 'o', 'u'] else '' if items == 'no items' else ' a'} {items} from the `pls postmeme` command.",
    )
    Client._update_coins("pls postmeme", coins)