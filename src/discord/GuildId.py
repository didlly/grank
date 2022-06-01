from typing import Union

from instance.Client import Instance
from utils.Requests import request


def guild_id(Client: Instance) -> Union[bool, str]:
    """
    The guild_id function gets the guild id of the channel id in the account's class

    Args:
        Client (Instance): The Discord client
    """

    # Send a request to the Discord API
    req = request(
        f"https://discord.com/api/v10/channels/{Client.channel_id}",
        headers={"authorization": Client.token},
    )

    # If the channel was not found...
    if req.status_code == 404:
        # ...return False
        return False

    # Else if the channel is not a server channel (e.g., `dm`, `group dm`)...
    elif req.content["type"] != 0:
        # ...return False
        return False

    # Otherwise, return the guild id.
    return req.content["guild_id"]
