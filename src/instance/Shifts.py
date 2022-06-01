from datetime import datetime, timedelta
from random import uniform
from time import sleep

from instance.Client import Instance
from utils.Shared import data


def shifts(Client: Instance) -> None:
    """
    The shifts function is one of the main functions of the program. It is responsible for
    switching the account between active and passive modes, as well as sleeping when necessary.

    Args:
        Client (Instance): The account's class for interacting with Discord.

    Returns:
        None
    """

    # Gets the last shift the progrm was on
    index = Client.Repository.database["shifts"]["shift"]

    # If the last shift the program was on does not exist anymore, set the shift to `1`
    index = 1 if index not in Client.Repository.config["shifts"].keys() else index

    while True:
        # Set the current shift in the database to index
        Client.Repository.database["shifts"]["shift"] = index

        # Update the database
        Client.Repository.database_write()

        # If the shift the program is on isn't enabled...
        if not Client.Repository.config["shifts"][index]["enabled"]:
            # ...skip to the next shift. If there is no next shift, go back to the first shift
            index += (
                1
                if index + 1 in Client.Repository.config["shifts"].keys()
                else -index + 1
            )
            continue

        # If the current shift state is active...
        if Client.Repository.database["shifts"]["state"] == "active":
            # ...calculate the variation in the shift length
            variation = uniform(
                0, Client.Repository.config["shifts"][index]["variation"]
            )

            # Work out how long the program has to sleep for before it can switch to passive mode
            sleep_len = (
                (
                    datetime.strptime(
                        Client.Repository.database["shifts"]["active"],
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                    + timedelta(
                        seconds=Client.Repository.config["shifts"][index]["active"]
                    )
                )
                - datetime.now()
            ).total_seconds() + variation

            # If the sleep time is negative, then set it to 1
            sleep_len = sleep_len if sleep_len > 0 else 1

            Client.log("DEBUG", "Currently in active mode.")

            # Tell the program it can run commands
            data[Client.username] = True

            # Sleep the required time
            sleep(sleep_len)

            Client.log("DEBUG", "Moving to passive mode.")

            # Tell the program it can't run commands
            data[Client.username] = False

            # Set the shift state to `passive`
            Client.Repository.database["shifts"]["state"] = "passive"

            # Set the shift start time to the time now
            Client.Repository.database["shifts"]["passive"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )

            # Update the database
            Client.Repository.database_write()

        # If the current shift state is passive...
        if Client.Repository.database["shifts"]["state"] == "passive":
            # ...calculate the variation in the shift length
            variation = uniform(
                0, Client.Repository.config["shifts"][index]["variation"]
            )

            # Work out how long the program has to sleep for before it can switch to active mode
            sleep_len = (
                (
                    datetime.strptime(
                        Client.Repository.database["shifts"]["passive"],
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                    + timedelta(
                        seconds=Client.Repository.config["shifts"][index]["passive"]
                    )
                )
                - datetime.now()
            ).total_seconds() + variation

            # If the sleep time is negative, then set it to 1
            sleep_len = sleep_len if sleep_len > 0 else 1

            # Tell the program it can't run commands
            data[Client.username] = False

            Client.log("DEBUG", "Currently in passive mode.")

            # Sleep the required time
            sleep(sleep_len)

            Client.log("DEBUG", "Moving to active mode.")

            # Tell the program it can run commands
            data[Client.username] = True

            # Set the shift state to `active`
            Client.Repository.database["shifts"]["state"] = "active"

            # Set the shift start time to the time now
            Client.Repository.database["shifts"]["active"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )
            # Update the database
            Client.Repository.database_write()

        # Move to the next shift. If there is no next shift, go back to the first shift
        index += (
            1 if index + 1 in Client.Repository.config["shifts"].keys() else -index + 1
        )
