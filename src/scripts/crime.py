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

    # If the crime setting is random...
    if Client.Repository.config["crime"]["random"]:
        # ...choose a random button to interact with
        custom_id = choice(latest_message["components"][0]["components"])["custom_id"]
    # Else...
    else:
        # Get a list of all the possible places
        places = [button["label"].lower().replace("'", "") for button in latest_message["components"][0]["components"]]
        
        # Initialize custom_id as None
        custom_id = None
        
        # For each key in the list of preferred crime places...
        for key in Client.Repository.config["crime"]["preferences"]:
            # If the key is not enabled...
            if not Client.Repository.config["crime"]["preferences"][key]:
                # ...continue to the next iteration of the for loop
                continue
            
            # For each place that can be chosen...
            for index, place in enumerate(places):
                # ...if the key, in lowercase, is in the place that can be chosen...
                if key.lower() in place:
                    # Choose that place to interact with
                    custom_id = latest_message["components"][0]["components"][index]["custom_id"]
                    
                    # Break out of the places for loop
                    break
                
            # If a button has been chosen...
            if custom_id is not None:
                # ...break out of the keys for loop
                break
            
        # If a button hasn't been chosen...
        if custom_id is None:
            # Choose a random button to interact with
            custom_id = choice(latest_message["components"][0]["components"])["custom_id"]

    # Interact with the button
    Client.interact_button(
        "pls crime",
        custom_id,
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
