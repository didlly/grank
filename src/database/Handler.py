from contextlib import suppress
from datetime import datetime
from json import dumps, loads
from json.decoder import JSONDecodeError
from os import listdir, mkdir
from os.path import isdir
from time import time
from typing import Optional, Union

import utils.Yaml
from discord.UserInfo import user_info
from instance.Client import Instance
from instance.Exceptions import ExistingUserID, IDNotFound, InvalidUserID
from utils.Converter import DictToClass
from utils.Merge import merge


def create_config(cwd: str, folder: int) -> tuple:
    """
    The create_config function creates a config file for the specified account.

    Args:
        cwd (str): The current working directory
        folder (int): The name of the account's folder

    Returns:
        A tuple of the config file and the parsed config
    """

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


def rebuild_config(cwd: str, folder: int) -> bool:
    """
    The rebuild_config function is used to rebuild the config file for the specified account.

    Args:
        cwd (str): The current working directory of the program
        folder (int): The name of the account's folder

    Returns:
        bool: Indicates whether the subprogram executed successfully or not
    """

    with open(f"{cwd}database/templates/config.yml", "r") as config_template_file:
        config_template = utils.Yaml.loads(config_template_file.read())

    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/config.yml", "x").close()

    config_file = open(f"{cwd}database/{folder}/config.yml", "r+")

    try:
        config = utils.Yaml.loads(config_file.read())
    except Exception:
        config = {}

    config = merge(config, config_template)

    config_file.seek(0)

    config_file.truncate()

    config_file.write(utils.Yaml.dumps(config))

    config_file.flush()

    return True


def create_database(cwd: str, folder: int) -> tuple:
    """
    The create_database function creates a database file for the specified account.

    Args:
        cwd (str): The current working directory
        folder (int): The name of the account's folder

    Returns:
        A tuple of the database file and the parsed database
    """

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


def rebuild_database(cwd: str, folder: int) -> bool:
    """
    The rebuild_database function is used to rebuild the database file for the specified account.

    Args:
        cwd (str): The current working directory of the program
        folder (int): The name of the account's folder

    Returns:
        bool: Indicates whether the subprogram executed successfully or not
    """

    with open(f"{cwd}database/templates/database.json", "r") as database_template_file:
        database_template = loads(database_template_file.read())

    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/database.json", "x").close()

    database_file = open(f"{cwd}database/{folder}/database.json", "r+")

    try:
        database = loads(database_file.read())
    except JSONDecodeError:
        database = {}

    database = merge(database, database_template)

    database_file.seek(0)

    database_file.truncate()

    database_file.write(dumps(database, indent=4))

    database_file.flush()

    return True


def create_controllers(cwd: str, account: DictToClass) -> tuple:
    """
    The create_controllers function creates a controllers file for the specified account.

    Args:
        cwd (str): The current working directory
        account (DictToClass): The account's data class

    Returns:
        A tuple of the controllers file and the parsed controllers
    """

    with suppress(FileExistsError):
        open(f"{cwd}database/{account.id}/controllers.json", "x").close()

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

    controllers_file = open(f"{cwd}database/{account.id}/controllers.json", "r+")

    controllers_file.seek(0)

    controllers_file.truncate()

    controllers_file.write(dumps(controllers_template, indent=4))

    controllers_file.flush()

    return controllers_file, controllers_template


def rebuild_controllers(cwd: str, folder: int) -> bool:
    """
    The rebuild_controllers function is used to rebuild the controllers file for the specified account.

    Args:
        cwd (str): The current working directory of the program
        folder (int): The name of the account's folder

    Returns:
        bool: Indicates whether the subprogram executed successfully or not
    """

    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/controllers.json", "x").close()

    controllers_file = open(f"{cwd}database/{folder}/controllers.json", "r+")

    try:
        controllers = loads(controllers_file.read())
    except JSONDecodeError:
        controllers = {}

    controllers = merge(
        controllers,
        {
            "controllers": [folder],
            "controllers_info": {
                folder: {
                    "added": int(time()),
                    "added_by": folder,
                    "commands": [],
                }
            },
        },
    )

    controllers_file.seek(0)

    controllers_file.truncate()

    controllers_file.write(dumps(controllers, indent=4))

    controllers_file.flush()

    return True


def create_info(cwd: str, account: DictToClass) -> tuple:
    """
    The create_info function creates a info file for the specified account.

    Args:
        cwd (str): The current working directory
        account (DictToClass): The account's data class

    Returns:
        A tuple of the info file and the parsed info
    """

    with suppress(FileExistsError):
        open(f"{cwd}database/{account.id}/info.json", "x").close()

    account.stats = {
        "commands_ran": 0,
        "buttons_clicked": 0,
        "dropdowns_selected": 0,
        "coins_gained": 0,
        "items_gained": {},
    }

    info_file = open(f"{cwd}database/{account.id}/info.json", "r+")

    info_file.seek(0)

    info_file.truncate()

    info_file.write(dumps(account.__dict__, indent=4))

    info_file.flush()

    return info_file, account.__dict__


