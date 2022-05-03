from json import loads, dumps
from utils.Logger import log
from contextlib import suppress
from os import listdir, mkdir
from os.path import isdir, isfile
from typing import Optional, Union
from utils.Converter import DictToClass
from discord.UserInfo import user_info
from instance.Exceptions import InvalidUserID, IDNotFound, ExistingUserID
import utils.Yaml
from time import time


def create_config(cwd: str, folder: int) -> open:
    with open(f"{cwd}database/templates/config.yml", "r") as config_template_file:
        config_template = config_template_file.read()

    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/config.yml", "x").close()

    config_file = open(f"{cwd}database/{folder}/config.yml", "r+")
    config_file.write(config_template)
    config_file.flush()

    return config_file, utils.Yaml.loads(config_template)


def create_database(cwd: str, folder: int) -> open:
    with open(f"{cwd}database/templates/database.json", "r") as database_template_file:
        database_template = database_template_file.read()

    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/database.json", "x").close()

    database_file = open(f"{cwd}database/{folder}/database.json", "r+")
    database_file.write(database_template)
    database_file.flush()

    return database_file, loads(database_template)


def create_info(cwd: str, account) -> open:
    info_template = account.__dict__
    info_template["controllers"] = [account.id]
    info_template["controllers_info"] = {
        account.id: {"added": int(time()), "added_by": account.id, "commands": []}
    }
    info_template["stats"] = {
        "commands_ran": 0,
        "buttons_clicked": 0,
        "dropdowns_selected": 0,
    }

    with suppress(FileExistsError):
        open(f"{cwd}database/{account.id}/info.json", "x").close()

    info_file = open(f"{cwd}database/{account.id}/info.json", "r+")
    info_file.write(dumps(info_template))
    info_file.flush()

    return info_file, info_template


class Database(object):
    def __init__(self, cwd: str, account: DictToClass, Client):
        self.token = Client.token

        if Client.id in [
            obj
            for obj in listdir(f"{cwd}database")
            if isdir(f"{cwd}database/{obj}") and obj != "__pycache__"
        ]:
            log(f"{Client.username}", "DEBUG", f"Found existing database.")

            self.config_file = open(f"{cwd}database/{Client.id}/config.yml", "r+")
            self.config = utils.Yaml.loads(self.config_file.read())

            self.database_file = open(f"{cwd}database/{Client.id}/database.json", "r+")
            self.database = loads(self.database_file.read())

            self.info_file = open(f"{cwd}database/{Client.id}/info.json", "r+")
            old_info = loads(self.info_file.read())
            account.controllers = old_info["controllers"]
            account.controllers_info = old_info["controllers_info"]
            account.stats = old_info["stats"]
            self.info = account.__dict__
            self.info_write()
        else:
            log(
                f"{Client.username}",
                "DEBUG",
                f"Database does not exist. Creating database now.",
            )

            mkdir(f"{cwd}database/{Client.id}")

            self.config_file, self.config = create_config(cwd, Client.id)

            self.database_file, self.database = create_database(cwd, Client.id)

            self.info_file, self.info = create_info(cwd, account)

    def config_write(self) -> None:
        self.config_file.seek(0)
        self.config_file.truncate()
        self.config_file.write(utils.Yaml.dumps(self.config))
        self.config_file.flush()

    def database_write(self) -> None:
        self.database_file.seek(0)
        self.database_file.truncate()
        self.database_file.write(dumps(self.database))
        self.database_file.flush()

    def info_write(self) -> None:
        self.info_file.seek(0)
        self.info_file.truncate()
        self.info_file.write(dumps(self.info))
        self.info_file.flush()

    def database_handler(
        self,
        command: str,
        arg: Optional[str] = None,
        data: Optional[Union[str, int]] = None,
        ID: int = None,
    ) -> Optional[bool]:
        if command == "write":
            if arg == "controller add":
                if data in self.info["controllers"]:
                    return (
                        False,
                        ExistingUserID,
                        "The ID you provided already is in the list of controllers for this account.",
                    )

                info = user_info(self.token, data)

                if info is None:
                    message = "The ID you provided does not belong to any user."

                    try:
                        data = int(data)
                    except ValueError:
                        message = "IDs contain only numbers. The ID you provided contained other characters."

                    return False, InvalidUserID, message
                else:
                    self.info["controllers"].append(data)
                    self.info["controllers_info"][data] = {
                        "added": int(time()),
                        "added_by": ID,
                        "commands": [],
                    }
                    self.info_write()
                    return True, None
            elif arg == "controller remove":
                if data not in self.info["controllers"]:
                    return (
                        False,
                        IDNotFound,
                        "The ID you provided was not found in the list of controllers.",
                    )
                else:
                    self.info["controllers"].remove(data)
                    self.info_write()
                    return True, None

    def log_command(self, command: str, message: dict) -> None:
        self.info["controllers_info"][message["author"]["id"]]["commands"].append(
            [round(int(time())), command]
        )
        self.info_write()
