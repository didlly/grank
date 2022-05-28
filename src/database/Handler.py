from contextlib import suppress
from datetime import datetime
from json import dumps, loads
from os import listdir, mkdir
from os.path import isdir
from time import time
from typing import Optional, Union

import utils.Yaml
from discord.UserInfo import user_info
from instance.Exceptions import ExistingUserID, IDNotFound, InvalidUserID
from utils.Converter import DictToClass
from utils.Logger import log


def create_config(cwd: str, folder: int) -> open:
    with open(f"{cwd}database/templates/config.yml", "r") as config_template_file:
        config_template = config_template_file.read()

    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/config.yml", "x").close()

    config_file = open(f"{cwd}database/{folder}/config.yml", "r+")
    config_file.seek(0)
    config_file.truncate()
    config_file.write(config_template)
    config_file.flush()

    return config_file, utils.Yaml.loads(config_template)


def rebuild_config(cwd: str, folder: int):
    with open(f"{cwd}database/templates/config.yml", "r") as config_template_file:
        config_template = utils.Yaml.loads(config_template_file.read())

    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/config.yml", "x").close()

    config_file = open(f"{cwd}database/{folder}/config.yml", "r+")
    config = utils.Yaml.loads(config_file.read())
    
    config = config | config_template
    config_file.seek(0)
    config_file.truncate()
    config_file.write(utils.Yaml.dumps(config))
    config_file.flush() 

def create_database(cwd: str, folder: int) -> open:
    with open(f"{cwd}database/templates/database.json", "r") as database_template_file:
        database_template = database_template_file.read()

    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/database.json", "x").close()

    database_file = open(f"{cwd}database/{folder}/database.json", "r+")
    database_file.seek(0)
    database_file.truncate()
    database_file.write(database_template)
    database_file.flush()

    return database_file, loads(database_template)

def rebuild_database(cwd: str, folder: int):
    with open(f"{cwd}database/templates/database.json", "r") as database_template_file:
        database_template = loads(database_template_file.read())

    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/database.json", "x").close()

    database_file = open(f"{cwd}database/{folder}/database.json", "r+")
    database = loads(database_file.read())
    
    database = database | database_template
    
    database_file.seek(0)
    database_file.truncate()
    database_file.write(dumps(database, indent=4))
    database_file.flush()

def create_info(cwd: str, account):
    with suppress(FileExistsError):
        open(f"{cwd}database/{account.id}/info.json", "x").close()

    account.stats = {
        "commands_ran": 0,
        "buttons_clicked": 0,
        "dropdowns_selected": 0,
        "coins_gained": 0
    }

    info_file = open(f"{cwd}database/{account.id}/info.json", "r+")
    info_file.seek(0)
    info_file.truncate()
    info_file.write(dumps(account.__dict__, indent=4))
    info_file.flush()

    return info_file, account.__dict__

def rebuild_info(cwd: str, folder: int):
    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/info.json", "x").close()

    info_file = open(f"{cwd}database/{folder}/info.json", "r+")
    info = loads(info_file.read())
    
    info = info | {"stats": {
            "commands_ran": 0,
            "buttons_clicked": 0,
            "dropdowns_selected": 0,
            "coins_gained": 0,
        }}
    
    info_file.seek(0)
    info_file.truncate()
    info_file.write(dumps(info, indent=4))
    info_file.flush()

def create_controllers(cwd: str, account) -> open:
    controllers_template = {
        "controllers": [account.id],
        "controllers_info": {
            account.id: {
                "added": int(time()),
                "added_by": account.id,
                "commands": [],
            }
        },
    }

    with suppress(FileExistsError):
        open(f"{cwd}database/{account.id}/controllers.json", "x").close()

    controllers_file = open(f"{cwd}database/{account.id}/controllers.json", "r+")
    controllers_file.write(dumps(controllers_template, indent=4))
    controllers_file.flush()

    return controllers_file, controllers_template

