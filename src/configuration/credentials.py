from json import load, loads

from discord.gateway import gateway
from requests import get
from utils.logger import log


def load_credentials(cwd: str) -> dict:
    """Loads the credentials file (`credentials.json`) and makes sure the required authorization values are present.

    Args:
            cwd (str): The current working directory.

    Returns:
            data (dict): The dictionary version of the json configuration file.
    """

    try:
        credentials = load(open(f"{cwd}credentials.json", "r"))
        log(None, "DEBUG", "Found `credentials.json` and parsed values from it.")
    except FileNotFoundError:
        log(
            None, "ERROR", "Unable to find `credentials.json`. Make sure it is present."
        )

    if "tokens" in credentials.keys():
        log(None, "DEBUG", "Found key `tokens` in `credentials.json`.")
    else:
        log(
            None,
            "ERROR",
            "Unable to find key `tokens` in `credentials.json`. Make sure it is present.",
        )

    if "channel ids" in credentials.keys():
        log(None, "DEBUG", "Found key `channel ids` in `credentials.json`.")
    else:
        log(
            None,
            "ERROR",
            "Unable to find key `channel ids` in `credentials.json`. Make sure it is present.",
        )

    if len(credentials["tokens"]) == 0:
        log(
            None,
            "ERROR",
            "Unable to find values for `tokens` in `credentials.json`. Make sure they are present.",
        )

    if len(credentials["channel ids"]) == 0:
        log(
            None,
            "ERROR",
            "Unable to find values for `channel ids` in `credentials.json`. Make sure they are present.",
        )

    if len(credentials["tokens"]) != len(credentials["channel ids"]):
        log(
            None,
            "ERROR",
            "The amount of tokens and channel ids in `credentials.json` are not the same.",
        )

    data = []

    for index in range(len(credentials["tokens"])):
        request = get(
            "https://discord.com/api/v10/users/@me",
            headers={"authorization": credentials["tokens"][index]},
        )

        if request.status_code != 200:
            log(
                None,
                "ERROR",
                f"Deemed token number {index + 1} invalid. Please double-check you entered a valid token in `configuration.json`.",
            )

        request2 = get(
            f"https://discord.com/api/v10/channels/{credentials['channel ids'][index]}/messages",
            headers={"authorization": credentials["tokens"][index]},
        )

        if request2.status_code == 401:
            log(
                None,
                "ERROR",
                f"Unabled to access channel number {index + 1} with token {index + 1}. Please double-check the specified token has access to that channel.",
            )

        request = loads(request.text)

        data.append(
            [
                request["id"],
                f"{request['username']}#{request['discriminator']}",
                credentials["channel ids"][index],
                credentials["tokens"][index],
            ]
        )

        log(
            None,
            "DEBUG",
            f"Logged in as {request['username']}#{request['discriminator']}.",
        )

    print("")

    return data
