from random import randint

from instance.Client import Instance


def blackjack(Client: Instance) -> bool:
    """
    The blakjack function is used to interact with the blackjack command.

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    amount = (
        randint(
            Client.Repository.config["blackjack"]["minimum"],
            Client.Repository.config["blackjack"]["maximum"],
        )
        if Client.Repository.config["blackjack"]["random"]
        else Client.Repository.config["blackjack"]["amount"]
    )

    Client.send_message(f"pls blackjack {amount}")

    latest_message = Client.retreive_message(f"pls blackjack {amount}")

    if (
        "coins, dont try and lie to me hoe." in latest_message["content"]
        or "You have no coins in your wallet to gamble with lol."
        in latest_message["content"]
    ):
        Client.log(
            "WARNING",
            f"Insufficient funds to run the command `pls bj {amount}`. Aborting command.",
        )
        return False

    while True:
        if "description" in latest_message["embeds"][0]:
            if (
                "You lost" in latest_message["embeds"][0]["description"]
                or "You didn't" in latest_message["embeds"][0]["description"]
            ):
                Client.log(
                    "DEBUG", f"Lost {amount} through the `pls blackjack` command."
                )
                return True
            elif "You won" in latest_message["embeds"][0]["description"]:
                try:
                    coins = int(
                        "".join(
                            filter(
                                str.isdigit,
                                latest_message["embeds"][0]["description"].split("**")[
                                    4
                                ],
                            )
                        )
                    )
                except Exception:
                    coins = "no"

                Client.log(
                    "DEBUG",
                    f"Won {coins} coin{'' if coins == 1 else 's'} from the `pls blackjack` command.",
                )
                Client._update_coins("pls blackjack", coins)

                return True
            elif "hasn't changed" in latest_message["embeds"][0]["description"]:
                Client.log(
                    "DEBUG", "Tied with the dealer in the `pls blackjack` command."
                )
                return True

        total = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["embeds"][0]["fields"][0]["value"].split("\n")[-1],
                )
            )
        )

        if total < 17:
            Client.interact_button(
                f"pls bj {amount}",
                latest_message["components"][0]["components"][0]["custom_id"],
                latest_message,
            )
        else:
            Client.interact_button(
                f"pls bj {amount}",
                latest_message["components"][0]["components"][1]["custom_id"],
                latest_message,
            )
            break

        latest_message = Client.retreive_message(
            f"pls blackjack {amount}", old_latest_message=latest_message
        )
