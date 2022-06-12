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

    Client.send_message("pls dig")

    latest_message = Client.retreive_message("pls dig")

    if (
        latest_message["content"]
        == "You don't have a shovel, you need to go buy one. I'd hate to let you dig with your bare hands."
    ):
        Client.log("DEBUG", "Account does not have item `shovel`. Buying shovel now.")

        if (
            Client.Repository.config["auto buy"]
            and Client.Repository.config["auto buy"]["shovel"]
        ):
            return buy(Client, "shovel")
        else:
            Client.log(
                "WARNING",
                f"A shovel is required for the command `pls dig`. However, since {'auto buy is off for shovels,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
            )
            return False

    if (
        latest_message["content"]
        == "LMAO you found nothing in the ground. SUCKS TO BE YOU!"
    ):
        Client.log("DEBUG", f"Received nothing from the `pls dig` command.")
    else:
        item = (
            latest_message["content"]
            .replace("You dig in the dirt and brought back 1 ", "")
            .split("<:")[0]
            .split("<a:")[0]
        ).strip()

        Client.log("DEBUG", f"Received 1 {item.lower()} from the `pls dig` command.")

        Client._update_items("pls dig", item)

    return True
