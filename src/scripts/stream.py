from random import choice, randint

from instance.Client import Instance
from scripts.buy import buy
from scripts.item import has_item


def stream(Client: Instance) -> bool:
    """
    The stream function is used to interact with the stream command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    bought_mouse, bought_keyboard = [True] * 2

    Client.send_message("pls stream")

    latest_message = Client.retreive_message("pls stream")

    if "You were inactive" in latest_message["content"]:
        Client.log("WARNING", "Stream ended due to inactivity. Re-starting stream.")

        latest_message = Client.retreive_message(
            "pls stream", old_latest_message=latest_message
        )

    if "description" in latest_message["embeds"][0]:
        if "keyboard" in latest_message["embeds"][0]["description"].lower():
            if not has_item(Client, "keyboard"):
                Client.log(
                    "DEBUG",
                    "Account does not have item `keyboard`. Buying keyboard now.",
                )

                if (
                    Client.Repository.config["auto buy"]
                    and Client.Repository.config["auto buy"]["keyboard"]
                ):
                    bought_keyboard = buy(Client, "keyboard")
                else:
                    Client.log(
                        "WARNING",
                        f"A keyboard is required for the command `pls stream`. However, since {'autobuy is off for keyboards,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
                    )
                    return False
        if "mouse" in latest_message["embeds"][0]["description"].lower():
            if not has_item(Client, "mouse"):
                Client.log(
                    "DEBUG", "Account does not have item `mouse`. Buying mouse now."
                )

                if (
                    Client.Repository.config["auto buy"]
                    and Client.Repository.config["auto buy"]["mouse"]
                ):
                    bought_mouse = buy(Client, "mouse")
                else:
                    Client.log(
                        "WARNING",
                        f"A mouse is required for the command `pls stream`. However, since {'autobuy is off for mouses,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
                    )
                    return False

    if not bought_mouse or not bought_keyboard:
        return False

    if len(latest_message["components"][0]["components"]) == 3:
        if "footer" in latest_message["embeds"][0]:
            if "Wait" in latest_message["embeds"][0]["footer"]["text"]:
                Client.log("DEBUG", "Cannot stream yet - awaiting cooldown end.")

                Client.interact_button(
                    "pls stream",
                    latest_message["components"][-1]["components"][-1]["custom_id"],
                    latest_message,
                )
                return False

        Client.interact_button(
            "pls stream",
            latest_message["components"][0]["components"][0]["custom_id"],
            latest_message,
        )

        latest_message = Client.retreive_message(
            "pls stream", old_latest_message=latest_message
        )

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

    latest_message = Client.retreive_message(
        "pls stream", old_latest_message=latest_message
    )

    if "fields" not in latest_message["embeds"][0]:
        latest_message = Client.fallback_retreive_message("pls stream")
    elif len(latest_message["embeds"][0]["fields"]) != 6:
        latest_message = Client.fallback_retreive_message("pls stream")

    sponsors = int(latest_message["embeds"][0]["fields"][5]["value"].replace("`", ""))

    if sponsors > 0 and Client.Repository.config["stream"]["ads"]:
        Client.interact_button(
            "pls stream",
            latest_message["components"][0]["components"][0]["custom_id"],
            latest_message,
        )
    else:
        if len(Client.Repository.config["settings"]["preferences"]["stream"]["moveset"]) == 0:
            button = (
                randint(1, 2)
                if Client.Repository.config["stream"]["chat"]
                and Client.Repository.config["stream"]["donations"]
                else 1
                if Client.Repository.config["stream"]["chat"]
                else 2
                if Client.Repository.config["stream"]["donations"] and sponsors > 0
                else None
            )
        else:
            ms_settings = Client.Repository.config["settings"]["preferences"]["stream"]
            if sponsors > 0:
                if len(Client.cache["stream"]) == len(ms_settings["moveset"]):
                    Client.cache["stream"] = []
                
                button = ms_settings["moveset"][len(Client.cache["stream"])]
                Client.cache["stream"].append(button)
            else:
                button = ms_settings["no_sponsor_move"]
                
        if button is None:
            Client.log(
                "WARNING",
                "Interacting with a random button on the `pls stream` command since no button fulfills the requirements in the config.",
            )
            button = randint(1, 2)

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

    return True
