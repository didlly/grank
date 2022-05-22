from json import loads
from requests import get


def guild_id(Client):
    req = get(
        f"https://discord.com/api/v10/channels/{Client.channel_id}",
        headers={"authorization": Client.token},
    )

    if req.status_code == 404:
        return False

    response = loads(req.content.decode())

    if response["type"] != 0:
        return False

    return response["guild_id"]
