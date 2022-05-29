def highlow(Client) -> None:
    Client.send_message("pls highlow")

    latest_message = Client.retreive_message("pls highlow")

    if "description" not in latest_message["embeds"][0].keys():
        latest_message = Client.fallback_retreive_message("pls highlow")
    elif (
        "I just chose a secret number between 1 and 100"
        not in latest_message["embeds"][0]["description"]
    ):
        latest_message = Client.fallback_retreive_message("pls highlow")

    number = int(latest_message["embeds"][0]["description"].split("**")[-2])

    Client.interact_button(
        "pls highlow",
        latest_message["components"][0]["components"][0]["custom_id"]
        if number > 50
        else latest_message["components"][0]["components"][2]["custom_id"],
        latest_message,
    )

    latest_message = Client.retreive_message(
        "pls highlow", old_latest_message=latest_message
    )

    if "You won" in latest_message["embeds"][0]["description"]:
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
            coins = "no"

        Client.log(
            "DEBUG",
            f"Received {coins} coin{'' if coins == 1 else 's'} from the `pls highlow` command.",
        )
        Client._update_coins("pls highlow", coins)
    else:
        Client.log(
            "DEBUG", "Lost the `pls highlow` command (no negative balance impacts)."
        )
