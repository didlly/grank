from random import choice
from time import sleep

from instance.Client import Instance


def work(Client: Instance) -> bool:
    """
    The work function is used to interact with the work command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    Client.send_message("pls work")

    latest_message = Client.retreive_message("pls work")

    if "You don't currently have a job to work at" in latest_message["content"]:
        Client.send_message("pls work babysitter")

        Client.send_message("pls work")

        latest_message = Client.retreive_message(
            "pls work", old_latest_message=latest_message
        )
    elif "boss was tired" in latest_message["content"]:
        Client.log("WARNING", "Fired from job.")

        return False
    elif "you were fired" in latest_message["content"]:
        Client.log("WARNING", "Awaiting cooldown to join new job.")

        return False
    elif "You need to wait" in latest_message["content"]:
        time_left = latest_message["content"].split("**")[1]

        Client.log(
            "WARNING", f"Cannot work - awaiting cooldown end ({time_left} left)."
        )

        return False
    elif "deserve a fat promotion" in latest_message["content"]:
        promotion = latest_message["content"].split("\n")[1].split("`")[-2]

        Client.log("DEBUG", f"Got promoted in the `pls work` command - {promotion}.")

        Client.send_message("pls work")

        latest_message = Client.retreive_message(
            "pls work", old_latest_message=latest_message
        )

    if "Dunk the ball" in latest_message["content"]:
        Client.log("DEBUG", "Detected dunk the ball game.")

        level = (
            latest_message["content"]
            .split("\n")[2]
            .split(":basketball")[0]
            .count("       ")
        )

        custom_id = latest_message["components"][0]["components"][level]["custom_id"]

        Client.interact_button("pls work", custom_id, latest_message)

    elif "Color Match" in latest_message["content"]:
        Client.log("DEBUG", "Detected colour match game.")

        items = [
            [item.split(" ")[0].replace(":", ""), item.split(" ")[-1]]
            for item in latest_message["content"].lower().split("\n")[1:]
        ]

        while True:
            latest_message = Client.retreive_message(
                "pls work", old_latest_message=latest_message
            )

            if len(latest_message["components"]) > 0:
                break

            sleep(2.5)

        word = latest_message["content"].split("`")[1].lower()

        for item in items:
            if item[-1] == word:
                word = item[0]
                break

        custom_id = None

        for button in latest_message["components"][0]["components"]:
            if button["label"] == word:
                custom_id = button["custom_id"]

                break

        if custom_id is None:
            Client.log(
                "WARNING",
                "Failed to get answer to the colour match game. Choosing a random button.",
            )

            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]

        Client.interact_button("pls trivia", custom_id, latest_message)
    elif "Hit the ball" in latest_message["content"]:
        Client.log("DEBUG", "Detected hit the ball game.")

        level = latest_message["content"].split("\n")[2].count("       ")

        level -= 1 if level == 2 else -1

        Client.interact_button(
            "pls work",
            latest_message["components"][0]["components"][level]["custom_id"],
            latest_message,
        )
    elif "Repeat Order" in latest_message["content"]:
        Client.log("DEBUG", "Detected repeat the order game.")

        words = [
            word.replace("`", "") for word in latest_message["content"].split("\n")[1:]
        ]

        while True:
            latest_message = Client.retreive_message(
                "pls work", old_latest_message=latest_message
            )

            if len(latest_message["components"]) > 0:
                break

            sleep(2.5)

        for word in words:
            for button in latest_message["components"][0]["components"]:
                if button["label"] == word:
                    Client.interact_button(
                        "pls work", button["custom_id"], latest_message
                    )

                    sleep(0.5)

                    break

    elif "Emoji Match" in latest_message["content"]:
        Client.log("DEBUG", "Detected emoji match game.")

        emoji = latest_message["content"].split("\n")[-1]

        while True:
            latest_message = Client.retreive_message(
                "pls work", old_latest_message=latest_message
            )

            if len(latest_message["components"]) > 0:
                break

            sleep(2.5)

        custom_id = None

        for button_row in latest_message["components"]:
            for button in button_row["components"]:
                if emoji == button["emoji"]["name"]:
                    custom_id = button["custom_id"]

                    Client.interact_button("pls work", custom_id, latest_message)

                    break

            if custom_id is not None:
                break

        if custom_id is None:
            Client.log("WARNING", "Failed to match the emoji. Clicking a random emoji.")

            Client.interact_button(
                "pls work",
                choice(latest_message["components"][0]["components"])["custom_id"],
                latest_message,
            )
    else:
        Client.log("WARNING", "Unknown `pls work` game. Clicking a random button.")
        print(f"\n\nIMPORTANT\n{latest_message}\n\n")
        if len(latest_message["components"]) > 0:
            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]
        else:
            for _ in range(1, 6):
                latest_message = Client.retreive_message(
                    "pls work", old_latest_message=latest_message
                )

                if len(latest_message["components"]) > 0:
                    break

                sleep(2.5)

            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]

        Client.interact_button("pls work", custom_id, latest_message)

    return True
