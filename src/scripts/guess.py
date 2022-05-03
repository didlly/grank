from random import randint


def guess(Client) -> None:
    Client.send_message("pls guess")

    latest_message = Client.retreive_message("pls guess")

    Client.send_message("10")

    latest_message = Client.retreive_message("10")

    if (
        latest_message["content"]
        == "not this time, `3` attempts left and `2` hints left."
    ):
        Client.send_message("hint")

        latest_message = Client.retreive_message("hint")

        if (
            latest_message["content"]
            == "Your last number (**10**) was too low\nYou've got `3` attempts left and `1` hint left."
        ):
            Client.send_message("15")

            latest_message = Client.retreive_message("15")

            if (
                latest_message["content"]
                == "not this time, `2` attempts left and `1` hint left."
            ):
                Client.send_message("hint")

                latest_message = Client.retreive_message("hint")

                if (
                    latest_message["content"]
                    == "Your last number (**15**) was too low\nYou've got `2` attempts left and `0` hints left."
                ):
                    num = randint(16, 20)

                    Client.send_message(num)

                    latest_message = Client.retreive_message(num)

                    if (
                        latest_message["content"]
                        == "not this time, `1` attempt left and `0` hints left."
                    ):
                        num = randint(16, 20)

                        Client.send_message(num)

                        return
                elif (
                    latest_message["content"]
                    == "Your last number (**15**) was too high\nYou've got `2` attempts left and `0` hints left."
                ):
                    num = randint(11, 14)

                    Client.send_message(num)

                    latest_message = Client.retreive_message(num)

                    if (
                        latest_message["content"]
                        == "not this time, `1` attempt left and `0` hints left."
                    ):
                        num = randint(11, 14)

                        Client.send_message(num)

                        return

        else:
            Client.send_message("5")

            latest_message = Client.retreive_message("5")

            if (
                latest_message["content"]
                == "not this time, `2` attempts left and `1` hint left."
            ):
                Client.send_message("hint")

                latest_message = Client.retreive_message("hint")

                if (
                    latest_message["content"]
                    == "Your last number (**5**) was too low\nYou've got `2` attempts left and `0` hints left."
                ):
                    num = randint(6, 9)

                    Client.send_message(num)

                    latest_message = Client.retreive_message(num)

                    if (
                        latest_message["content"]
                        == "not this time, `1` attempt left and `0` hints left."
                    ):
                        num = randint(6, 9)

                        Client.send_message(num)

                        return
                elif (
                    latest_message["content"]
                    == "Your last number (**5**) was too high\nYou've got `2` attempts left and `0` hints left."
                ):
                    num = randint(1, 4)

                    Client.send_message(num)

                    latest_message = Client.retreive_message(num)

                    if (
                        latest_message["content"]
                        == "not this time, `1` attempt left and `0` hints left."
                    ):
                        num = randint(1, 4)

                        Client.send_message(num)

                        return
