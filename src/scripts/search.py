from random import choice

from instance.Client import Instance


def search(Client: Instance) -> bool:
    """
    The search function is used to interact with the search command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Send the command `pls search`
    Client.send_message("pls search")

    # Get Dank Memer's response to `pls search`
    latest_message = Client.retreive_message("pls search")

    # If the wrong latest message was retreived...
    if "Where do you want to search" not in latest_message["content"]:
        # ...get the correct latest message
        latest_message = Client.fallback_retreive_message("pls crime")

    # If the search setting is random...
    if Client.Repository.config["search"]["random"]:
        # ...choose a random button to interact with
        custom_id = choice(latest_message["components"][0]["components"])["custom_id"]
    # Else...
    else:
        # Get a list of all the possible places
        places = [
            button["label"].lower().replace("'", "")
            for button in latest_message["components"][0]["components"]
        ]

        # Initialize custom_id as None
        custom_id = None

        # For each key in the list of preferred search places...
        for key in Client.Repository.config["search"]["preferences"]:
            # If the key is not enabled...
            if not Client.Repository.config["search"]["preferences"][key]:
                # ...continue to the next iteration of the for loop
                continue

            # For each place that can be chosen...
            for index, place in enumerate(places):
                # ...if the key, in lowercase, is in the place that can be chosen...
                if key.lower() in place:
                    # Choose that place to interact with
                    custom_id = latest_message["components"][0]["components"][index][
                        "custom_id"
                    ]

                    # Break out of the places for loop
                    break

            # If a button has been chosen...
            if custom_id is not None:
                # ...break out of the keys for loop
                break

        # If a button hasn't been chosen...
        if custom_id is None:
            # Choose a random button to interact with
            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]

    # Interacts with the chosen button, or a random one if one hasn't been chosen
    Client.interact_button(
        "pls search",
        custom_id,
        latest_message,
    )

    # Get Dank Memer's edited response
    latest_message = Client.retreive_message(
        "pls search", old_latest_message=latest_message
    )

    # Remove the horseshoe emoji from Dank Memer's response
    latest_message["embeds"][0]["description"] = (
        latest_message["embeds"][0]["description"]
        .replace("! <:horseshoe:813911522975678476>", "")
        .replace(" <:horseshoe:813911522975678476>", "")
    )

    try:
        # Try and get the coins gained from the command
        coins = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["embeds"][0]["description"]
                    .split("\n")[0]
                    .split("https://")[0],
                )
            )
        )
    except Exception:
        # If an Exception is raised, it will be caught here and the coins gained will be set to 0
        coins = 0

    try:
        # Try and get the items gained from the command
        item = (
            latest_message["embeds"][0]["description"].split("**")[-2]
            if latest_message["embeds"][0]["description"].count("**") == 2
            else "no items"
        )
    except Exception:
        # If an Exception is raised, it will be caught here and the items gained will be set to `no items`
        item = "no items"

    Client.log(
        "DEBUG",
        f"Received {coins} coin{'' if coins == 1 else 's'} &{' an' if item[0] in ['a', 'e', 'i', 'o', 'u'] else '' if item == 'no items' else ' a'} {item} from the `pls search` command.",
    )

    # Update the coins gained
    Client._update_coins("pls search", coins)

    # Update the items gained
    Client._update_items("pls search", item)

    return True
