from os import listdir
from os.path import isdir, isfile
from shutil import rmtree
import utils.Yaml
from json import loads
from typing import Union, Optional
from instance.Client import Instance
from database.Handler import create_config, create_database


def verify(cwd: str, Client: Instance) -> None:
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

    if not isfile(f"{cwd}database/{Client.id}/info.json"):
        statuses.append(False)
    else:
        statuses.append(verify_info(cwd, Client.id))

    if False in statuses:
        if statuses[-1] is False:
            rmtree(f"{cwd}database/{Client.id}")

        if statuses[0] is False:
            create_config(cwd, Client.id)

        if statuses[1] is False:
            create_database(cwd, Client.id)


def verify_config(cwd: str, folder: str) -> bool:
    options = [
        "['commands']",
        "['commands']['crime']",
        "['commands']['daily']",
        "['commands']['beg']",
        "['commands']['fish']",
        "['commands']['guess']",
        "['commands']['hunt']",
        "['commands']['dig']",
        "['commands']['search']",
        "['commands']['highlow']",
        "['commands']['postmeme']",
        "['commands']['trivia']",
        "['commands']['vote']",
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
        "['custom commands']",
        "['custom commands']['enabled']",
        "['shifts']",
        "['shifts']['enabled']",
        "['shifts']['active']",
        "['shifts']['passive']",
        "['auto buy']",
        "['auto buy']['enabled']",
        "['auto buy']['shovel']",
        "['auto buy']['fishing pole']",
        "['auto buy']['hunting rifle']",
        "['auto buy']['keyboard']",
        "['auto buy']['mouse']",
        "['auto trade']",
        "['auto trade']['enabled']",
        "['auto trade']['trader token']",
        "['typing indicator']",
        "['typing indicator']['enabled']",
        "['typing indicator']['minimum']",
        "['typing indicator']['maximum']",
        "['cooldowns']",
        "['cooldowns']['patron']",
        "['cooldowns']['timeout']",
        "['logging']['debug']",
        "['logging']['warning']",
    ]

    config = utils.Yaml.load(f"{cwd}database/{folder}/config.yml")

    for option in options:
        try:
            exec(f"_ = config{option}")
        except KeyError:
            return False

    return True


def verify_database(
    cwd: str,
    folder: Union[None, str],
    database_template: Optional[dict] = None,
    database: Optional[dict] = None,
) -> bool:
    if folder is not None:
        with open(
            f"{cwd}database/templates/database.json", "r"
        ) as database_template_file:
            database_template = loads(database_template_file.read())

        with open(f"{cwd}database/{folder}/database.json", "r") as database_file:
            database = loads(database_file.read())

    for key in database_template.keys():
        if type(key) == dict:
            output = verify_database(cwd, None, database_template[key], database[key])

            if not output:
                return False

        if key not in database.keys():
            return False

    return True


def verify_info(
    cwd: str,
    folder: Union[None, str],
    info_template: Optional[dict] = None,
    info: Optional[dict] = None,
) -> bool:
    with open(f"{cwd}database/{folder}/info.json", "r") as info_file:
        info = loads(info_file.read())

    return True if "controllers" in info.keys() else False
