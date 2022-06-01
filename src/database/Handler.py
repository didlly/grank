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

    # Open the config template file...
    with open(f"{cwd}database/templates/config.yml", "r") as config_template_file:
        # ...and read the config template from it
        config_template = config_template_file.read()

    with suppress(FileExistsError):
        # Create the config file, and suppress the FileExistsError if it occurs
        open(f"{cwd}database/{folder}/config.yml", "x").close()

    # Re-open the config file in read & write mode
    config_file = open(f"{cwd}database/{folder}/config.yml", "r+")

    # Move the cursor to the start of the config file
    config_file.seek(0)

    # Remove the contents of the config file after the cursor (i.e, delete the contents of the config file)
    config_file.truncate()

    # Write the config template to the config file
    config_file.write(config_template)

    # Flush all changes to the config file to make sure they take effect
    config_file.flush()

    # Return the config file and the parsed config
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

    # Open the config template file...
    with open(f"{cwd}database/templates/config.yml", "r") as config_template_file:
        # ...and read the config template from it
        config_template = utils.Yaml.loads(config_template_file.read())

    with suppress(FileExistsError):
        # Create the config file, and suppress the FileExistsError if it occurs
        open(f"{cwd}database/{folder}/config.yml", "x").close()

    # Re-open the config file in read & write mode
    config_file = open(f"{cwd}database/{folder}/config.yml", "r+")

    try:
        # Parse the contents of the config file into a dictionary
        config = utils.Yaml.loads(config_file.read())
    except Exception:
        # If there is an error while parsing, an Exception would be raised, which is caught here, and the program will set config to an empty dictionary
        config = {}

    # Merge the config and config template
    config = merge(config, config_template)

    # Move the cursor to the start of the config file
    config_file.seek(0)

    # Remove the contents of the config file after the cursor (i.e, delete the contents of the config file)
    config_file.truncate()

    # Write the config in string form to the config file
    config_file.write(utils.Yaml.dumps(config))

    # Flush all changes to the config file to make sure they take effect
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

    # Open the database template file...
    with open(f"{cwd}database/templates/database.json", "r") as database_template_file:
        # ...and read the database template from it
        database_template = database_template_file.read()

    with suppress(FileExistsError):
        # Create the database file, and suppress the FileExistsError if it occurs
        open(f"{cwd}database/{folder}/database.json", "x").close()

    # Re-open the database file in read & write mode
    database_file = open(f"{cwd}database/{folder}/database.json", "r+")

    # Move the cursor to the start of the database file
    database_file.seek(0)

    # Remove the contents of the database file after the cursor (i.e, delete the contents of the database file)
    database_file.truncate()

    # Write the database template to the database file
    database_file.write(database_template)

    # Flush all changes to the database file to make sure they take effect
    database_file.flush()

    # Return the database file and the parsed database
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

    # Open the database template file...
    with open(f"{cwd}database/templates/database.json", "r") as database_template_file:
        # ...and read the database template from it
        database_template = loads(database_template_file.read())

    with suppress(FileExistsError):
        # Create the database file, and suppress the FileExistsError if it occurs
        open(f"{cwd}database/{folder}/database.json", "x").close()

    # Re-open the database file in read & write mode
    database_file = open(f"{cwd}database/{folder}/database.json", "r+")

    try:
        # Parse the contents of the database file into a dictionary
        database = loads(database_file.read())
    except JSONDecodeError:
        # If there is an error while parsing, a JSONDecodeError would be raised, which is caught here, and the program will set database to an empty dictionary
        database = {}

    # Merge the database and database template
    database = merge(database, database_template)

    # Move the cursor to the start of the database file
    database_file.seek(0)

    # Remove the contents of the database file after the cursor (i.e, delete the contents of the database file)
    database_file.truncate()

    # Write the database in string from the the database file
    database_file.write(dumps(database, indent=4))

    # Flush all changes to the database file to make sure they take effect
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
        # Create the controllers file, and suppress the FileExistsError if it occurs
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

    # Re-open the controllers file in read & write mode
    controllers_file = open(f"{cwd}database/{account.id}/controllers.json", "r+")

    # Move the cursor to the start of the controllers file
    controllers_file.seek(0)

    # Remove the contents of the controllers file after the cursor (i.e, delete the contents of the controllers file)
    controllers_file.truncate()

    # Write the controllers template in string form to the controllers file
    controllers_file.write(dumps(controllers_template, indent=4))

    # Flush all changes to the controllers file to make sure they take effect
    controllers_file.flush()

    # Return the controllers file and the controllers template
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
        # Create the controllers file, and suppress the FileExistsError if it occurs
        open(f"{cwd}database/{folder}/controllers.json", "x").close()

    # Re-open the controllers file in read & write mode
    controllers_file = open(f"{cwd}database/{folder}/controllers.json", "r+")

    try:
        # Parse the contents of the controllers file into a dictionary
        controllers = loads(controllers_file.read())
    except JSONDecodeError:
        # If there is an error while parsing, a JSONDecodeError would be raised, which is caught here, and the program will set controllers to an empty dictionary
        controllers = {}

    # Merge the controllers & controllers template. `folder` is being used as it is the same as the account's ID
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

    # Move the cursor to the start of the controllers file
    controllers_file.seek(0)

    # Remove the contents of the controllers file after the cursor (i.e, delete the contents of the controllers file)
    controllers_file.truncate()

    # Write the controllers in string form the the controllers file
    controllers_file.write(dumps(controllers, indent=4))

    # Flush all changes to the controllers file to make sure they take effect
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
        # Create the info file, and suppress the FileExistsError if it occurs
        open(f"{cwd}database/{account.id}/info.json", "x").close()

    account.stats = {
        "commands_ran": 0,
        "buttons_clicked": 0,
        "dropdowns_selected": 0,
        "coins_gained": 0,
        "items_gained": {},
    }

    # Re-open the info file in read & write mode
    info_file = open(f"{cwd}database/{account.id}/info.json", "r+")

    # Move the cursor to the start of the info file
    info_file.seek(0)

    # Remove the contents of the info file after the cursor (i.e, delete the contents of the info file)
    info_file.truncate()

    # Write the account's class' dictionary in string form to the info file.
    info_file.write(dumps(account.__dict__, indent=4))

    # Flush all changes to the info file to make sure they take effect
    info_file.flush()

    # Return the info file and the account's class' dictionary
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
        # Create the info file, and suppress the FileExistsError if it occurs
        open(f"{cwd}database/{folder}/info.json", "x").close()

    # Re-open the info file in read & write mode
    info_file = open(f"{cwd}database/{folder}/info.json", "r+")

    try:
        # Parse the contents of the info file into a dictionary
        info = loads(info_file.read())
    except JSONDecodeError:
        # If there is an error while parsing, a JSONDecodeError would be raised, which is caught here, and the program will set info to the dictionary version of the account's data class
        info = account.__dict__

    # Merge the info and info template
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

    # Move the cursor to the start of the info file
    info_file.seek(0)

    # Remove the contents of the info file after the cursor (i.e, delete the contents of the info file)
    info_file.truncate()

    # Write the info in string form to the info file
    info_file.write(dumps(info, indent=4))

    # Flush all changes to the database file to make sure they take effect
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

        # Copy the Client class into this class
        self.Client = Client

        # If the account already has a database (when getting the list of folders, folders called `__pycache__` aren't added)...
        if Client.id in [
            obj
            for obj in listdir(f"{cwd}database")
            if isdir(f"{cwd}database/{obj}") and obj != "__pycache__"
        ]:
            self.Client.log("DEBUG", f"Found existing database.")

            # Open the config file in read & write mode
            self.config_file = open(f"{cwd}database/{Client.id}/config.yml", "r+")
            # Parse the contents of the config file into a dictionary
            self.config = utils.Yaml.loads(self.config_file.read())

            # Open the database file in read & write mode
            self.database_file = open(f"{cwd}database/{Client.id}/database.json", "r+")
            # Parse the contents of the database file into a dictionary
            self.database = loads(self.database_file.read())

            # Open the info file in read & write mode
            self.info_file = open(f"{cwd}database/{Client.id}/info.json", "r+")
            # Parse the contents of the info file into a dictionary
            self.info = loads(self.info_file.read())

            # Open the controllers file in read & write mode
            self.controllers_file = open(
                f"{cwd}database/{Client.id}/controllers.json", "r+"
            )
            # Parse the contents of the controllers file into a dictionary
            self.controllers = loads(self.controllers_file.read())
        # Else...
        else:
            self.Client.log(
                "DEBUG",
                f"Database does not exist. Creating database now.",
            )

            # Create a directory for the account
            mkdir(f"{cwd}database/{Client.id}")

            # Create and parse the config file
            self.config_file, self.config = create_config(cwd, Client.id)

            # Create and parse the database file
            self.database_file, self.database = create_database(cwd, Client.id)

            # Create and parse the info file
            self.info_file, self.info = create_info(cwd, account)

            # Create and parse the controllers file
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

        # Move the cursor to the start of the config file
        self.config_file.seek(0)

        # Remove the contents of the config file after the cursor (i.e, delete the contents of the config file)
        self.config_file.truncate()

        # Write the config in string form to the config file
        self.config_file.write(utils.Yaml.dumps(self.config))

        # Flush all changes to the config file to make sure they take effect
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

        # Move the cursor to the start of the database file
        self.database_file.seek(0)

        # Remove the contents of the database file after the cursor (i.e, delete the contents of the database file)
        self.database_file.truncate()

        # Write the database in string from the the database file
        self.database_file.write(dumps(self.database, indent=4))

        # Flush all changes to the database file to make sure they take effect
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

        # Move the cursor to the start of the info file
        self.info_file.seek(0)

        # Remove the contents of the info file after the cursor (i.e, delete the contents of the info file)
        self.info_file.truncate()

        # Write the info in string form to the info file
        self.info_file.write(dumps(self.info, indent=4))

        # Flush all changes to the database file to make sure they take effect
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

        # Move the cursor to the start of the controllers file
        self.controllers_file.seek(0)

        # Remove the contents of the controllers file after the cursor (i.e, delete the contents of the controllers file)
        self.controllers_file.truncate()

        # Write the controllers in string form the the controllers file
        self.controllers_file.write(dumps(self.controllers, indent=4))

        # Flush all changes to the controllers file to make sure they take effect
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

        # If the command is `write`...
        if command == "write":
            # ...if the arg is `controller add`...
            if arg == "controller add":
                # ...if the ID to add is already in the list of controllers...
                if data in self.controllers["controllers"]:
                    # ...return False and the error message
                    return (
                        False,
                        ExistingUserID,
                        "The ID you provided **is already** in the list of controllers for this account.",
                    )

                # Get the info about the ID to add
                controllers = user_info(self.Client.token, data)

                # If the ID does not exist
                if controllers is None:
                    # Initialize the error message
                    message = "The ID you provided does **not belong to any user**."

                    # If the ID contains letters...
                    if any(char.isalpha() for char in data):
                        # ...update the error message
                        message = "IDs contain **only numbers**. The ID you provided contained **other characters**."

                    # Return False and the error message
                    return False, InvalidUserID, message
                # Else...
                else:
                    # Add the ID to the list of controllers
                    self.controllers["controllers"].append(data)

                    # Add the information about the time the controller was added etc. to the controllers file
                    self.controllers["controllers_info"][data] = {
                        "added": int(time()),
                        "added_by": ID,
                        "commands": [],
                    }

                    # Update the controllers file
                    self.controllers_write()

                    # Return True and no error message
                    return True, None
            # ...else if the arg is `controller remove`...
            elif arg == "controller remove":
                # ...if the ID provided is not in the lsit of controllers...
                if data not in self.controllers["controllers"]:
                    # ...return False and the error message
                    return (
                        False,
                        IDNotFound,
                        "The ID you provided was **not found** in the list of controllers.",
                    )
                else:
                    # Remove the controller from the controllers file
                    self.controllers["controllers"].remove(data)

                    # Update the controllers file
                    self.controllers_write()

                    # Return True and no error message
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

        # Add the command to the list of commands ran by that user, and include the UNIX time it was run
        self.controllers["controllers_info"][message["author"]["id"]][
            "commands"
        ].append([round(int(time())), message["content"]])

        # Update the controllers file
        self.controllers_write()

        return True
