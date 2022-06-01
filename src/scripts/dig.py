from instance.Client import Instance
from scripts.buy import buy


def dig(Client: Instance) -> bool:
    """
    The dig function is used to interact with the dig command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Send the command `pls dig`
    Client.send_message("pls dig")

    # Get Dank Memer's response to `pls dig`
    latest_message = Client.retreive_message("pls dig")

    # If the account does not have a `shovel`...
    if (
        latest_message["content"]
        == "You don't have a shovel, you need to go buy one. I'd hate to let you dig with your bare hands."
    ):
        Client.log("DEBUG", "User does not have item `shovel`. Buying shovel now.")

        # ...if autobuy is enabled...
        if (
            Client.Repository.config["auto buy"]
            and Client.Repository.config["auto buy"]["shovel"]
        ):
            # ...try and buy a `shovel`
            return buy(Client, "shovel")
        # Else...
        else:
            Client.log(
                "WARNING",
                f"A shovel is required for the command `pls dig`. However, since {'auto buy is off for shovels,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
            )
            # ...return False
            return False

    if (
        latest_message["content"]
        == "LMAO you found nothing in the ground. SUCKS TO BE YOU!"
    ):
        Client.log("DEBUG", f"Received nothing from the `pls dig` command.")
    # If an item was gained...
    else:
        # ...get the item gained
        item = (
            latest_message["content"]
            .replace("You dig in the dirt and brought back 1 ", "")
            .split("<:")[0]
            .split("<a:")[0]
        ).strip()

        Client.log("DEBUG", f"Received 1 {item.lower()} from the `pls dig` command.")

        # Update the items gained
        Client._update_items("pls dig", item)

    return True
