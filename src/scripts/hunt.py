from time import sleep


def hunt(Client) -> None:
    Client.send_message("pls hunt")

    latest_message = Client.retreive_message("pls hunt")

    if "Dodge the Fireball" in latest_message["content"]:
        if Client.Repository.config["logging"]["debug"]:
            Client.log("DEBUG", "Detected dodge the fireball game.")

        while True:
            latest_message = Client.retreive_message("pls hunt", old_latest_message=latest_message)

            level = (
                latest_message["content"]
                .split("\n")[1]
                .replace(latest_message["content"].split("\n")[1].strip(), "")
                .count("       ")
            )

            if level != 1:
                sleep(1)

                continue

            Client.interact_button(
                "pls hunt",
                latest_message["components"][0]["components"][1]["custom_id"],
                latest_message,
            )

            break

    if (
        latest_message["content"]
        == "You don't have a hunting rifle, you need to go buy one. You're not good enough to shoot animals with your bare hands... I hope."
    ):
        if Client.Repository.config["logging"]["debug"]:
            Client.log(
                "DEBUG",
                "User does not have item `hunting rifle`. Buying hunting rifle now.",
            )

        if (
            Client.Repository.config["auto buy"]
            and Client.Repository.config["auto buy"]["hunting rifle"]
        ):
            from scripts.buy import buy

            buy(Client, "hunting rifle")
            return
        elif Client.Repository.config["logging"]["warning"]:
            Client.log(
                "WARNING",
                f"A hunting rifle is required for the command `pls fish`. However, since {'auto buy is off for hunting rifles,' if Client.Repository.config['auto buy']['enabled'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
            )
            return

    if latest_message["content"] in [
        "Imagine going into the woods to hunt something, and coming out empty handed",
        "All that time in the woods, and you couldn't catch a single thing hahaha",
        "You might be the only hunter in the world to never hit anything, just like this time",
        "You went hunting the woods and brought back literally nothing lol",
    ]:
        Client.log("DEBUG", f"Found nothing from the `pls hunt` command.")
        return
    else:
        item = (
            latest_message["content"]
            .replace("You went hunting and brought back a ", "")
            .split("<:")[0]
            .split("<a:")[0]
        ).strip()

        Client.log("DEBUG", f"Received 1 {item.lower()} from the `pls hunt` command.")
