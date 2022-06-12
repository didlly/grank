from typing import Union

from instance.Client import Instance
from utils.Requests import request


def guild_id(Client: Instance) -> Union[bool, str]:
    """
    The guild_id function gets the guild id of the channel id in the account's class

    Args:
        Client (Instance): The Discord client
    """

    req = request(
        f"https://discord.com/api/v10/channels/{Client.channel_id}",
        headers={"authorization": Client.token},
    )

    if req.status_code == 404:
        return False

    elif req.content["type"] != 0:
        return False

    return req.content["guild_id"]
