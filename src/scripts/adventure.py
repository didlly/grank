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

    # Send the command `pls adv`
    Client.send_message("pls adv")

    # Get Dank Memer's response to `pls adv`
    latest_message = Client.retreive_message("pls adv")

    # If the response has a `description` section in the embed...
    if "description" in latest_message["embeds"][0].keys():
        # ...if the adventure has ended
        if (
            "You reached the end of your adventure!"
            in latest_message["embeds"][0]["description"]
        ):
            Client.log("DEBUG", "Adventure has ended.")

            # ...get Dank Memer's latest message
            latest_message = Client.retreive_message(
                "pls adv", old_latest_message=latest_message
            )

            # Get the adventure that has ended
            adventure = latest_message["embeds"][0]["fields"][0]["value"]

            # Get the items taken on the adventure
            backpack = latest_message["embeds"][0]["fields"][2]["value"].split(":")
            backpack = ", ".join(
                backpack[index].lower() for index in range(1, len(backpack), 2)
            )

            # Get the items found during the adventure
            found = latest_message["embeds"][0]["fields"][3]["value"].split(":")
            found = ", ".join(found[index].lower() for index in range(1, len(found), 2))

            try:
                # Try and get the coins gained during the adventure
                coins = int(
                    "".join(
                        filter(
                            str.isdigit,
                            latest_message["embeds"][0]["fields"][4],
                        )
                    )
                )
            except Exception:
                # If an Exception is raised, it will be caught here and the coins gained will be set to 0
                coins = 0

            # Get the amount of interactions completed during the adventure
            interactions = latest_message["embeds"][0]["fields"][-1]["value"]

            Client.log(
                "DEBUG",
                f"Ended adventure: `{adventure}`; Items taken: `{backpack}`; Items found: `{found}`; Coins found: `{coins}`; Amount of Interactions: `{interactions}`.",
            )

            # Update the coins gained
            Client._update_coins("pls adv", coins)
            
            # For each item gained...
            for item in found.split(", "):
                # ...update the items gained
                Client._update_items("pls adv", item)

            sleep(1)

            # Send the command `pls adv`
            Client.send_message("pls adv")

            # Get Dank Memer's response to `pls adv`
            latest_message = Client.retreive_message(
                "pls adv", old_latest_message=latest_message
            )
        # ...else if the cooldown period hasn't ended...
        elif (
            "You can interact with the adventure again"
            in latest_message["embeds"][0]["description"]
        ):
            Client.log(
                "WARNING", "Cannot interact with adventure yet - awaiting cooldown end."
            )

            # ...return False
            return False

    # If the response has an `author` section in the embed...
    if "author" in latest_message["embeds"][0].keys():
        # ...if a new adventure has to be started...
        if "Choose an Adventure" in latest_message["embeds"][0]["author"]["name"]:
            Client.log("DEBUG", "Starting new adventure.")

            # ...if the account does not have an `adventure ticket`...
            if "footer" in latest_message["embeds"][0].keys():
                Client.log(
                    "DEBUG",
                    "Account does not have item `adventure ticket`. Buying adventure ticket now.",
                )

                # ...if autobuy is enabled...
                if (
                    Client.Repository.config["auto buy"]
                    and Client.Repository.config["auto buy"]["adventure ticket"]
                ):
                    # ...interact with the `End Interaction` button
                    Client.interact_button(
                        "pls adv",
                        latest_message["components"][-1]["components"][-1]["custom_id"],
                        latest_message,
                    )

                    # Try and buy an `adventure ticket`
                    output = buy(Client, "adventure ticket")

                    # If the adventure ticket was not bought...
                    if not output:
                        # ...return False
                        return False

                    # Send the command `pls adv`
                    Client.send_message("pls adv")

                    # Get Dank Memer's response to `pls adv`
                    latest_message = Client.retreive_message(
                        "pls adv", old_latest_message=latest_message
                    )
                # ...else...
                else:
                    Client.log(
                        "WARNING",
                        f"An adventure ticket is required for the command `pls adv`. However, since {'auto buy is off for advenure tickets,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
                    )

                    # ...return False
                    return False

            # Choose the `Start Adventure` button
            Client.interact_button(
                "pls adv",
                latest_message["components"][1]["components"][0]["custom_id"],
                latest_message,
            )

            # Get Dank Memer's edited response
            latest_message = Client.retreive_message(
                "pls adv", old_latest_message=latest_message
            )

            # Choose the `Equip all` button
            Client.interact_button(
                "pls adv",
                latest_message["components"][-1]["components"][1]["custom_id"],
                latest_message,
            )

            # Choose the `Start Adventure` button
            Client.interact_button(
                "pls adv",
                latest_message["components"][-1]["components"][0]["custom_id"],
                latest_message,
            )

            # Get Dank Memer's edited response
            latest_message = Client.retreive_message(
                "pls adv", old_latest_message=latest_message
            )
    # If there is only one button (the `End Interaction` one) on Dank Memer's response
    if len(latest_message["components"][0]["components"]) == 1:
        Client.log("DEBUG", "Uneventful adventure phase.")

        # Choose the `End Interaction` button
        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "You ran out of fuel! What next?" in latest_message["embeds"][0]["description"]
    ):
        Client.log(
            "DEBUG", "Fuel loss adventure phase. Choosing `Search a planet` option."
        )

        # Choose the `Search a planet` button
        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "You accidentally bumped into the Webb Telescope."
        in latest_message["embeds"][0]["description"]
    ):
        Client.log(
            "DEBUG", "Webb telescope adventure phase. Choosing `Try and fix it` option."
        )

        # Choose the `Try and fix it` button
        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "You found a strange looking object. What do you do?"
        in latest_message["embeds"][0]["description"]
    ):
        Client.log(
            "DEBUG",
            "Strange looking object adventure phase. Choosing `Inspect` option.",
        )

        # Choose the `Inspect` button
        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "A friendly alien approached you slowly."
        in latest_message["embeds"][0]["description"]
    ):
        Client.log("DEBUG", "Friendly alien adventure phase. Choosing `Talk` option.")

        # Choose the `Talk` button
        custom_id = latest_message["components"][0]["components"][1]["custom_id"]
    elif (
        "You got abducted by a group of aliens,"
        in latest_message["embeds"][0]["description"]
    ):
        Client.log(
            "DEBUG", "Alien abduction adventure. Choosing `Sit back and enjoy` option."
        )

        # Choose the `Sit back and enjoy` button
        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "You uh, just came across a pair of Odd Eyes floating around"
        in latest_message["embeds"][0]["description"]
    ):
        Client.log("DEBUG", "Odd eye adventure phase. Choosing `Collect` option.")

        # Choose the `Collect` button
        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    elif (
        "Oh my god even in space you cannot escape it"
        in latest_message["embeds"][0]["description"]
    ):
        Client.log("DEBUG", "Rick roll adventure phase. Choosing `up` option.")

        # Choose the `up` button
        custom_id = latest_message["components"][0]["components"][-1]["custom_id"]
    elif (
        "You encountered someone named Dank Sidious, what do you do?"
        in latest_message["embeds"][0]["description"]
    ):
        Client.log("DEBUG", "Dank Sidious adventure phase. Choosing `Do it` option.")

        # Choose the `Do it` button
        custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    else:
        Client.log(
            "WARNING", "Unknown `pls adventure` phase. Clicking a random button."
        )

        # Interacts with a random button
        custom_id = choice(latest_message["components"][0]["components"])["custom_id"]

    # Choose the button
    Client.interact_button("pls adv", custom_id, latest_message)

    return True
