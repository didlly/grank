from instance.Client import Instance
from datetime import datetime, timedelta
from utils.Shared import data
from time import sleep
from random import uniform


def shifts(Client: Instance) -> None:
    index = Client.Repository.database["shifts"]["shift"]

    index = 1 if index not in Client.Repository.config["shifts"].keys() else 1

    while True:
        Client.Repository.database["shifts"]["shift"] = index
        Client.Repository.database_write()

        if not Client.Repository.config["shifts"][index]["enabled"]:
            index += (
                1
                if index + 1 in Client.Repository.config["shifts"].keys()
                else -index + 1
            )
            continue

        if Client.Repository.database["shifts"]["state"] == "active":
            variation = uniform(
                0, Client.Repository.config["shifts"][index]["variation"]
            )

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

            sleep_len = sleep_len if sleep_len > 0 else 1

            Client.log("DEBUG", "Currently in active mode.")

            data[Client.username] = True

            sleep(sleep_len)

            Client.log("DEBUG", "Moving to passive mode.")

            data[Client.username] = False

            Client.Repository.database["shifts"]["state"] = "passive"
            Client.Repository.database["shifts"]["passive"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )
            Client.Repository.database_write()

        if Client.Repository.database["shifts"]["state"] == "passive":
            variation = uniform(
                0, Client.Repository.config["shifts"][index]["variation"]
            )

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

            sleep_len = sleep_len if sleep_len > 0 else 1

            data[Client.username] = False

            Client.log("DEBUG", "Currently in passive mode.")

            sleep(sleep_len)

            Client.log("DEBUG", "Moving to active mode.")

            data[Client.username] = True

            Client.Repository.database["shifts"]["state"] = "active"
            Client.Repository.database["shifts"]["active"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )
            Client.Repository.database_write()

        index += (
            1 if index + 1 in Client.Repository.config["shifts"].keys() else -index + 1
        )
