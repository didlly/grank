def beg(Client) -> None:
    Client.send_message("pls beg")

    latest_message = Client.retreive_message("pls beg")

    latest_message["embeds"][0]["description"] = latest_message["embeds"][0]["description"].replace(" <:horseshoe:813911522975678476>", "")

    try:
        coins = latest_message["embeds"][0]["description"].split("**")[1].replace("⏣ ", "") if "⏣" in latest_message["embeds"][0]["description"] else "no"
    except Exception:
        coins = "no"

    try:
        items = latest_message["embeds"][0]["description"].split("**")[-2] if latest_message["embeds"][0]["description"].count("**") == 4 else "no items"
    except Exception:
        items = "no items"

    Client.log(
        "DEBUG",
        f"Received {'⏣ ' if coins != 'no' else ''}{coins} coin{'' if coins == 1 else 's'} &{' an' if items[0] in ['a', 'e', 'i', 'o', 'u'] else '' if items == 'no items' else ' a'} {items} from the `pls beg` command.",
    )
