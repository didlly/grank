from json import loads

from requests import get
from utils.shared import data


def guild_id(Client):
    """Gets the `guild_id` of the channel specified by the `channel_id` in the `Client` argument.

    Args:
            Client (class): The Client class for the account.

    Returns:
            None
    """

    if len(data["messages"][Client.channel_id]) < 1:
        response = loads(
            get(
                f" https://discord.com/api/v10/channels/{Client.channel_id}/messages?limit=1",
                headers={"authorization": Client.token},
            ).content.decode()
        )

        found = False

        if len(response) != 0:
            for latest_message in response:
                if "message_reference" in latest_message.keys():
                    found = True
                    data[f"{Client.channel_id}_guild"] = latest_message[
                        "message_reference"
                    ]["guild_id"]
                    break
        elif not found:
            Client.send_message("pls beg")

            while True:
                latest_message = Client.retreive_message("pls beg")

                if latest_message is not None:
                    break

            data[f"{Client.channel_id}_guild"] = latest_message["message_reference"][
                "guild_id"
            ]
    else:
        data[f"{Client.channel_id}_guild"] = data["messages"][Client.channel_id][0]["guild_id"]