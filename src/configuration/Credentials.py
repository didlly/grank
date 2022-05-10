from json import load
from utils.Logger import log
from discord.UserInfo import user_info


def verify_credentials(cwd: str) -> list:
    try:
        credentials = load(open(f"{cwd}credentials.json", "r"))
        log(None, "DEBUG", "Found `credentials.json` and parsed values from it.")
    except FileNotFoundError:
        log(
            None, "ERROR", "Unable to find `credentials.json`. Make sure it is present."
        )

    if "TOKENS" in credentials.keys():
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
        else:
            data.append(info)
            log(
                f"{info.username}#{info.discriminator}",
                "DEBUG",
                "Logged in successfully.",
            )

    return data
