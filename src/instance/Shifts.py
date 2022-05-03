from instance.Client import Instance
from database.Handler import Database
from datetime import datetime
from json import dumps
from utils.Shared import data


def shifts(Client: Instance, Repository: Database) -> None:
    while True:
        if (
            not data[Client.username]
            and (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(Repository.database["shifts"]["passive"], "%x-%X")
            ).total_seconds()
            >= Repository.config["shifts"]["passive"]
        ):
            data[Client.username] = True
            Repository.database["shifts"]["passive"] = datetime.now().strftime("%x-%X")
            Repository.database["shifts"]["active"] = datetime.now().strftime("%x-%X")
            Repository.database_write()
            Client.log("DEBUG", "Beginning active phase.")
        elif (
            data[Client.username]
            and (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(Repository.database["shifts"]["active"], "%x-%X")
            ).total_seconds()
            >= Repository.config["shifts"]["active"]
        ):
            data[Client.username] = False
            Repository.database["shifts"]["active"] = datetime.now().strftime("%x-%X")
            Repository.database["shifts"]["passive"] = datetime.now().strftime("%x-%X")
            Repository.database_write()
            Client.log("DEBUG", "Beginning passive phase.")
