from instance.Client import Instance


def balance(Client: Instance) -> tuple:
    """
    The balance function returns the balance of the account associated with the Client.

    Args:
        Client (Instance): The Discord client

    Returns:
        The amount of money in the bank & wallet of the account
    """

    # Send the command `pls bal`
    Client.send_message("pls bal")

    # Gets Dank Memer's response to `pls bal`
    latest_message = Client.retreive_message("pls bal")

    # Get the amount of money in the account's bank
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

    # Get the amount of money in the account's wallet
    wallet = int(
        "".join(
            filter(
                str.isdigit,
                latest_message["embeds"][0]["description"].split("\n")[0],
            )
        )
    )

    # Returns the amount of money in the account's bank & wallet
    return bank, wallet
