from random import choice
from time import sleep

from instance.Client import Instance
from scripts.buy import buy


def adventure(Client: Instance) -> bool:
    """
    The adventure function is used to interact with the adventure command.
    It will start a new adventure if one is not already in progress, or it will continue an existing one.
    If the cooldown period hasn't ended, it will return False

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    Client.send_message("pls adv")

    latest_message = Client.retreive_message("pls adv")

    if "description" in latest_message["embeds"][0]:
        if (
            "You reached the end of your adventure!"
            in latest_message["embeds"][0]["description"]
        ):
            Client.log("DEBUG", "Adventure has ended.")

            latest_message = Client.retreive_message(
                "pls adv", old_latest_message=latest_message
            )

            adventure = latest_message["embeds"][0]["fields"][0]["value"]

            backpack = latest_message["embeds"][0]["fields"][2]["value"].split(":")
            backpack = ", ".join(
                backpack[index].lower() for index in range(1, len(backpack), 2)
            )

            found = latest_message["embeds"][0]["fields"][3]["value"].split(":")
            found = ", ".join(found[index].lower() for index in range(1, len(found), 2))

            try:
                coins = int(
                    "".join(
                        filter(
                            str.isdigit,
                            latest_message["embeds"][0]["fields"][4],
                        )
                    )
                )
            except Exception:
                coins = 0

            interactions = latest_message["embeds"][0]["fields"][-1]["value"]

            Client.log(
                "DEBUG",
                f"Ended adventure: `{adventure}`; Items taken: `{backpack}`; Items found: `{found}`; Coins found: `{coins}`; Amount of Interactions: `{interactions}`.",
            )

            Client._update_coins("pls adv", coins)

            for item in found.split(", "):
                Client._update_items("pls adv", item)

            sleep(1)

            Client.send_message("pls adv")

            latest_message = Client.retreive_message(
                "pls adv", old_latest_message=latest_message
            )
        elif (
            "You can interact with the adventure again"
            in latest_message["embeds"][0]["description"]
        ):
            Client.log(
                "WARNING", "Cannot interact with adventure yet - awaiting cooldown end."
            )

            return False

    if "author" in latest_message["embeds"][0]:
        if "Choose an Adventure" in latest_message["embeds"][0]["author"]["name"]:
            Client.log("DEBUG", "Starting new adventure.")

            if "footer" in latest_message["embeds"][0]:
                Client.log(
                    "DEBUG",
                    "Account does not have item `adventure ticket`. Buying adventure ticket now.",
                )

                if (
                    Client.Repository.config["auto buy"]
                    and Client.Repository.config["auto buy"]["adventure ticket"]
                ):
                    Client.interact_button(
                        "pls adv",
                        latest_message["components"][-1]["components"][-1]["custom_id"],
                        latest_message,
                    )

                    output = buy(Client, "adventure ticket")

                    if not output:
                        return False

                    Client.send_message("pls adv")

                    latest_message = Client.retreive_message(
                        "pls adv", old_latest_message=latest_message
                    )
                else:
                    Client.log(
                        "WARNING",
                        f"An adventure ticket is required for the command `pls adv`. However, since {'auto buy is off for advenure tickets,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
                    )

                    return False

            Client.interact_button(
                "pls adv",
                latest_message["components"][1]["components"][0]["custom_id"],
                latest_message,
            )

            latest_message = Client.retreive_message(
                "pls adv", old_latest_message=latest_message
            )

            Client.interact_button(
                "pls adv",
                latest_message["components"][-1]["components"][1]["custom_id"],
                latest_message,
            )

            Client.interact_button(
                "pls adv",
                latest_message["components"][-1]["components"][0]["custom_id"],
                latest_message,
            )

            latest_message = Client.retreive_message(
                "pls adv", old_latest_message=latest_message
            )
    if len(latest_message["components"][0]["components"]) == 1:
        Client.log("DEBUG", "Uneventful adventure phase.")

        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "You ran out of fuel! What next?" in latest_message["embeds"][0]["description"]
    ):
        Client.log(
            "DEBUG", "Fuel loss adventure phase. Choosing `Search a planet` option."
        )

        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "You accidentally bumped into the Webb Telescope."
        in latest_message["embeds"][0]["description"]
    ):
        Client.log(
            "DEBUG", "Webb telescope adventure phase. Choosing `Try and fix it` option."
        )

        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "You found a strange looking object. What do you do?"
        in latest_message["embeds"][0]["description"]
    ):
        Client.log(
            "DEBUG",
            "Strange looking object adventure phase. Choosing `Inspect` option.",
        )

        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "A friendly alien approached you slowly."
        in latest_message["embeds"][0]["description"]
    ):
        Client.log("DEBUG", "Friendly alien adventure phase. Choosing `Talk` option.")

        custom_id = latest_message["components"][0]["components"][1]["custom_id"]
    elif (
        "You got abducted by a group of aliens,"
        in latest_message["embeds"][0]["description"]
    ):
        Client.log(
            "DEBUG", "Alien abduction adventure. Choosing `Sit back and enjoy` option."
        )

        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "You uh, just came across a pair of Odd Eyes floating around"
        in latest_message["embeds"][0]["description"]
    ):
        Client.log("DEBUG", "Odd eye adventure phase. Choosing `Collect` option.")

        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "Oh my god even in space you cannot escape it"
        in latest_message["embeds"][0]["description"]
    ):
        Client.log("DEBUG", "Rick roll adventure phase. Choosing `up` option.")

        custom_id = latest_message["components"][0]["components"][-1]["custom_id"]
    elif (
        "You encountered someone named Dank Sidious, what do you do?"
        in latest_message["embeds"][0]["description"]
    ):
        Client.log("DEBUG", "Dank Sidious adventure phase. Choosing `Do it` option.")

        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    else:
        Client.log(
            "WARNING", "Unknown `pls adventure` phase. Clicking a random button."
        )

        custom_id = choice(latest_message["components"][0]["components"])["custom_id"]

    Client.interact_button("pls adv", custom_id, latest_message)

    return True
