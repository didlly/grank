from json import load, loads
from utils.logger import log
from requests import get
from discord.gateway import gateway

def load_credentials(cwd):
    try:
        credentials = load(open(f"{cwd}/credentials.json", "r"))
        log(None, "DEBUG", "Found `credentials.json` and parsed values from it.")
    except FileNotFoundError:
        log(None, "ERROR", "Unable to find `credentials.json`. Make sure it is present.")

    if "tokens" in credentials.keys():
        log(None, "DEBUG", "Found key `tokens` in `credentials.json`.")
    else:
        log(None, "ERROR", "Unable to find key `tokens` in `credentials.json`. Make sure it is present.")

    if "channel_ids" in credentials.keys():
        log(None, "DEBUG", "Found key `channel_ids` in `credentials.json`.")
    else:
        log(None, "ERROR", "Unable to find key `channel_ids` in `credentials.json`. Make sure it is present.")

    if len(credentials["tokens"]) > 1:
        log(None, "ERROR", "Unable to find values for `tokens` in `credentials.json`. Make sure they are present.")

    if len(credentials["channel_ids"]) > 1:
        log(None, "ERROR", "Unable to find values for `channel_ids` in `credentials.json`. Make sure they are present.")

    if len(credentials["tokens"]) != len(credentials["channel_ids"]):
        log(None, "ERROR", "The amount of tokens and channel_ids in `credentials.json` are not the same.")

    data = []

    for index in range(len(credentials["tokens"])):
        request = get("https://discord.com/api/v9/users/@me", headers={"authorization": credentials["tokens"][index]})

        if request.status_code != 200:
            log(None, "ERROR", f"Deemed token number {index + 1} invalid. Please double-check you entered a valid token in `configuration.json`.")

        request = loads(request.text)

        data.append([request["id"], f"{request['username']}#{request['discriminator']}", gateway(credentials["tokens"][index]), credentials["channel_ids"][index], credentials["tokens"][index]])

        log(None, "DEBUG", f"Logged in as {request['username']}#{request['discriminator']}.")

    print("")

    return data