from utils.Requests import request


def guild_id(Client):
    req = request(
        f"https://discord.com/api/v10/channels/{Client.channel_id}",
        headers={"authorization": Client.token},
    )

    if req.status_code == 404:
        return False

    if req.content["type"] != 0:
        return False

    return req.content["guild_id"]
