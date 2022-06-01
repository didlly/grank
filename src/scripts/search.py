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

    # Initialize custom_id as None
    custom_id = None

    # For each button in the list of buttons...
    for option in latest_message["components"][0]["components"]:
        # ...try and find the best option to select

        if option["label"] == "street":
            # Gives `Golden Phalic Object` / `Rare Pepe`
            custom_id = option["custom_id"]
            break
        elif option["label"] == "dresser":
            # Gives `Bank note` / `Normie Box` / `Apple`
            custom_id = option["custom_id"]
            break
        elif option["label"] == "mailbox":
            # Gives `Normie Box` / `Bank note`
            custom_id = option["custom_id"]
            break
        elif option["label"] == "bushes":
            # Gives ``Normie Box`
            custom_id = option["custom_id"]
            break
        elif option["label"] == "bank":
            # Gives `Bank note`
            custom_id = option["custom_id"]
            break
        elif option["label"] == "laundromat":
            # Gives `Tidepod`
            custom_id = option["custom_id"]
            break
        elif option["label"] == "hospital":
            # Gives `Life Saver` / `Apple`
            custom_id = option["custom_id"]
            break
        elif option["label"] == "laundromat":
            # Gives `Tidepod`
            custom_id = option["custom_id"]
            break

    # Interacts with the chosen button, or a random one if one hasn't been chosen
    Client.interact_button(
        "pls search",
        choice(latest_message["components"][0]["components"])["custom_id"]
        if custom_id is None
        else custom_id,
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