def rebuild_info(cwd: str, folder: int, account: DictToClass) -> bool:
    """
    The rebuild_info function is used to rebuild the info file for the specified account.

    Args:
        cwd (str): The current working directory of the program
        folder (int): The name of the account's folder
        account (DictToClass): The account's data class

    Returns:
        bool: Indicates whether the subprogram executed successfully or not
    """

    with suppress(FileExistsError):
        open(f"{cwd}database/{folder}/info.json", "x").close()

    info_file = open(f"{cwd}database/{folder}/info.json", "r+")

    try:
        info = loads(info_file.read())
    except JSONDecodeError:
        info = account.__dict__

    info = merge(
        info,
        {
            "stats": {
                "commands_ran": 0,
                "buttons_clicked": 0,
                "dropdowns_selected": 0,
                "coins_gained": 0,
                "items_gained": {},
            }
        },
    )

    info_file.seek(0)

    info_file.truncate()

    info_file.write(dumps(info, indent=4))

    info_file.flush()

    return True


class Database(object):
    def __init__(self, cwd: str, account: DictToClass, Client: Instance) -> None:
        """
        The __init__ function is called when the class is instantiated.
        It initializes all of the variables and sets up any data structures that
        the object will need to use later on. It's very important to understand
        that every variable defined in this function will be an attribute of every
        instance created from this class.

        Args:
            self: Gives access to the class' attributes and methods
            cwd (str): The current working directory of the program
            account (DictToClass) The account's data class
            Client (Instance): The account's class for interacting with Discord

        Returns:
            NoneType: __init__ functions for classes aren't allowed to return anything, don't ask me why
        """

        self.Client = Client

        if Client.id in [
            obj
            for obj in listdir(f"{cwd}database")
            if isdir(f"{cwd}database/{obj}") and obj != "__pycache__"
        ]:
            self.Client.log("DEBUG", f"Found existing database.")

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
            self.Client.log(
                "DEBUG",
                f"Database does not exist. Creating database now.",
            )

            mkdir(f"{cwd}database/{Client.id}")

            self.config_file, self.config = create_config(cwd, Client.id)

            self.database_file, self.database = create_database(cwd, Client.id)

            self.info_file, self.info = create_info(cwd, account)

            self.controllers_file, self.controllers = create_controllers(cwd, account)

            self.Client.log(
                "DEBUG",
                f"Created database.",
            )

    def config_write(self) -> bool:
        """
        The config_write function writes the config dictionary in memory, converted to a string, to it's file

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            bool: Indicates whether the subprogram executed successfully or not
        """

        self.config_file.seek(0)

        self.config_file.truncate()

        self.config_file.write(utils.Yaml.dumps(self.config))

        self.config_file.flush()

        return True

    def database_write(self) -> bool:
        """
        The database_write function writes the database dictionary in memory, converted to a string, to it's file

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            bool: Indicates whether the subprogram executed successfully or not
        """

        self.database_file.seek(0)

        self.database_file.truncate()

        self.database_file.write(dumps(self.database, indent=4))

        self.database_file.flush()

        return True

    def info_write(self) -> bool:
        """
        The info_write function writes the info dictionary in memory, converted to a string, to it's file

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            bool: Indicates whether the subprogram executed successfully or not
        """

        self.info_file.seek(0)

        self.info_file.truncate()

        self.info_file.write(dumps(self.info, indent=4))

        self.info_file.flush()

        return True

    def controllers_write(self) -> bool:
        """
        The controllers_write function writes the controllers dictionary in memory, converted to a string, to it's file

        Args:
            self: Access the attributes and methods of the class in python

        Returns:
            bool: Indicates whether the subprogram executed successfully or not
        """

        self.controllers_file.seek(0)

        self.controllers_file.truncate()

        self.controllers_file.write(dumps(self.controllers, indent=4))

        self.controllers_file.flush()

        return True

    def database_handler(
        self,
        command: str,
        arg: Optional[str] = None,
        data: Optional[Union[str, int]] = None,
        ID: int = None,
    ) -> Optional[tuple]:
        """
        The database_handler function is used to write and read data from the database.
        The database_handler function takes in a command, an argument, some data, and an ID as arguments.
        If the command is "write" it will write to the database

        Args:
            self: Access variables that belongs to the class
            command:str: Specify what command is being run
            arg:Optional[str]=None: Tell the user that they do not have to provide an argument
            data:Optional[Union[str: Pass the data to the function
            int]]=None: Specify the id of the user that requested this action
            ID:int=None: Specify the id of the user who is executing the command
            : Specify the command that is being run

        Returns:
            A tuple containing data indicating whether the subprogram ran successfully or not
        """

        if command == "write":
            if arg == "controller add":
                if data in self.controllers["controllers"]:
                    return (
                        False,
                        ExistingUserID,
                        "The ID you provided **is already** in the list of controllers for this account.",
                    )

                controllers = user_info(self.Client.token, data)

                if controllers is None:
                    message = "The ID you provided does **not belong to any user**."

                    if any(char.isalpha() for char in data):
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

    def log_command(self, Client: Instance, message: dict) -> Optional[bool]:
        """
        The log_command function is called when a command is ran. It logs the command in the log file, and also sends a webhook to the logging channel.

        Args:
            self: Access the bot's attributes and methods
            Client (Instance): The Discord client
            message (dict): The command that was sent by the user

        Returns:
            bool: Indicates whether the subprogram ran successfully or not
        """

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

        return True
