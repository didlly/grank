from datetime import datetime

from instance.Client import Instance
from scripts.balance import balance


def buy(Client: Instance, item: str) -> bool:
    """
    The buy function is used to buy items from the shop.

    Args:
        Client (Instance): The Discord client
        item (str) The item to buy

    Returns:
        bool: Indicates whether the item was successfully bought or not
    """

    Client.send_message(f"pls buy {item}")

    latest_message = Client.retreive_message(f"pls buy {item}")

    if latest_message["content"] in [
        "your wallet is short on cash, go withdraw some BANK money to make this purchase",
        "Far out, you don't have enough money in your wallet or your bank to buy that much!!",
    ]:
        bank, wallet = balance(Client)

        Client.webhook_log(
            {
                "content": None,
                "embeds": [
                    {
                        "title": "Auto Tool",
                        "url": f"https://discord.com/channels/{Client.guild_id}/{Client.channel_id}/{latest_message['id']}",
                        "color": None,
                        "fields": [
                            {"name": "Bank", "value": f"`{bank}`", "inline": True},
                            {"name": "Wallet", "value": f"`{wallet}`", "inline": True},
                        ],
                        "author": {
                            "name": f"{latest_message['author']['username']}#{latest_message['author']['discriminator']}",
                            "icon_url": f"https://cdn.discordapp.com/avatars/{latest_message['author']['id']}/{latest_message['author']['avatar']}.webp?size=32",
                        },
                        "footer": {
                            "text": Client.username,
                            "icon_url": f"https://cdn.discordapp.com/avatars/{Client.id}/{Client.avatar}.webp?size=32",
                        },
                        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    }
                ],
                "attachments": [],
                "username": "Grank",
                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
            }
        )

        if (wallet + bank) - Client.Repository.database["price"][item] > 0:
            amount = Client.Repository.database["price"][item] - wallet

            Client.send_message(f"pls with {amount}")

            Client.send_message(f"pls buy {item}")

            Client.retreive_message(
                f"pls buy {item}", old_latest_message=latest_message
            )
        else:
            Client.log(
                "WARNING",
                f"Insufficient funds to buy {'an' if item[0] in ['a', 'e', 'i', 'o', 'u'] else 'a'} {item}.",
            )
            Client.webhook_log(
                {
                    "content": None,
                    "embeds": [
                        {
                            "title": "Auto Tool",
                            "description": f"**Insufficient funds** to buy {'an' if item[0] in ['a', 'e', 'i', 'o', 'u'] else 'a'} **{item}**.",
                            "url": f"https://discord.com/channels/{Client.guild_id}/{Client.channel_id}/{latest_message['id']}",
                            "color": None,
                            "author": {
                                "name": f"{latest_message['author']['username']}#{latest_message['author']['discriminator']}",
                                "icon_url": f"https://cdn.discordapp.com/avatars/{latest_message['author']['id']}/{latest_message['author']['avatar']}.webp?size=32",
                            },
                            "footer": {
                                "text": Client.username,
                                "icon_url": f"https://cdn.discordapp.com/avatars/{Client.id}/{Client.avatar}.webp?size=32",
                            },
                            "timestamp": datetime.now().strftime(
                                "%Y-%m-%dT%H:%M:%S.000Z"
                            ),
                        }
                    ],
                    "attachments": [],
                    "username": "Grank",
                    "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                }
            )
            return False

    Client.log("DEBUG", f"Successfully bought {item}.")

    Client.webhook_log(
        {
            "content": None,
            "embeds": [
                {
                    "title": "Auto Tool",
                    "description": f"**Successfully bought** {'an' if item[0] in ['a', 'e', 'i', 'o', 'u'] else 'a'} **{item}**.",
                    "url": f"https://discord.com/channels/{Client.guild_id}/{Client.channel_id}/{latest_message['id']}",
                    "color": None,
                    "author": {
                        "name": f"{latest_message['author']['username']}#{latest_message['author']['discriminator']}",
                        "icon_url": f"https://cdn.discordapp.com/avatars/{latest_message['author']['id']}/{latest_message['author']['avatar']}.webp?size=32",
                    },
                    "footer": {
                        "text": Client.username,
                        "icon_url": f"https://cdn.discordapp.com/avatars/{Client.id}/{Client.avatar}.webp?size=32",
                    },
                    "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                }
            ],
            "attachments": [],
            "username": "Grank",
            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
        }
    )

    return True
