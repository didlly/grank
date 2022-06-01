from random import randint

from instance.Client import Instance


def guess(Client: Instance) -> bool:
    """
    The guess function is used to interact with the guess command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    # Send the command `pls guess`
    Client.send_message("pls guess")

    # Get Dank Memer's response to `pls guess`
    latest_message = Client.retreive_message("pls guess")

    # Send the message 10
    Client.send_message("10")

    # Get Dank Memer's response to 10
    latest_message = Client.retreive_message("10", old_latest_message=latest_message)

    # If that wasn't the number...
    if (
        latest_message["content"]
        == "not this time, `3` attempts left and `2` hints left."
    ):
        # ...send the message `hint`
        Client.send_message("hint")

        # Get Dank Memer's response to `hint`
        latest_message = Client.retreive_message(
            "hint", old_latest_message=latest_message
        )

        # If 10 was too low...
        if (
            latest_message["content"]
            == "Your last number (**10**) was too low\nYou've got `3` attempts left and `1` hint left."
        ):
            # ...send the message 15
            Client.send_message("15")

            # Get Dank Memer's response to 15
            latest_message = Client.retreive_message(
                "15", old_latest_message=latest_message
            )

            # If that wasn't the number...
            if (
                latest_message["content"]
                == "not this time, `2` attempts left and `1` hint left."
            ):
                # ...send the message `hint`
                Client.send_message("hint")

                # Get Dank Memer's response to `hint`
                latest_message = Client.retreive_message(
                    "hint", old_latest_message=latest_message
                )

                # If 15 was too low...
                if (
                    latest_message["content"]
                    == "Your last number (**15**) was too low\nYou've got `2` attempts left and `0` hints left."
                ):
                    # ...send a message containing a random number between 16 & 20
                    num = randint(16, 20)

                    Client.send_message(num)

                    # Get Dank Memer's response
                    latest_message = Client.retreive_message(
                        num, old_latest_message=latest_message
                    )

                    # If that wasn't the number...
                    if (
                        latest_message["content"]
                        == "not this time, `1` attempt left and `0` hints left."
                    ):
                        num = randint(16, 20)

                        # ...send a message containing a random number between 16 & 20
                        Client.send_message(num)

                        return True
                # Elif 15 was too high...
                elif (
                    latest_message["content"]
                    == "Your last number (**15**) was too high\nYou've got `2` attempts left and `0` hints left."
                ):
                    num = randint(11, 14)

                    # ...send a message containing a random number between 11 & 14
                    Client.send_message(num)

                    # Get Dank Memer's response
                    latest_message = Client.retreive_message(
                        num, old_latest_message=latest_message
                    )

                    # If that wasn't the number...
                    if (
                        latest_message["content"]
                        == "not this time, `1` attempt left and `0` hints left."
                    ):
                        num = randint(11, 14)

                        # ...send a message containing a random number between 11 & 14
                        Client.send_message(num)

                        return True
        # Else...
        else:
            # ...send the message 5
            Client.send_message("5")

            # Get Dank Memer's response to 5
            latest_message = Client.retreive_message(
                "5", old_latest_message=latest_message
            )

            # If 5 was not the number...
            if (
                latest_message["content"]
                == "not this time, `2` attempts left and `1` hint left."
            ):
                # ...send the message `hint`
                Client.send_message("hint")

                # Get Dank Memer's response to `hint`
                latest_message = Client.retreive_message(
                    "hint", old_latest_message=latest_message
                )

                # If 5 was too low...
                if (
                    latest_message["content"]
                    == "Your last number (**5**) was too low\nYou've got `2` attempts left and `0` hints left."
                ):
                    num = randint(6, 9)

                    # ...send a message containing a random number between 6 & 9
                    Client.send_message(num)

                    # Get Dank Memer's response
                    latest_message = Client.retreive_message(
                        num, old_latest_message=latest_message
                    )

                    # If that wasn't the number...
                    if (
                        latest_message["content"]
                        == "not this time, `1` attempt left and `0` hints left."
                    ):
                        num = randint(6, 9)

                        # ...send a message containing a random number between 6 & 9
                        Client.send_message(num)

                        return True
                # Elif 5 was too high...
                elif (
                    latest_message["content"]
                    == "Your last number (**5**) was too high\nYou've got `2` attempts left and `0` hints left."
                ):
                    num = randint(1, 4)

                    # Send a message containing a random number between 1 & 4
                    Client.send_message(num)

                    # Get Dank Memer's response
                    latest_message = Client.retreive_message(
                        num, old_latest_message=latest_message
                    )

                    # If that wasn't the number...
                    if (
                        latest_message["content"]
                        == "not this time, `1` attempt left and `0` hints left."
                    ):
                        num = randint(1, 4)

                        # Send a message containing a random number between 1 & 4
                        Client.send_message(num)

                        return True

    return True
