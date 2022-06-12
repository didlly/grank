from json import loads
from json.decoder import JSONDecodeError
from os.path import isdir, isfile
from typing import Optional

import utils.Yaml
from database.Handler import (
    rebuild_config,
    rebuild_controllers,
    rebuild_database,
    rebuild_info,
)
from instance.Client import Instance
from utils.Converter import DictToClass


def verify(cwd: str, Client: Instance, account: DictToClass) -> None:
    """
    The verify function checks if the database is corrupted. If it is, it will rebuild the database.

    Args:
        cwd (str): The current working directory of the program
        Client (Instance): The account's class for interacting with Discord.
        account (DictToClass): The account's data class

    Returns:
        None
    """

    if not isdir(f"{cwd}database/{Client.id}"):
        return

    statuses = []

    if not isfile(f"{cwd}database/{Client.id}/config.yml"):
        statuses.append(False)
    else:
        statuses.append(verify_config(cwd, Client.id))

    if not isfile(f"{cwd}database/{Client.id}/database.json"):
        statuses.append(False)
    else:
        statuses.append(verify_database(cwd, Client.id))

    if not isfile(f"{cwd}database/{Client.id}/controllers.json"):
        statuses.append(False)
    else:
        statuses.append(verify_controllers(cwd, Client.id))

    if not isfile(f"{cwd}database/{Client.id}/info.json"):
        statuses.append(False)
    else:
        statuses.append(verify_info(cwd, Client.id))

    if statuses != [True] * len(statuses):
        Client.log("WARNING", "Database is corrupted. Rebuilding now.")

        if statuses[0] != True:
            Client.log("DEBUG", f"Rebuilding `/database/{Client.id}/config.yml")
            rebuild_config(cwd, Client.id)

        if statuses[1] != True:
            Client.log("DEBUG", f"Rebuilding `/database/{Client.id}/database.json")
            rebuild_database(cwd, Client.id)

        if statuses[2] != True:
            Client.log("DEBUG", f"Rebuilding `/database/{Client.id}/controllers.json")
            rebuild_controllers(cwd, Client.id)

        if statuses[-1] != True:
            Client.log("DEBUG", f"Rebuilding `/database/{Client.id}/info.json")
            rebuild_info(cwd, Client.id, account)


def verify_config(cwd: str, folder: str) -> bool:
    """
    The verify_config function checks to see if the config.yml file is valid.
    It does this by checking for all of the required options and making sure that they are present.

    Args:
        cwd (str): The current working directory
        folder (str): The account's folder to check

    Returns:
        True if the config file is valid, else False
    """

    options = [
        "['commands']",
        "['commands']['adventure']",
        "['commands']['beg']",
        "['commands']['daily']",
        "['commands']['dig']",
        "['commands']['fish']",
        "['commands']['guess']",
        "['commands']['hunt']",
        "['commands']['highlow']",
        "['commands']['postmeme']",
        "['commands']['trivia']",
        "['commands']['vote']",
        "['commands']['work']",
        "['crime']",
        "['crime']['enabled']",
        "['crime']['random']",
        "['crime']['preferences']",
        "['search']",
        "['search']['enabled']",
        "['search']['random']",
        "['search']['preferences']",
        "['lottery']",
        "['lottery']['enabled']",
        "['lottery']['cooldown']",
        "['stream']",
        "['stream']['ads']",
        "['stream']['chat']",
        "['stream']['donations']",
        "['blackjack']",
        "['blackjack']['random']",
        "['blackjack']['enabled']",
        "['blackjack']['amount']",
        "['blackjack']['minimum']",
        "['blackjack']['maximum']",
        "['cooldowns']",
        "['cooldowns']['adventure']",
        "['cooldowns']['beg']",
        "['cooldowns']['beg']['default']",
        "['cooldowns']['beg']['patron']",
        "['cooldowns']['blackjack']",
        "['cooldowns']['blackjack']['default']",
        "['cooldowns']['blackjack']['patron']",
        "['cooldowns']['crime']",
        "['cooldowns']['crime']['default']",
        "['cooldowns']['crime']['patron']",
        "['cooldowns']['daily']",
        "['cooldowns']['dig']",
        "['cooldowns']['dig']['default']",
        "['cooldowns']['dig']['patron']",
        "['cooldowns']['fish']",
        "['cooldowns']['fish']['default']",
        "['cooldowns']['fish']['patron']",
        "['cooldowns']['guess']",
        "['cooldowns']['highlow']",
        "['cooldowns']['highlow']['default']",
        "['cooldowns']['highlow']['patron']",
        "['cooldowns']['hunt']",
        "['cooldowns']['hunt']['default']",
        "['cooldowns']['hunt']['patron']",
        "['cooldowns']['postmeme']",
        "['cooldowns']['postmeme']['default']",
        "['cooldowns']['postmeme']['patron']",
        "['cooldowns']['search']",
        "['cooldowns']['search']['default']",
        "['cooldowns']['search']['patron']",
        "['cooldowns']['snakeeyes']",
        "['cooldowns']['snakeeyes']['default']",
        "['cooldowns']['snakeeyes']['patron']",
        "['cooldowns']['stream']",
        "['cooldowns']['trivia']",
        "['cooldowns']['trivia']['default']",
        "['cooldowns']['trivia']['patron']",
        "['cooldowns']['vote']",
        "['cooldowns']['work']",
        "['cooldowns']['commands']",
        "['cooldowns']['commands']['enabled']",
        "['cooldowns']['commands']['value']",
        "['custom commands']",
        "['custom commands']['enabled']",
        "['shifts']",
        "['shifts']['enabled']",
        "['auto buy']",
        "['auto buy']['enabled']",
        "['auto buy']['shovel']",
        "['auto buy']['fishing pole']",
        "['auto buy']['hunting rifle']",
        "['auto buy']['keyboard']",
        "['auto buy']['mouse']",
        "['auto buy']['adventure ticket']",
        "['auto trade']",
        "['auto trade']['enabled']",
        "['auto trade']['trader token']",
        "['auto sell']",
        "['auto sell']['enabled']",
        "['typing indicator']",
        "['typing indicator']['enabled']",
        "['typing indicator']['minimum']",
        "['typing indicator']['maximum']",
        "['message delay']['enabled']",
        "['message delay']['minimum']",
        "['message delay']['maximum']",
        "['button delay']['enabled']",
        "['button delay']['minimum']",
        "['button delay']['maximum']",
        "['dropdown delay']['enabled']",
        "['dropdown delay']['minimum']",
        "['dropdown delay']['maximum']",
        "['logging']['debug']",
        "['logging']['warning']",
        "['blacklisted servers']",
        "['blacklisted servers']['enabled']",
        "['blacklisted servers']['servers']",
        "['auto start']",
        "['auto start']['enabled']",
        "['auto start']['channel']",
        "['anti heist']",
        "['anti heist']['enabled']",
        "['auto join heist']",
        "['auto join heist']['enabled']",
        "['auto accept trade']",
        "['auto accept trade']['enabled']",
        "['auto accept trade']['traders']",
        "['settings']",
        "['settings']['prefix']",
        "['settings']['patron']",
        "['settings']['timeout']",
        "['events']['enabled']",
        "['events']['attack the boss by clicking disenfect']",
        "['events']['windows sucks lol']",
        "['events']['why my pls rich no work']",
        "['events']['f']",
        "['events']['frick off karen']",
        "['events']['attack the boss by clicking jerk']",
        "['logging']['webhook logging']",
        "['logging']['webhook logging']['enabled']",
        "['logging']['webhook logging']['url']",
    ]

    try:
        config = utils.Yaml.load(f"{cwd}database/{folder}/config.yml")
    except Exception:
        return False

    try:
        config_template = utils.Yaml.load(f"{cwd}database/templates/config.yml")
    except Exception:
        return False

    for option in options:
        try:
            exec(f"_ = config{option}")

            wrong_type = False

            exec(
                f"if type(config{option}) != type(config_template{option}): wrong_type = True"
            )

            if wrong_type:
                return False
        except KeyError:
            return False

    return True


