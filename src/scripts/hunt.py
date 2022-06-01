from time import sleep

from instance.Client import Instance
from scripts.buy import buy


def hunt(Client: Instance) -> bool:
    """
    The hunt function is used to interact with the hunt command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Send the command `pls hunt`
    Client.send_message("pls hunt")

    # Get Dank Memer's response to `pls hunt`
    latest_message = Client.retreive_message("pls hunt")

    # If Dank Memer replied with the `Dodge the Fireball` game...
    if "Dodge the Fireball" in latest_message["content"]:
        Client.log("DEBUG", "Detected dodge the fireball game.")

        while True:
            # ...get the level the fireball is on
            level = (
                latest_message["content"]
                .split("\n")[1]
                .replace(latest_message["content"].split("\n")[1].strip(), "")
                .count("       ")
            )

            # If the fireball is on level 1 (i.e, it is blocking the path to the dragon)...
            if level == 1:
                # ...sleep for one second
                sleep(1)

                # Get Dank Memer's edited response
                latest_message = Client.retreive_message(
                    "pls hunt", old_latest_message=latest_message
                )

                # Continue to the next iteration of the loop
                continue

            # Interact with the `Catch` button in the middle
            Client.interact_button(
                "pls hunt",
                latest_message["components"][0]["components"][1]["custom_id"],
                latest_message,
            )

            break

    # If the account does not have a `hunting rifle`...
    if (
        latest_message["content"]
        == "You don't have a hunting rifle, you need to go buy one. You're not good enough to shoot animals with your bare hands... I hope."
    ):
        Client.log(
            "DEBUG",
            "User does not have item `hunting rifle`. Buying hunting rifle now.",
        )

        # ...if autobuy is enabled...
        if (
            Client.Repository.config["auto buy"]
            and Client.Repository.config["auto buy"]["hunting rifle"]
        ):
            # ...try and buy a `hunting rifle`
            return buy(Client, "hunting rifle")
        # Else...
        else:
            Client.log(
                "WARNING",
                f"A hunting rifle is required for the command `pls fish`. However, since {'auto buy is off for hunting rifles,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
            )
            # ...return False
            return False

    if latest_message["content"] in [
        "Imagine going into the woods to hunt something, and coming out empty handed",
        "All that time in the woods, and you couldn't catch a single thing hahaha",
        "You might be the only hunter in the world to never hit anything, just like this time",
        "You went hunting the woods and brought back literally nothing lol",
    ]:
        Client.log("DEBUG", f"Found nothing from the `pls hunt` command.")
    # If an item was gained...
    else:
        # ...get the item gained
        item = (
            latest_message["content"]
            .replace("You went hunting and brought back a ", "")
            .split("<:")[0]
            .split("<a:")[0]
        ).strip()

        Client.log("DEBUG", f"Received 1 {item.lower()} from the `pls hunt` command.")

        # Update the items gained
        Client._update_items("pls hunt", item)

    return True
