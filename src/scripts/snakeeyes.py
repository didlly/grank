from random import randint


def snakeeyes(Client) -> None:
    amount = (
        randint(
            Client.Repository.config["snakeeyes"]["minimum"],
            Client.Repository.config["snakeeyes"]["maximum"],
        )
        if Client.Repository.config["snakeeyes"]["random"]
        else Client.Repository.config["snakeeyes"]["amount"]
    )

    Client.send_message(f"pls snakeeyes {amount}")
