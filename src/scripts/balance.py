from instance.Client import Instance


def balance(Client: Instance) -> tuple:
    """
    The balance function returns the balance of the account associated with the Client.

    Args:
        Client (Instance): The Discord client

    Returns:
        The amount of money in the bank & wallet of the account
    """

    Client.send_message("pls bal")

    latest_message = Client.retreive_message("pls bal")

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

    return bank, wallet
