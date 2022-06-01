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

    # Send the command `pls work`
    Client.send_message("pls work")

    # Get Dank Memer's response to `pls work`
    latest_message = Client.retreive_message("pls work")

    # If the account doesn't have a job...
    if "You don't currently have a job to work at" in latest_message["content"]:
        # Send the command `pls work babysitter`
        Client.send_message("pls work babysitter")

        # Send the command `pls work`
        Client.send_message("pls work")

        # Get Dank Memer's response to `pls work`
        latest_message = Client.retreive_message(
            "pls work", old_latest_message=latest_message
        )
    # Else if the account was fired...
    elif "boss was tired" in latest_message["content"]:
        Client.log("WARNING", "Fired from job.")

        # ...return False
        return False
    # Else if awaiting cooldown to join new job...
    elif "you were fired" in latest_message["content"]:
        Client.log("WARNING", "Awaiting cooldown to join new job.")

        # ...return False
        return False
    # Else if awaiting cooldown to work...
    elif "You need to wait" in latest_message["content"]:
        # ...get the time left till the account can work
        time_left = latest_message["content"].split("**")[1]

        Client.log(
            "WARNING", f"Cannot work - awaiting cooldown end ({time_left} left)."
        )

        return False
    # Else if the account was promoted...
    elif "deserve a fat promotion" in latest_message["content"]:
        # ...get the old pay & promotion amount
        promotion = latest_message["content"].split("\n")[1].split("`")[-2]

        Client.log("DEBUG", f"Got promoted in the `pls work` command - {promotion}.")

        # Send the command `pls work`
        Client.send_message("pls work")

        # Get Dank Memer's response to `pls work`
        latest_message = Client.retreive_message(
            "pls work", old_latest_message=latest_message
        )

    # If Dank Memer replied with the `Dunk The ball`` minigame...
    if "Dunk the ball" in latest_message["content"]:
        Client.log("DEBUG", "Detected dunk the ball game.")

        # ...get the index of the button under the ball
        level = (
            latest_message["content"]
            .split("\n")[2]
            .split(":basketball")[0]
            .count("       ")
        )

        # Interact with the `Catch` button
        custom_id = latest_message["components"][0]["components"][level]["custom_id"]

        Client.interact_button("pls work", custom_id, latest_message)

    # Else if Dank Memer replied with the `Colour Match` minigame...
    elif "Color Match" in latest_message["content"]:
        Client.log("DEBUG", "Detected colour match game.")

        # ...get the colours and the word next to them
        items = [
            [item.split(" ")[0].replace(":", ""), item.split(" ")[-1]]
            for item in latest_message["content"].lower().split("\n")[1:]
        ]

        while True:
            # Get Dank Memer's edited message
            latest_message = Client.retreive_message(
                "pls work", old_latest_message=latest_message
            )

            # If Dank Memer's response has buttons...
            if len(latest_message["components"]) > 0:
                # ...break out of the loop
                break

            # Sleep for 2.5 seconds
            sleep(2.5)

        # Get the word to be matched
        word = latest_message["content"].split("`")[1].lower()

        # For each word...
        for item in items:
            # ...if the word to be matched is found...
            if item[-1] == word:
                # ...set word to the colour next to the word
                word = item[0]
                break

        # Initialize custom_id as None
        custom_id = None

        # For each button in Dank Memer's response...
        for button in latest_message["components"][0]["components"]:
            # ...if the button's label is the same as the word's colour...
            if button["label"] == word:
                # ...choose that button as the button to interact with
                custom_id = button["custom_id"]

                # Break out of the for loop
                break

        # If the program failed to match the labels on the buttons to the word's colour...
        if custom_id is None:
            Client.log(
                "WARNING",
                "Failed to get answer to the colour match game. Choosing a random button.",
            )

            # ...choose a random button to interact with
            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]

        # Interact with the button
        Client.interact_button("pls trivia", custom_id, latest_message)
    # Else if Dank Memer replied with the `Hit the ball` minigame...
    elif "Hit the ball" in latest_message["content"]:
        Client.log("DEBUG", "Detected hit the ball game.")

        # ...get the index of the goalkeeper
        level = latest_message["content"].split("\n")[2].count("       ")

        # Minus 1 from the level if the level equals 2 else add 1
        level -= 1 if level == 2 else -1

        # Interact with the button
        Client.interact_button(
            "pls work",
            latest_message["components"][0]["components"][level]["custom_id"],
            latest_message,
        )
    # Else if Dank Memer replied with the `Repeat Order` minigame...
    elif "Repeat Order" in latest_message["content"]:
        Client.log("DEBUG", "Detected repeat the order game.")

        # ...get the words
        words = [
            word.replace("`", "") for word in latest_message["content"].split("\n")[1:]
        ]

        while True:
            # Get Dank Memer's edited message
            latest_message = Client.retreive_message(
                "pls work", old_latest_message=latest_message
            )

            # If Dank Memer's response has buttons...
            if len(latest_message["components"]) > 0:
                # ...break out of the loop
                break

            # Sleep for 2.5 seconds
            sleep(2.5)

        # For each word in words...
        for word in words:
            # ...for each button in Dank Memer's response...
            for button in latest_message["components"][0]["components"]:
                # ...if the button label equals the word...
                if button["label"] == word:
                    # ...interact with the button
                    Client.interact_button(
                        "pls work", button["custom_id"], latest_message
                    )

                    # Sleep for 1 second
                    sleep(0.5)

                    # Break out of the buttons for loop
                    break

    # Else if Dank Memer replied with the `Emoji Match` minigame
    elif "Emoji Match" in latest_message["content"]:
        Client.log("DEBUG", "Detected emoji match game.")

        # Get the emoji to be matched
        emoji = latest_message["content"].split("\n")[-1]

        while True:
            # Get Dank Memer's edited message
            latest_message = Client.retreive_message(
                "pls work", old_latest_message=latest_message
            )

            # If Dank Memer's response has buttons...
            if len(latest_message["components"]) > 0:
                # ...break out of the loop
                break

            # Sleep for 2.5 seconds
            sleep(2.5)

        # Initialize custom_id as None
        custom_id = None

        # For each row of buttons...
        for button_row in latest_message["components"]:
            # ...for each button in that row...
            for button in button_row["components"]:
                # ...if that button's emoji is the emoji to be matched...
                if emoji == button["emoji"]["name"]:
                    # ...choose that button was the button to interact with
                    custom_id = button["custom_id"]

                    # Interact with the button
                    Client.interact_button("pls work", custom_id, latest_message)

                    # Break out of the button for loop
                    break

            # If custom_id doesn't equal None
            if custom_id is not None:
                # Break out of the button_row for loop
                break

        # If the emoji wasn't matched...
        if custom_id is None:
            Client.log("WARNING", "Failed to match the emoji. Clicking a random emoji.")

            # ...interact with a random button
            Client.interact_button(
                "pls work",
                choice(latest_message["components"][0]["components"])["custom_id"],
                latest_message,
            )
    # Else if Dank Memer replied with an unknown minigame...
    else:
        Client.log("WARNING", "Unknown `pls work` game. Clicking a random button.")
        print(f"\n\nIMPORTANT\n{latest_message}\n\n")
        # If there are buttons to click...
        if len(latest_message["components"]) > 0:
            # ...choose a random butotn to interact with
            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]
        # Else...
        else:
            # ...try to get Dank Memer's edited message with buttons (i.e, the command could be one where you have to memorise a pattern and the buttons will only appear after a certain time)
            for _ in range(1, 6):
                # Get Dank Memer's edited message
                latest_message = Client.retreive_message(
                    "pls work", old_latest_message=latest_message
                )

                # If Dank Memer's response has buttons...
                if len(latest_message["components"]) > 0:
                    # ...break out of the loop
                    break

                # Sleep for 2.5 seconds
                sleep(2.5)

            # Choose a random button to interact with
            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]

        # Interact with the random button
        Client.interact_button("pls work", custom_id, latest_message)

    return True
