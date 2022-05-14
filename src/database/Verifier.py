from os.path import isdir, isfile
from json.decoder import JSONDecodeError
import utils.Yaml
from json import loads
from typing import Union, Optional
from instance.Client import Instance
from database.Handler import create_config, create_database, create_controllers


def verify(cwd: str, account, Client: Instance) -> None:
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

    if False in statuses:
        Client.log("WARNING", "Database is corrupted. Rebuilding now.")

        if statuses[0] is False:
            Client.log("DEBUG", f"Rebuilding `/database/{Client.id}/config.yml")
            create_config(cwd, Client.id)

        if statuses[1] is False:
            Client.log("DEBUG", f"Rebuilding `/database/{Client.id}/database.json")
            create_database(cwd, Client.id)

        if statuses[-1] is False:
            Client.log("DEBUG", f"Rebuilding `/database/{Client.id}/controllers.json")
            create_controllers(cwd, account)


def verify_config(cwd: str, folder: str) -> bool:
    options = [
        "['commands']",
        "['commands']['adventure']",
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
        "['commands']['work']",
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
        "['auto start']['channels']",
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
            try:
                database = loads(database_file.read())
            except JSONDecodeError:
                return False

    for key in database_template.keys():
        if type(database_template[key]) == dict:
            if not verify_database(cwd, None, database_template[key], database[key]):
                return False

        if key not in database.keys():
            return False

    return True


def verify_controllers(
    cwd: str,
    folder: Union[None, str],
) -> bool:
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
