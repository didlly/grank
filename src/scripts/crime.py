from random import choice

from instance.Client import Instance


def crime(Client: Instance) -> bool:
    """
    The crime function is used to interact with the crime command.

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Send the command `pls crime`
    Client.send_message("pls crime")

    # Get Dank Memer's response to `pls crime`
    latest_message = Client.retreive_message("pls crime")

    # If the wrong latest message was retreived...
    if "What crime do you want to commit" not in latest_message["content"]:
        # ...get the correct latest message
        latest_message = Client.fallback_retreive_message("pls crime")

    # Interact with a random button
    Client.interact_button(
        "pls crime",
        choice(latest_message["components"][0]["components"])["custom_id"],
        latest_message,
    )

    # Get Dank Memer's edited response
    latest_message = Client.retreive_message(
        "pls crime", old_latest_message=latest_message
    )

    # Remove the horseshoe emoji from Dank Memer's response
    latest_message["embeds"][0]["description"] = latest_message["embeds"][0][
        "description"
    ].replace(" <:horseshoe:813911522975678476>", "")

    try:
        # Try and get the coins gained from the command
        coins = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["embeds"][0]["description"].split("\n")[0],
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
        f"Received {coins} coin{'' if coins == 1 else 's'} &{' an' if item[0] in ['a', 'e', 'i', 'o', 'u'] else '' if item == 'no items' else ' a'} {item} from the `pls crime` command.",
    )

    # Update the coins gained
    Client._update_coins("pls crime", coins)

    # Update the items gained
    Client._update_items("pls crime", item)

    return True
