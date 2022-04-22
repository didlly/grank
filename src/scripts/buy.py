def buy(Client, item: str) -> None:
    """Buys an item

    Required item(s): None

    Args:
            Client (class): The Client for the user.
            item (str): The item to be bought.

    Returns:
            bought (bool): Boolean dictating whether the item was bought or not.
    """

    Client.send_message(f"pls buy {item}")

    latest_message = Client.retreive_message(f"pls buy {item}")

    if latest_message["content"] in [
        "your wallet is short on cash, go withdraw some BANK money to make this purchase",
        "Far out, you don't have enough money in your wallet or your bank to buy that much!!",
    ]:
        from scripts.balance import balance

        latest_message = balance(Client)

        bank = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["embeds"][0]["description"]
                    .split("\n")[1]
                    .split("/")[0]
                    .strip(),
                )
            )
        )
        wallet = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["embeds"][0]["description"].split("\n")[0],
                )
            )
        )

        if (wallet + bank) - Client.database["price"][item] > 0:
            amount = (wallet + bank) - Client.database["price"][item]

            Client.send_message(f"pls with {amount}")
            Client.send_message(f"pls buy {item}")
        else:
            if Client.config["logging"]["warning"]:
                Client.log("WARNING", f"Insufficient funds to buy a {item}.")
            return False
    elif (
        latest_message["embeds"][0]["author"]["name"].lower()
        == f"successful {item} purchase"
    ):
        if Client.config["logging"]["debug"]:
            Client.log("DEBUG", f"Successfully bought {item}.")
        return True
