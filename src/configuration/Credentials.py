from json import load
from json.decoder import JSONDecodeError
from sys import exc_info

from discord.UserInfo import user_info
from utils.Logger import log


def verify_credentials(cwd: str) -> list:
    try:
        credentials = load(open(f"{cwd}credentials.json", "r"))
        log(None, "DEBUG", "Found `credentials.json` and parsed values from it.")
    except FileNotFoundError:
        log(
            None, "ERROR", "Unable to find `credentials.json`. Make sure it is present."
        )
    except JSONDecodeError:
        log(None, "ERROR", f"Credentials file is invalidly formatted - {exc_info()}.")

    if "TOKENS" in credentials:
        log(None, "DEBUG", "Found key `TOKENS` in `credentials.json`.")
    else:
        log(
            None,
            "ERROR",
            "Unable to find key `TOKENS` in `credentials.json`. Make sure it is present.",
        )

    data = []

    for index in range(len(credentials["TOKENS"])):
        info = user_info(credentials["TOKENS"][index])

        if info is None:
            log(
                None,
                "ERROR",
                f"Token {index + 1} (`{credentials['TOKENS'][index]}`) is invalid.",
            )

        data.append(info)

        log(
            f"{info.username}#{info.discriminator}",
            "DEBUG",
            "Logged in successfully.",
        )

    return data
