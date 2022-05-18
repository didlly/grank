from random import choice, randint
from time import sleep

from scripts.buy import buy
from scripts.item import has_item


def stream(Client) -> None:
    bought_keyboard, bought_mouse = [True] * 2

    while True:
        Client.send_message("pls stream")

        latest_message = Client.retreive_message("pls stream")

        if "You were inactive" in latest_message["content"]:
            Client.log("WARNING", "Stream ended due to inactivity. Re-starting stream.")
            sleep(2)
            latest_message = Client.retreive_message("pls stream")

        if "title" not in latest_message["embeds"][0].keys():
            break

        if "Keyboard" in latest_message["embeds"][0]["description"]:
            if not has_item(Client, "keyboard"):
                if Client.Repository.config["logging"]["debug"]:
                    Client.log(
                        "DEBUG",
                        "User does not have item `keyboard`. Buying keyboard now.",
                    )

                if (
                    Client.Repository.config["auto buy"]
                    and Client.Repository.config["auto buy"]["keyboard"]
                ):
                    bought_keyboard = buy(Client, "keyboard")

                elif Client.Repository.config["logging"]["warning"]:
                    Client.log(
                        "WARNING",
                        f"A keyboard is required for the command `pls stream`. However, since {'autobuy is off for keyboards,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
                    )

        if "Mouse" in latest_message["embeds"][0]["description"]:
            if not has_item(Client, "mouse"):
                if Client.Repository.config["logging"]["debug"]:
                    Client.log(
                        "DEBUG", "User does not have item `mouse`. Buying mouse now."
                    )

                if (
                    Client.Repository.config["auto buy"]
                    and Client.Repository.config["auto buy"]["mouse"]
                ):
                    bought_mouse = buy(Client, "mouse")

                elif Client.Repository.config["logging"]["warning"]:
                    Client.log(
                        "WARNING",
                        f"A mouse is required for the command `pls stream`. However, since {'autobuy is off for mouses,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
                    )

    if not bought_keyboard or not bought_mouse:
        return False

    if len(latest_message["components"][0]["components"]) == 3:
        if "footer" in latest_message["embeds"][0].keys():
            if "text" in latest_message["embeds"][0]["footer"].keys():
                if "Wait" in latest_message["embeds"][0]["footer"]["text"]:
                    Client.log("DEBUG", "Cannot stream yet - awaiting cooldown end.")

                    Client.interact_button(
                        "pls stream",
                        latest_message["components"][0]["components"][-1]["custom_id"],
                        latest_message,
                    )
                    return

        Client.interact_button(
            "pls stream",
            latest_message["components"][0]["components"][0]["custom_id"],
            latest_message,
        )

        sleep(1)

        latest_message = Client.retreive_message("pls stream")

        Client.interact_dropdown(
            "pls stream",
            latest_message["components"][0]["components"][0]["custom_id"],
            choice(latest_message["components"][0]["components"][0]["options"])[
                "value"
            ],
            latest_message,
        )

        Client.interact_button(
            "pls stream",
            latest_message["components"][-1]["components"][0]["custom_id"],
            latest_message,
        )

    sleep(1)

    latest_message = Client.retreive_message("pls stream")

    if (
        int(latest_message["embeds"][0]["fields"][5]["value"].replace("`", "")) > 0
        and Client.Repository.config["stream"]["ads"]
    ):
        Client.interact_button(
            "pls stream",
            latest_message["components"][0]["components"][0]["custom_id"],
            latest_message,
        )
    else:
        button = (
            randint(1, 2)
            if Client.Repository.config["stream"]["chat"]
            and Client.Repository.config["stream"]["donations"]
            else 1
            if Client.Repository.config["stream"]["chat"]
            else 2
            if Client.Repository.config["stream"]["donations"]
            else None
        )

        if button is None:
            return

        Client.interact_button(
            "pls stream",
            latest_message["components"][0]["components"][button]["custom_id"],
            latest_message,
        )

    Client.interact_button(
        "pls stream",
        latest_message["components"][-1]["components"][-1]["custom_id"],
        latest_message,
    )