def verify_database(
    cwd: str,
    folder: Optional[str],
    database_template: Optional[dict] = None,
    database: Optional[dict] = None,
) -> bool:
    """
    The verify_database function verifies that the database.json file is valid.

    Args:
        cwd (str): The current working directory
        folder (Optional[str]): The account's folder to check (or None if the files are specified)
        database_template (Optional[dict]) = None: The database template (or None if the program should read it from the account's folder)
        database (Optional[dict]) = None: The database to check (or None if the prgraom should read it from the account's folder)

    Returns:
        True if the database file is valid, else False
    """

    if folder is not None:
        with open(
            f"{cwd}database/templates/database.json", "r"
        ) as database_template_file:
            database_template = loads(database_template_file.read())

        with open(f"{cwd}database/{folder}/database.json", "r") as database_file:
            try:
                database = loads(database_file.read())
            except JSONDecodeError:
                return False

    for key in database_template:
        try:
            if type(database_template[key]) == dict:
                if not verify_database(
                    cwd, None, database_template[key], database[key]
                ):
                    return False
        except KeyError:
            return False

        if key not in database:
            return False

    return True


def verify_controllers(
    cwd: str,
    folder: str,
) -> bool:
    """
    The verify_controllers function checks to see if the controllers.json file exists in the database folder and then checks to see if it contains a "controllers" key and a "controllers_info" key. If either of these keys are missing, then this function returns False.

    Args:
        cwd (str): The current working directory
        folder (str): The account's folder to check

    Returns:
        True if the controllers file is valid, else False
    """

    with open(f"{cwd}database/{folder}/controllers.json", "r") as controllers_file:
        try:
            controllers = loads(controllers_file.read())
        except JSONDecodeError:
            return False

    return (
        True
        if "controllers" in controllers.keys()
        and "controllers_info" in controllers.keys()
        else False
    )


def verify_info(
    cwd: str,
    folder: str,
) -> bool:
    """
    The verify_info function checks if the info.json file is formatted correctly.

    Args:
        cwd (str): The current working directory
        folder (str): The account's folder to check

    Returns:
        True if the info file is valid, else False
    """

    with open(f"{cwd}database/{folder}/info.json", "r") as info_file:
        try:
            info = loads(info_file.read())
        except JSONDecodeError:
            return False

    if "stats" in info:
        if (
            "commands_ran" not in info["stats"].keys()
            or "buttons_clicked" not in info["stats"].keys()
            or "dropdowns_selected" not in info["stats"].keys()
            or "coins_gained" not in info["stats"].keys()
            or "items_gained" not in info["stats"].keys()
        ):
            return False
    else:
        return False

    return True
