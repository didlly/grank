from random import choice

from instance.Client import Instance
from utils.Shared import data


def trivia(Client: Instance) -> bool:
    """
    The trivia function is used to interact with the trivia command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Send the command `pls trivia`
    Client.send_message("pls trivia")

    # Get Dank Memer's response to `pls trivia`
    latest_message = Client.retreive_message("pls trivia")

    # If the wrong latest message was retreived...
    if "description" not in latest_message["embeds"][0].keys():
        # ...get the correct latest message
        latest_message = Client.fallback_retreive_message("pls trivia")
    elif "seconds to answer" not in latest_message["embeds"][0]["description"]:
        # ...get the correct latest message
        latest_message = Client.fallback_retreive_message("pls trivia")

    try:
        # Get the answer to the triva question from the database
        answer = data["trivia"][
            latest_message["embeds"][0]["description"]
            .split("\n")[0]
            .replace("*", "")
            .replace('"', "&quot;")
        ].replace("&quot;", '"')
    except KeyError:
        # If a KeyError is raised (i.e, the trivia question isn't in the database), it will be caught here and the answer will be set to Nonw
        answer = None

    # If answer is None...
    if answer is None:
        Client.log(
            "WARNING",
            f"Unknown trivia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Answers: `{latest_message['components'][0]['components']}`.",
        )

        # ...choose a random button to interact with
        custom_id = choice(latest_message["components"][0]["components"])["custom_id"]
    # Else...
    else:
        # Initialize custom_id as None
        custom_id = None

        # For each button in Dank Memer's response...
        for button in latest_message["components"][0]["components"]:
            # ...if the button's label is the same as the question's answer...
            if button["label"] == answer:
                # ...choose that button as the button to interact with
                custom_id = button["custom_id"]

                # Break out of the for loop
                break

        # If custom_id is None (i.e, the correct answer in the database was not found in Dank Memers response)...
        if custom_id is None:
            Client.log(
                "WARNING",
                f"Unknown answer to known trivia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Answers: `{latest_message['components'][0]['components']}`.",
            )

            # ...choose a random button to interact with
            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]

    # Interact with the button
    Client.interact_button("pls trivia", custom_id, latest_message)

    # Get Dank Memer's edited message
    latest_message = Client.retreive_message(
        "pls trivia", old_latest_message=latest_message
    )

    try:
        # Try and get the coins gained from the command
        coins = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["content"],
                )
            )
        )
    except Exception:
        # If an Exception is raised, it will be caught here and the coins gained will be set to 0
        coins = 0

    Client.log(
        "DEBUG",
        f"Received {coins} coin{'' if coins == 1 else 's'} from the `pls trivia` command.",
    )

    # Update the coins gained
    Client._update_coins("pls trivia", coins)

    return True
