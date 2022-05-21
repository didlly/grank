def dig(Client):
    Client.send_message("pls dig")

    latest_message = Client.retreive_message("pls dig")

    if (
        latest_message["content"]
        == "You don't have a shovel, you need to go buy one. I'd hate to let you dig with your bare hands."
    ):
        if Client.Repository.config["logging"]["debug"]:
            Client.log("DEBUG", "User does not have item `shovel`. Buying shovel now.")

        if (
            Client.Repository.config["auto buy"]
            and Client.Repository.config["auto buy"]["shovel"]
        ):
            from scripts.buy import buy

            buy(Client, "shovel")
            return
        elif Client.Repository.config["logging"]["warning"]:
            Client.log(
                "WARNING",
                f"A shovel is required for the command `pls dig`. However, since {'auto buy is off for shovels,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
            )
            return

    if (
        latest_message["content"]
        == "LMAO you found nothing in the ground. SUCKS TO BE YOU!"
    ):
        Client.log("DEBUG", f"Received nothing from the `pls dig` command.")
        return
    else:       
        item = (
            latest_message["content"]
            .replace("You dig in the dirt and brought back 1 ", "")
            .split("<:")[0]
            .split("<a:")[0]
        ).strip()

        Client.log("DEBUG", f"Received 1 {item.lower()} from the `pls dig` command.")
