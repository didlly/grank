from datetime import datetime, timedelta
from time import sleep
from random import choice


def work(Client) -> None:
    Client.send_message("pls work")

    latest_message = Client.retreive_message("pls work")

    if "You don't currently have a job to work at." in latest_message["content"]:
        Client.send_message("pls work babysitter")

        sleep(1)

        Client.send_message("pls work")

        latest_message = Client.retreive_message("pls work")
    elif "You need to wait" in latest_message["content"]:
        time_left = latest_message["content"].split("**")[1]

        Client.log(
            "WARNING", f"Cannot work - awaiting cooldown end ({time_left} left)."
        )
    elif "Dunk the ball!" in latest_message["content"]:
        Client.log("DEBUG", "Detected dunk the ball game.")

        button_index = (
            latest_message["content"]
            .split("\n")[2]
            .split(":basketball")[0]
            .count("       ")
        )

        custom_id = latest_message["components"][0]["components"][button_index][
            "custom_id"
        ]

        Client.interact_button("pls work", custom_id, latest_message)
    elif "Color Match" in latest_message["content"]:
        Client.log("DEBUG", "Detected colour match game.")

        items = [
            [item.split(" ")[0].replace(":", ""), item.split(" ")[-1]]
            for item in latest_message["content"].lower().split("\n")[1:]
        ]

        while True:
            latest_message = Client.retreive_message("pls work")

            if len(latest_message["components"]) > 0:
                break

            sleep(2.5)

        word = latest_message["content"].split("`")[1].lower()

        for item in items:
            if item[-1] == word:
                word = item[:]

        for button in enumerate(latest_message["components"][0]["components"]):
            custom_id = None

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
    elif "Hit the ball!" in latest_message["content"]:
        Client.log("DEBUG", "Detected hit the ball game.")

        index = latest_message["content"].split("\n")[2].count("       ")

        index -= 1 if index == 2 else -1

        custom_id = latest_message["components"][0]["components"][index]["custom_id"]

        Client.interact_button("pls work", custom_id, latest_message)
    elif "Repeat Order" in latest_message["content"]:
        Client.log("DEBUG", "Detected repeat the order game.")

        words = latest_message["content"].split("\n")[1:]

        while True:
            latest_message = Client.retreive_message("pls work")

            if len(latest_message["components"]) > 0:
                break

            sleep(2.5)

        for word in words:
            for option in latest_message["components"][0]["components"]:
                if word == option["label"]:
                    Client.interact_button(
                        "pls work", option["custom_id"], latest_message
                    )
                    sleep(1)
                    break
    elif "Emoji Match" in latest_message["content"]:
        Client.log("DEBUG", "Detected emoji match game.")

        emoji = latest_message["content"].split("\n")[-1]

        while True:
            latest_message = Client.retreive_message("pls work")

            if len(latest_message["components"]) > 0:
                break

            sleep(2.5)

        custom_id = False

        for index in range(len(latest_message["components"])):
            for index2 in range(len(latest_message["componenets"][index])):
                if (
                    emoji
                    == latest_message["componenets"][index]["components"][index2][
                        "emoji"
                    ]["name"]
                ):
                    custom_id = latest_message["componenets"][index]["components"][
                        index2
                    ]["custom_id"]
                    Client.interact_button("pls work", custom_id, latest_message)
                    custom_id = True
                    break

        if not custom_id:
            Client.log("WARNING", "Failed to match the emoji. Clicking a random emoji.")
            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]
            Client.interact_button("pls work", custom_id, latest_message)
    else:
        Client.log("WARNING", "Unknown `pls work` game. Clicking a random button.")

        if len(latest_message["components"]) > 0:
            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]
        else:
            while True:
                latest_message = Client.retreive_message("pls work")

                if len(latest_message["components"]) > 0:
                    break

                sleep(2.5)

            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]

        Client.interact_button("pls work", custom_id, latest_message)
