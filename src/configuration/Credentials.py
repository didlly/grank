from json import load
from json.decoder import JSONDecodeError
from sys import exc_info

from discord.UserInfo import user_info
from utils.Logger import log


def verify_credentials(cwd: str) -> list:
    try:
        # Open the credentials file and parse the credentials from it
        credentials = load(open(f"{cwd}credentials.json", "r"))
        log(None, "DEBUG", "Found `credentials.json` and parsed values from it.")
    except FileNotFoundError:
        # If the credentials file does not exist, a FileExistsError would be reaised, which is caught here, and the program will raise an error
        log(
            None, "ERROR", "Unable to find `credentials.json`. Make sure it is present."
        )
    except JSONDecodeError:
        # If there is an error while parsing, a JSONDecodeError would be raised, which is caught here, and the program will raise an error
        log(None, "ERROR", f"Credentials file is invalidly formatted - {exc_info()}.")

    if "TOKENS" in credentials:
        log(None, "DEBUG", "Found key `TOKENS` in `credentials.json`.")
    else:
        # If the key `TOKENS` is not in credentials, the program will raise an error
        log(
            None,
            "ERROR",
            "Unable to find key `TOKENS` in `credentials.json`. Make sure it is present.",
        )

    # Initialize data to an empty list
    data = []

    # For each token in credentials...
    for index in range(len(credentials["TOKENS"])):
        # ...get the information about the account linked to the token
        info = user_info(credentials["TOKENS"][index])

        # If the information is None (i.e, the token is invalid)...
        if info is None:
            # ... the program will raise an error
            log(
                None,
                "ERROR",
                f"Token {index + 1} (`{credentials['TOKENS'][index]}`) is invalid.",
            )

        # Append the account's information to data
        data.append(info)

        log(
            f"{info.username}#{info.discriminator}",
            "DEBUG",
            "Logged in successfully.",
        )

    # Return the information for all of the accounts
    return data