def rebuild_controllers(cwd: str, folder: int):
    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/controllers.json", "x").close()

    controllers_file = open(f"{cwd}database/{folder}/controllers.json", "r+")
    controllers = loads(controllers_file.read())
    
    controllers = controllers | {"controllers": [folder],
        "controllers_info": {
            folder: {
                "added": int(time()),
                "added_by": folder,
                "commands": [],
            }
        }}
    
    controllers_file.seek(0)
    controllers_file.truncate()
    controllers_file.write(dumps(controllers, indent=4))
    controllers_file.flush()

class Database(object):
    def __init__(self, cwd: str, account: DictToClass, Client):
        self.Client = Client
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
            self.info = loads(self.info_file.read())

            self.controllers_file = open(
                f"{cwd}database/{Client.id}/controllers.json", "r+"
            )
            self.controllers = loads(self.controllers_file.read())
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

            self.controllers_file, self.controllers = create_controllers(cwd, account)

            log(
                f"{Client.username}",
                "DEBUG",
                f"Created database.",
            )

        exec(
            f"self.config['auto accept trade']['traders'] = {[str(trader) for trader in self.config['auto accept trade']['traders']]}"
        )

    def config_write(self) -> None:
        self.config_file.seek(0)
        self.config_file.truncate()
        self.config_file.write(utils.Yaml.dumps(self.config))
        self.config_file.flush()

    def database_write(self) -> None:
        self.database_file.seek(0)
        self.database_file.truncate()
        self.database_file.write(dumps(self.database, indent=4))
        self.database_file.flush()

    def info_write(self) -> None:
        self.info_file.seek(0)
        self.info_file.truncate()
        self.info_file.write(dumps(self.info, indent=4))
        self.info_file.flush()

    def controllers_write(self) -> None:
        self.controllers_file.seek(0)
        self.controllers_file.truncate()
        self.controllers_file.write(dumps(self.controllers, indent=4))
        self.controllers_file.flush()

    def database_handler(
        self,
        command: str,
        arg: Optional[str] = None,
        data: Optional[Union[str, int]] = None,
        ID: int = None,
    ) -> Optional[bool]:
        if command == "write":
            if arg == "controller add":
                if data in self.controllers["controllers"]:
                    return (
                        False,
                        ExistingUserID,
                        "The ID you provided **is already** in the list of controllers for this account.",
                    )

                controllers = user_info(self.token, data)

                if controllers is None:
                    message = "The ID you provided does **not belong to any user**."

                    try:
                        data = int(data)
                    except ValueError:
                        message = "IDs contain **only numbers**. The ID you provided contained **other characters**."

                    return False, InvalidUserID, message
                else:
                    self.controllers["controllers"].append(data)
                    self.controllers["controllers_info"][data] = {
                        "added": int(time()),
                        "added_by": ID,
                        "commands": [],
                    }
                    self.controllers_write()
                    return True, None
            elif arg == "controller remove":
                if data not in self.controllers["controllers"]:
                    return (
                        False,
                        IDNotFound,
                        "The ID you provided was **not found** in the list of controllers.",
                    )
                else:
                    self.controllers["controllers"].remove(data)
                    self.controllers_write()
                    return True, None

    def log_command(self, Client, message: dict) -> None:
        Client.log(
            "DEBUG",
            f"Received command `{message['content']}` from `{message['author']['username']}#{message['author']['discriminator']}`.",
        )

        Client.webhook_log(
            {
                "content": None,
                "embeds": [
                    {
                        "title": f"**Command received**",
                        "url": f"https://discord.com/channels/{Client.guild_id}/{Client.channel_id}/{message['id']}",
                        "description": f"`{message['content']}`",
                        "color": 3063249,
                        "author": {
                            "name": f"{message['author']['username']}#{message['author']['discriminator']}",
                            "icon_url": f"https://cdn.discordapp.com/avatars/{message['author']['id']}/{message['author']['avatar']}.webp?size=32",
                        },
                        "footer": {
                            "text": Client.username,
                            "icon_url": f"https://cdn.discordapp.com/avatars/{Client.id}/{Client.avatar}.webp?size=32",
                        },
                        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    }
                ],
                "attachments": [],
                "username": "Grank",
                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
            }
        )

        self.controllers["controllers_info"][message["author"]["id"]][
            "commands"
        ].append([round(int(time())), message["content"]])
        self.controllers_write()
