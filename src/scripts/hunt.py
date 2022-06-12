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

    Client.send_message("pls hunt")

    latest_message = Client.retreive_message("pls hunt")

    if "Dodge the Fireball" in latest_message["content"]:
        Client.log("DEBUG", "Detected dodge the fireball game.")

        while True:
            level = latest_message["content"].split("\n")[2].rstrip().count("       ")

            if level == 1:
                sleep(1)

                latest_message = Client.retreive_message(
                    "pls hunt", old_latest_message=latest_message
                )

                continue

            Client.interact_button(
                "pls hunt",
                latest_message["components"][0]["components"][1]["custom_id"],
                latest_message,
            )

            return True

    if (
        latest_message["content"]
        == "You don't have a hunting rifle, you need to go buy one. You're not good enough to shoot animals with your bare hands... I hope."
    ):
        Client.log(
            "DEBUG",
            "Account does not have item `hunting rifle`. Buying hunting rifle now.",
        )

        if (
            Client.Repository.config["auto buy"]
            and Client.Repository.config["auto buy"]["hunting rifle"]
        ):
            return buy(Client, "hunting rifle")
        else:
            Client.log(
                "WARNING",
                f"A hunting rifle is required for the command `pls fish`. However, since {'auto buy is off for hunting rifles,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
            )
            return False

    if latest_message["content"] in [
        "Imagine going into the woods to hunt something, and coming out empty handed",
        "All that time in the woods, and you couldn't catch a single thing hahaha",
        "You might be the only hunter in the world to never hit anything, just like this time",
        "You went hunting the woods and brought back literally nothing lol",
    ]:
        Client.log("DEBUG", f"Found nothing from the `pls hunt` command.")
    else:
        item = (
            latest_message["content"]
            .replace("You went hunting and brought back a ", "")
            .split("<:")[0]
            .split("<a:")[0]
        ).strip()

        Client.log("DEBUG", f"Received 1 {item.lower()} from the `pls hunt` command.")

        Client._update_items("pls hunt", item)

    return True
