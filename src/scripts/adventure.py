from time import sleep
from random import choice


def adventure(Client) -> None:
    Client.send_message("pls adv")

    latest_message = Client.retreive_message("pls adv")

    if "description" in latest_message["embeds"][0].keys():
        if (
            "You reached the end of your adventure!"
            in latest_message["embeds"][0]["description"]
        ):
            Client.log("DEBUG", "Adventure has ended.")

            sleep(1)

            latest_message = Client.retreive_message("pls adv")

            adventure = latest_message["embeds"][0]["fields"][0]["value"]

            backpack = latest_message["embeds"][0]["fields"][3].split(":")
            backpack = ", ".join(
                backpack[index].lower() for index in range(1, len(backpack), 2)
            )

            found = latest_message["embeds"][0]["fields"][5].split(":")
            found = ", ".join(found[index].lower() for index in range(1, len(found), 2))

            try:
                coins = int(
                    "".join(
                        filter(
                            str.isdigit,
                            latest_message["embeds"][0]["fields"][6],
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

            sleep(1)

            Client.send_message("pls adv")

            latest_message = Client.retreive_message("pls adv")
        elif (
            "You can interact with the adventure again"
            in latest_message["embeds"][0]["description"]
        ):
            Client.log(
                "WARNING", "Cannot interact with adventure yet - awaiting cooldown end."
            )
            return

    if "author" in latest_message["embeds"][0].keys():
        if "Choose an Adventure" in latest_message["embeds"][0]["author"]["name"]:
            Client.log("DEBUG", "Starting new adventure.")

            if "footer" in latest_message["embeds"][0].keys():
                if Client.Repository.config["logging"]["debug"]:
                    Client.log(
                        "DEBUG",
                        "User does not have item `adventure ticket`. Buying adventure ticket now.",
                    )

                if (
                    Client.Repository.config["auto buy"]
                    and Client.Repository.config["auto buy"]["adventure ticket"]
                ):
                    from scripts.buy import buy

                    custom_id = latest_message["components"][-1]["components"][-1][
                        "custom_id"
                    ]

                    Client.interact_button("pls adv", custom_id, latest_message)

                    sleep(1)

                    output = buy(Client, "adventure ticket")

                    if not output:
                        return

                    sleep(1)

                    Client.send_message("pls adv")

                    latest_message = Client.retreive_message("pls adv")
                elif Client.Repository.config["logging"]["warning"]:
                    Client.log(
                        "WARNING",
                        f"An adventure ticket is required for the command `pls adv`. However, since {'auto buy is off for advenure tickets,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
                    )
                    return

            custom_id = latest_message["components"][1]["components"][0]["custom_id"]

            Client.interact_button("pls adv", custom_id, latest_message)

            sleep(1)

            latest_message = Client.retreive_message("pls adv")

            custom_id = latest_message["components"][-1]["components"][1]["custom_id"]

            Client.interact_button("pls adv", custom_id, latest_message)

            sleep(1)

            custom_id = latest_message["components"][-1]["components"][0]["custom_id"]

            Client.interact_button("pls adv", custom_id, latest_message)

            sleep(1)

            latest_message = Client.retreive_message("pls adv")

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
            "DEBUG", "Strange looking object adventure phase. Choosing `Ignore` option."
        )

        custom_id = latest_message["components"][0]["components"][-1]["custom_id"]
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
        Client.log("DEBUG", "Alien abduction adventure. Choosing `Flee` option.")

        custom_id = latest_message["components"][0]["components"][-1]["custom_id"]
    elif (
        "You uh, just came across a pair of Odd Eyes floating around"
        in latest_message["embeds"][0]["description"]
    ):

        Client.log("DEBUG", "Odd eye adventure phase. Choosing `Flee` option.")
        custom_id = latest_message["components"][0]["components"][1]["custom_id"]
    else:
        Client.log(
            "WARNING", "Unknown `pls adventure` phase. Clicking a random button."
        )

        custom_id = choice(latest_message["components"][0]["components"])["custom_id"]

    Client.interact_button("pls adv", custom_id, latest_message)
