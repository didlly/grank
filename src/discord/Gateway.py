from typing import Union, Optional
from instance.Client import ButtonInteractError, Instance
from websocket import WebSocket
from json import loads, dumps
from threading import Thread
from utils.Shared import data
import utils.Yaml
from scripts.buy import buy
from instance.ArgumentHandler import parse_args
from discord.GuildId import guild_id
from discord.UserInfo import user_info
from instance.Exceptions import InvalidUserID, IDNotFound, ExistingUserID
from instance.Shifts import shifts
from run import run
from utils.Shared import data
from time import sleep
from platform import python_version
from datetime import datetime
from copy import copy
from psutil import Process
from os import getpid
from sys import exc_info


def convert_size(num, suffix="B"):
    for unit in ["B", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024
    return f"{num:.1f}Yi{suffix}"


def anti_heist(Client, reset) -> None:
    sleep(2.5)

    Client.send_message("pls use phone")
    latest_message = Client.retreive_message("pls use phone")

    if "You don't own this item??" in latest_message["content"]:
        buy(Client, "phone")
        Client.send_message("pls use phone")

    Client.send_message("p")

    if reset:
        del data["channels"][Client.channel_id]
        data["running"].remove(Client.channel_id)

    Client.log("DEBUG", "Successfully averted heist.")


def join_heist(Client, latest_message) -> None:
    Client.log(
        "DEBUG",
        "Heist detected for another user. Joining now.",
    )

    custom_id = latest_message["components"][0]["components"][0]["custom_id"]
    Client.interact_button("pls heist", custom_id, latest_message)

    Client.log("DEBUG", "Joined heist.")


def receive_trade(Client, latest_message) -> None:
    sleep(2.5)

    Client.log(
        "DEBUG",
        f"Received a trade from {latest_message['referenced_message']['author']['username']}#{latest_message['referenced_message']['author']['discriminator']} - accepting now.",
    )

    custom_id = latest_message["components"][0]["components"][-1]["custom_id"]

    Client.interact_button(
        f"{latest_message['referenced_message']['content']}", custom_id, latest_message
    )

    Client.log(
        "DEBUG",
        f"Successfully accepted trade from {latest_message['referenced_message']['author']['username']}#{latest_message['referenced_message']['author']['discriminator']}.",
    )


def event_1(Client, latest_message) -> None:
    Client.log(
        "DEBUG",
        "Detected the `Your immune system is under attack from Covid-19` event. Participating now.",
    )

    custom_id = custom_id = latest_message["components"][0]["components"][0][
        "custom_id"
    ]

    while True:
        try:
            Client.interact_button(
                "Immune System attack event", custom_id, latest_message
            )
            sleep(1)
        except ButtonInteractError:
            return


def event_2(Client, latest_message) -> None:
    Client.log(
        "DEBUG",
        "Detected the `Microsoft is trying to buy Discord again!` event. Participating now.",
    )

    custom_id = custom_id = latest_message["components"][0]["components"][0][
        "custom_id"
    ]

    while True:
        try:
            Client.interact_button(
                "Microsoft buying Discord event", custom_id, latest_message
            )
            sleep(1)
        except ButtonInteractError:
            return


def event_3(Client, latest_message) -> None:
    Client.log(
        "DEBUG",
        "Detected the `pls rich cmd doesn't work` event. Participating now.",
    )

    custom_id = custom_id = latest_message["components"][0]["components"][0][
        "custom_id"
    ]

    while True:
        try:
            Client.interact_button(
                "The pls rich cmd doesn't work event", custom_id, latest_message
            )
            sleep(1)
        except ButtonInteractError:
            return


def send_heartbeat(ws, heartbeat_interval: int) -> None:
    while True:
        try:
            sleep(heartbeat_interval)
            ws.send(dumps({"op": 1, "d": "None"}))
        except Exception:
            return


def event_handler(Client, ws, event: dict) -> None:
    process = Process(getpid())
    process.cpu_percent()

    if Client.Repository.config["shifts"]["enabled"]:
        data[Client.username] = False
        Thread(target=shifts, args=[Client]).start()
    else:
        data[Client.username] = True

    Client.session_id = event["d"]["sessions"][0]["session_id"]
    heist = False

    if Client.Repository.config["auto start"]["enabled"]:
        for index, channel in enumerate(
            Client.Repository.config["auto start"]["channels"]
        ):
            try:
                Client.channel_id = str(channel)
                Client.guild_id = guild_id(Client)

                if Client.guild_id == False:
                    Client.log(
                        "ERROR",
                        f"Autostart channel ID {index + 1} (`{channel}`) is invalid.",
                    )

                if Client.channel_id not in data["channels"]:
                    data["channels"][Client.channel_id] = {}

                data["channels"][Client.channel_id][Client.token] = True
                data["running"].append(Client.channel_id)
                data["channels"][Client.channel_id]["messages"] = []
                New_Client = copy(Client)
                Thread(target=run, args=[New_Client]).start()
            except ValueError:
                Client.log(
                    "ERROR",
                    f"Autostart channel ID {index + 1} (`{channel}`) is invalid.",
                )

    while True:
        try:
            event = loads(ws.recv())

            if event["t"] == "MESSAGE_CREATE":
                length = len(Client.Repository.config["settings"]["prefix"])

                if (
                    event["d"]["content"][:length]
                    == Client.Repository.config["settings"]["prefix"]
                    and len(event["d"]["content"]) > length + 2
                ):

                    if event["d"]["author"]["id"] in Client.Repository.controllers[
                        "controllers"
                    ] and (
                        not Client.Repository.config["blacklisted servers"]["enabled"]
                        or int(event["d"]["guild_id"])
                        not in Client.Repository.config["blacklisted servers"][
                            "servers"
                        ]
                    ):
                        Client.channel_id = event["d"]["channel_id"]
                        Client.Repository.log_command(event["d"]["content"], event["d"])
                        args = parse_args(event["d"]["content"])

                        # Client.send_message(f"***DEBUG:***  `{dumps(parse_args(event['d']['content']).__dict__)}`")

                        if args.command == "help":
                            Client.webhook_send(
                                {
                                    "content": "**Grank** is a Discord self-bot made to automate Dank Memer commands. It supports many of Dank Memer's commands and includes many useful features such as auto-buy and anti-detection.",
                                    "embeds": [
                                        {
                                            "title": "Commands",
                                            "color": None,
                                            "fields": [
                                                {
                                                    "name": "*- `help`*",
                                                    "value": "Shows the help command.",
                                                },
                                                {
                                                    "name": "*- `info`*",
                                                    "value": "Shows information about the bot and the instance.",
                                                },
                                                {
                                                    "name": "*- `start`*",
                                                    "value": "Starts the grinder. Run `grank start -help` for more information.",
                                                },
                                                {
                                                    "name": "*- `stop`*",
                                                    "value": "Stops the grinder. Run `grank stop -help` for more information.",
                                                },
                                                {
                                                    "name": "*- `controllers`*",
                                                    "value": "Edits the controllers for this account. Run `grank controllers -help` for more information.",
                                                },
                                                {
                                                    "name": "*- `config`*",
                                                    "value": "Edits the config for this account. Run `grank config -help` for more information.",
                                                },
                                                {
                                                    "name": "*- `commands`*",
                                                    "value": "Edits the custom commands for this account. Run `grank commands -help` for more information.",
                                                },
                                                {
                                                    "name": "*- `servers`*",
                                                    "value": "Edits the blacklisted servers for this account. Run `grank servers -help` for more information.",
                                                },
                                                {
                                                    "name": "*- `autostart`*",
                                                    "value": "Edits the auto start channels for this account. Run `grank autostart -help` for more information.",
                                                },
                                            ],
                                        },
                                        {
                                            "title": "Useful Links",
                                            "description": "**Github:** https://github.com/didlly/grank\n**Discord:** https://discord.com/invite/X3JMC9FAgy",
                                            "color": None,
                                            "footer": {
                                                "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                            },
                                        },
                                    ],
                                    "username": "Grank",
                                    "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                    "attachments": [],
                                },
                                f"**Grank** is a Discord self-bot made to automate Dank Memer commands. It supports many of Dank Memer's commands and includes many useful features such as auto-buy and anti-detection.\n\n__**Commands:**__\n```yaml\nstart: Starts the grinder. Run 'grank start -help' for more information.\nstop: Stops the grinder. Run 'grank stop -help' for more information.\ncontrollers: Edits the controllers for this account. Run 'grank controllers -help' for more information.\nconfig: Edits the config for this account. Run 'grank config -help' for more information.\ncommands: Edits the custom commands for this account. Run 'grank commands -help' for more information.```\n__**Useful Links:**__\nGithub: https://github.com/didlly/grank\nDiscord: https://discord.com/invite/X3JMC9FAgy",
                            )
                        elif args.command == "info":
                            Client.webhook_send(
                                {
                                    "content": f"**Grank `{Client.current_version}`** runnning on **`Python {python_version()}`**",
                                    "embeds": [
                                        {
                                            "title": "Grank information",
                                            "color": None,
                                            "fields": [
                                                {
                                                    "name": "Active since:",
                                                    "value": f"`{datetime.utcfromtimestamp(Client.startup_time).strftime('%Y-%m-%d %H:%M:%S')}`",
                                                },
                                                {
                                                    "name": "Became active:",
                                                    "value": f"<t:{round(Client.startup_time)}:R>",
                                                },
                                            ],
                                        },
                                        {
                                            "title": "Resource usage information",
                                            "color": None,
                                            "fields": [
                                                {
                                                    "name": "CPU Load:",
                                                    "value": f"`{process.cpu_percent()}%`",
                                                    "inline": True,
                                                },
                                                {
                                                    "name": "Memory Usage:",
                                                    "value": f"`{convert_size(process.memory_info()[0])}`",
                                                    "inline": True,
                                                },
                                            ],
                                        },
                                        {
                                            "title": "Client information",
                                            "color": None,
                                            "fields": [
                                                {
                                                    "name": "Username:",
                                                    "value": f"`{Client.username}`",
                                                    "inline": True,
                                                },
                                                {
                                                    "name": "ID:",
                                                    "value": f"`{Client.id}`",
                                                    "inline": True,
                                                },
                                            ],
                                        },
                                        {
                                            "title": "Session stats",
                                            "color": None,
                                            "fields": [
                                                {
                                                    "name": "Commands ran:",
                                                    "value": f"`{data['stats'][Client.token]['commands_ran']}`",
                                                },
                                                {
                                                    "name": "Buttons clicked:",
                                                    "value": f"`{data['stats'][Client.token]['buttons_clicked']}`",
                                                },
                                                {
                                                    "name": "Dropdowns selected:",
                                                    "value": f"`{data['stats'][Client.token]['dropdowns_selected']}`",
                                                },
                                            ],
                                        },
                                        {
                                            "title": "Lifetime stats",
                                            "color": None,
                                            "fields": [
                                                {
                                                    "name": "Commands ran:",
                                                    "value": f"`{data['stats'][Client.token]['commands_ran'] + Client.Repository.info['stats']['commands_ran']}`",
                                                },
                                                {
                                                    "name": "Buttons clicked:",
                                                    "value": f"`{data['stats'][Client.token]['buttons_clicked']  + Client.Repository.info['stats']['buttons_clicked']}`",
                                                },
                                                {
                                                    "name": "Dropdowns selected:",
                                                    "value": f"`{data['stats'][Client.token]['dropdowns_selected']  + Client.Repository.info['stats']['dropdowns_selected']}`",
                                                },
                                            ],
                                            "footer": {
                                                "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                            },
                                        },
                                    ],
                                    "username": "Grank",
                                    "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                    "attachments": [],
                                },
                                f"**Grank `{Client.current_version}`** running on **`Python {python_version()}`**.\n\n__**Grank Information:**__\nActive since: `{datetime.utcfromtimestamp(Client.startup_time).strftime('%Y-%m-%d %H:%M:%S')}`\nBecame active: <t:{round(Client.startup_time)}:R>\n\n__**Client Information:**__\nUsername: `{Client.username}`\nID: `{Client.id}`\n\n__**Session Stats:**__\nCommands ran: `{data['stats'][Client.token]['commands_ran']}`\nButtons clicked: `{data['stats'][Client.token]['buttons_clicked']}`\nDropdowns selected: `{data['stats'][Client.token]['dropdowns_selected']}`\n\n__**Lifetime Stats:**__\nCommands ran: `{data['stats'][Client.token]['commands_ran'] + Client.Repository.info['stats']['commands_ran']}`\nButtons clicked: `{data['stats'][Client.token]['buttons_clicked'] + Client.Repository.info['stats']['buttons_clicked']}`\nDropdowns selected: `{data['stats'][Client.token]['dropdowns_selected'] + Client.Repository.info['stats']['dropdowns_selected']}`",
                            )
                        elif args.command == "servers":
                            if (
                                len(args.subcommand) == 0
                                and len(args.variables) == 0
                                and len(args.flags) == 0
                            ):
                                if Client.Repository.config["blacklisted servers"][
                                    "enabled"
                                ]:
                                    servers = ""
                                    embed = {
                                        "content": "All **blacklisted servers** for this account.",
                                        "embeds": [],
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    }

                                    for server in Client.Repository.config[
                                        "blacklisted servers"
                                    ]["servers"]:
                                        if server == "enabled":
                                            continue

                                        servers += f"\n{server}"
                                        embed["embeds"].append(
                                            {
                                                "title": f"`{server}`",
                                                "description": "",
                                                "color": None,
                                            }
                                        )

                                    embed["embeds"][-1]["footer"] = {
                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                    }

                                    Client.webhook_send(
                                        embed,
                                        f"__**All blacklisted servers for this account**__\n```yaml{servers}```",
                                    )
                                else:
                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": f"The blacklisted servers option is **not enabled**, so there are **no blacklisted servers!",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        "The blacklisted servers option is not enabled, so there are no blacklisted servers!",
                                    )

                            elif "help" in args.flags:
                                Client.webhook_send(
                                    {
                                        "content": "Help for the command **`servers`**. This command is used to modify the blacklisted servers for this account. Blacklisted servers are saved in the config file, and so are remembered even if you close Grank.",
                                        "embeds": [
                                            {
                                                "title": "Commands",
                                                "color": None,
                                                "fields": [
                                                    {
                                                        "name": "- *`servers`*",
                                                        "value": "Shows a list of all the blacklisted servers for this account.",
                                                    },
                                                    {
                                                        "name": "- *`servers enable`*",
                                                        "value": "Enables the blacklisted server function.",
                                                    },
                                                    {
                                                        "name": "- *`servers disable`*",
                                                        "value": "Disables the blacklisted server function.",
                                                    },
                                                    {
                                                        "name": "- *`servers add 0`*",
                                                        "value": "Adds the server with the ID of `0` to the list of blacklisted servers.",
                                                    },
                                                    {
                                                        "name": "- *`servers remove 0`*",
                                                        "value": "Removes the server with the ID of `0` from the list of blacklisted servers.",
                                                    },
                                                ],
                                                "footer": {
                                                    "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                    "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                },
                                            }
                                        ],
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    },
                                    f"Help for the command **`servers`**. This command is used to modify the blacklisted servers for this account. Blacklisted servers are saved in the config file, and so are remembered even if you close Grank.\n\n__**Commands:**__\n```yaml\nservers: Shows a list of all the blacklisted servers for this account.\nservers add 0: Adds the server with the ID of 0 to the list of blacklisted servers.\nRemoves the server with the ID of 0 from the list of blacklisted servers.\n```",
                                )
                            elif "enable" in args.subcommand:
                                if Client.Repository.config["blacklisted servers"][
                                    "enabled"
                                ]:
                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": "The blacklisted servers option is **already enabled**.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The blacklisted servers option is **already enabled**.",
                                    )
                                else:
                                    Client.Repository.config["blacklisted servers"][
                                        "enabled"
                                    ] = True
                                    Client.Repository.config_write()

                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The blacklisted server option ** was successfully set to `True`**.",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The blacklisted server option ** was successfully set to `True`**.",
                                    )
                            elif "disable" in args.subcommand:
                                if not Client.Repository.config["blacklisted servers"][
                                    "enabled"
                                ]:
                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": "The blacklisted servers option is **already disabled**.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The blacklisted servers option is **already enabled**.",
                                    )
                                else:
                                    Client.Repository.config["blacklisted servers"][
                                        "enabled"
                                    ] = False
                                    Client.Repository.config_write()

                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The blacklisted server option ** was successfully set to `False`**.",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The blacklisted server option ** was successfully set to `False`**.",
                                    )
                            elif "add" in args.subcommand:
                                try:
                                    args.subcommand[-1] = int(args.subcommand[-1])

                                    Client.Repository.config["blacklisted servers"][
                                        "servers"
                                    ].append(args.subcommand[-1])
                                    Client.Repository.config_write()

                                    Client.webhook_send(
                                        {
                                            "content": f"Successfull addition!",
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The guild with the ID of  **`{args.subcommand[1]}`** was **successfully added**.",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The ID **`{args.subcommand[-1]}`** was successfully added to the list of controllers for this account.",
                                    )
                                except ValueError:
                                    Client.webhook_send(
                                        {
                                            "content": f"An error occured while adding the server **`{args.subcommand[-1]}`**.",
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": "IDs contain **only numbers**. The ID you provided contained **other characters**.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"IDs contain **only numbers**. The ID you provided contained **other characters**.",
                                    )
                            elif "remove" in args.subcommand:
                                try:
                                    args.subcommand[-1] = int(args.subcommand[-1])

                                    if (
                                        args.subcommand[-1]
                                        in Client.Repository.config[
                                            "blacklisted servers"
                                        ]["servers"]
                                    ):
                                        Client.Repository.config["blacklisted servers"][
                                            "servers"
                                        ].remove(args.subcommand[-1])
                                        Client.Repository.config_write()

                                        Client.webhook_send(
                                            {
                                                "content": f"Successfull removal!",
                                                "embeds": [
                                                    {
                                                        "title": "Success!",
                                                        "description": f"The guild with the ID of  **`{args.subcommand[1]}`** was **successfully removed**.",
                                                        "color": 65423,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    },
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"The ID **`{args.subcommand[-1]}`** was successfully removed from the list of blacklisted servers for this account.",
                                        )
                                    else:
                                        Client.webhook_send(
                                            {
                                                "content": f"An error occured while removing the server **`{args.subcommand[-1]}`**.",
                                                "embeds": [
                                                    {
                                                        "title": "Error!",
                                                        "description": "The ID you provided was **not found** in the list of blacklisted servers.",
                                                        "color": 16711680,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    }
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"IDs contain **only numbers**. The ID you provided contained **other characters**.",
                                        )
                                except ValueError:
                                    Client.webhook_send(
                                        {
                                            "content": f"An error occured while removing the server **`{args.subcommand[-1]}`**.",
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": "IDs contain **only numbers**. The ID you provided contained **other characters**.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"IDs contain **only numbers**. The ID you provided contained **other characters**.",
                                    )
                        elif args.command == "autostart":
                            if (
                                len(args.subcommand) == 0
                                and len(args.variables) == 0
                                and len(args.flags) == 0
                            ):
                                if Client.Repository.config["auto start"]["enabled"]:
                                    channels = ""
                                    embed = {
                                        "content": "All **auto start channels** for this account.",
                                        "embeds": [],
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    }

                                    for channel in Client.Repository.config[
                                        "auto start"
                                    ]["channels"]:
                                        if channel == "enabled":
                                            continue

                                        channels += f"\n{channel}"
                                        embed["embeds"].append(
                                            {
                                                "title": f"`{channel}`",
                                                "description": "",
                                                "color": None,
                                            }
                                        )

                                    embed["embeds"][-1]["footer"] = {
                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                    }

                                    Client.webhook_send(
                                        embed,
                                        f"__**All auto start channels for this account**__\n```yaml{channels}```",
                                    )
                                else:
                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": f"The auto start channels option is **not enabled**, so there are **no auto start channels**!",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        "The auto start channels option is not enabled, so there are no auto start channels!",
                                    )

                            elif "help" in args.flags:
                                Client.webhook_send(
                                    {
                                        "content": "Help for the command **`channels`**. This command is used to modify the auto start channels for this account. auto start channels are saved in the config file, and so are remembered even if you close Grank.",
                                        "embeds": [
                                            {
                                                "title": "Commands",
                                                "color": None,
                                                "fields": [
                                                    {
                                                        "name": "- *`autostart`*",
                                                        "value": "Shows a list of all the auto start channels for this account.",
                                                    },
                                                    {
                                                        "name": "- *`autostart enable`*",
                                                        "value": "Enables the autostart server function.",
                                                    },
                                                    {
                                                        "name": "- *`autostart disable`*",
                                                        "value": "Disables the autostart server function.",
                                                    },
                                                    {
                                                        "name": "- *`autostart add 0`*",
                                                        "value": "Adds the channel with the ID of `0` to the list of auto start channels.",
                                                    },
                                                    {
                                                        "name": "- *`autostart remove 0`*",
                                                        "value": "Removes the channel with the ID of `0` from the list of auto start channels.",
                                                    },
                                                ],
                                                "footer": {
                                                    "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                    "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                },
                                            }
                                        ],
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    },
                                    f"Help for the command **`channels`**. This command is used to modify the auto start channels for this account. auto start channels are saved in the config file, and so are remembered even if you close Grank.\n\n__**Commands:**__\n```yaml\nchannels: Shows a list of all the auto start channels for this account.\nchannels add 0: Adds the channel with the ID of 0 to the list of auto start channels.\nRemoves the channel with the ID of 0 from the list of auto start channels.\n```",
                                )
                            elif "enable" in args.subcommand:
                                if Client.Repository.config["auto start"]["enabled"]:
                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": "The auto start option is **already enabled**.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The auto start option is **already disabled**.",
                                    )
                                else:
                                    Client.Repository.config["auto start"][
                                        "enabled"
                                    ] = True
                                    Client.Repository.config_write()

                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The auto start option ** was successfully set to `True`**.",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The auto start option ** was successfully set to `True`**.",
                                    )
                            elif "disable" in args.subcommand:
                                if not Client.Repository.config["auto start"][
                                    "enabled"
                                ]:
                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": "The auto start option is **already disabled**.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The auto start option is **already disabled**.",
                                    )
                                else:
                                    Client.Repository.config["auto start"][
                                        "enabled"
                                    ] = False
                                    Client.Repository.config_write()

                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The auto start option ** was successfully set to `False`**.",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The auto start option ** was successfully set to `False`**.",
                                    )
                            elif "add" in args.subcommand:
                                try:
                                    args.subcommand[-1] = int(args.subcommand[-1])

                                    Client.Repository.config["auto start"][
                                        "channels"
                                    ].append(args.subcommand[-1])
                                    Client.Repository.config_write()

                                    Client.webhook_send(
                                        {
                                            "content": f"Successfull addition!",
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The guild with the ID of  **`{args.subcommand[1]}`** was **successfully added**.",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The ID **`{args.subcommand[-1]}`** was successfully added to the list of controllers for this account.",
                                    )
                                except ValueError:
                                    Client.webhook_send(
                                        {
                                            "content": f"An error occured while adding the channel **`{args.subcommand[-1]}`**.",
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": "IDs contain **only numbers**. The ID you provided contained **other characters**.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"IDs contain **only numbers**. The ID you provided contained **other characters**.",
                                    )
                            elif "remove" in args.subcommand:
                                try:
                                    args.subcommand[-1] = int(args.subcommand[-1])

                                    if (
                                        args.subcommand[-1]
                                        in Client.Repository.config["auto start"][
                                            "channels"
                                        ]
                                    ):
                                        Client.Repository.config["auto start"][
                                            "channels"
                                        ].remove(args.subcommand[-1])
                                        Client.Repository.config_write()

                                        Client.webhook_send(
                                            {
                                                "content": f"Successfull removal!",
                                                "embeds": [
                                                    {
                                                        "title": "Success!",
                                                        "description": f"The guild with the ID of  **`{args.subcommand[1]}`** was **successfully removed**.",
                                                        "color": 65423,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    },
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"The ID **`{args.subcommand[-1]}`** was successfully removed from the list of auto start channels channels for this account.",
                                        )
                                    else:
                                        Client.webhook_send(
                                            {
                                                "content": f"An error occured while removing the channel **`{args.subcommand[-1]}`**.",
                                                "embeds": [
                                                    {
                                                        "title": "Error!",
                                                        "description": "The ID you provided was **not found** in the list of auto start channels.",
                                                        "color": 16711680,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    }
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"IDs contain **only numbers**. The ID you provided contained **other characters**.",
                                        )
                                except ValueError:
                                    Client.webhook_send(
                                        {
                                            "content": f"An error occured while removing the channel **`{args.subcommand[-1]}`**.",
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": "IDs contain **only numbers**. The ID you provided contained **other characters**.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"IDs contain **only numbers**. The ID you provided contained **other characters**.",
                                    )

                        elif args.command == "commands":
                            if (
                                len(args.subcommand) == 0
                                and len(args.variables) == 0
                                and len(args.flags) == 0
                            ):
                                commands = ""
                                embed = {
                                    "content": "All **custom commands** for this account.",
                                    "embeds": [],
                                    "username": "Grank",
                                    "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                    "attachments": [],
                                }

                                for command in Client.Repository.config[
                                    "custom commands"
                                ]:
                                    if command == "enabled":
                                        continue

                                    commands += f"\n{command}: {'Enabled' if Client.Repository.config['custom commands'][command]['enabled'] else 'Disabled'}, Cooldown = {Client.Repository.config['custom commands'][command]['cooldown']}"
                                    embed["embeds"].append(
                                        {
                                            "title": f"`{command}`:",
                                            "color": None,
                                            "fields": [
                                                {
                                                    "name": "Enabled:",
                                                    "value": f"`{'Enabled' if Client.Repository.config['custom commands'][command]['enabled'] else 'Disabled'}`",
                                                    "inline": True,
                                                },
                                                {
                                                    "name": "Cooldown:",
                                                    "value": f"`{Client.Repository.config['custom commands'][command]['cooldown']}`",
                                                    "inline": True,
                                                },
                                            ],
                                        }
                                    )

                                embed["embeds"][-1]["footer"] = {
                                    "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                    "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                }

                                Client.webhook_send(
                                    embed,
                                    f"__**All custom commands for this account**__\n```yaml{commands}```",
                                )

                            elif "help" in args.flags:
                                Client.webhook_send(
                                    {
                                        "content": "Help for the command **`commands`**. This command is used to modify the custom commands for this account. Custom commands are set with a cooldown which is tells Grank how often to execute the command. Custom commands are saved in the config file, and so are remembered even if you close Grank.",
                                        "embeds": [
                                            {
                                                "title": "Commands",
                                                "color": None,
                                                "fields": [
                                                    {
                                                        "name": "- *`commands`*",
                                                        "value": "Shows a list of all the custom commands for this account.",
                                                    },
                                                    {
                                                        "name": "- *`commands add pls_help 69`*",
                                                        "value": "Adds the custom command 'pls help' to the list of custom commands and tells Grank it needs to be run every 69 seconds.",
                                                    },
                                                    {
                                                        "name": "- *`commands remove pls_help`*",
                                                        "value": "Removes the custom commands called 'pls help' from the list of custom commands.",
                                                    },
                                                ],
                                                "footer": {
                                                    "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                    "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                },
                                            }
                                        ],
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    },
                                    f"Help for the command **`commands`**. This command is used to modify the custom commands for this account. Custom commands are set with a cooldown which is tells Grank how often to execute the command. Custom commands are saved in the config file, and so are remembered even if you close Grank.\n\n__**Commands:**__\n```yaml\ncommands: Shows a list of all the custom commands for this account.\ncommands add pls_help 69: Adds the custom command 'pls help' to the list of custom commands and tells Grank it needs to be run every 69 seconds.\ncommands remove pls_help: Removes the custom commands called 'pls help' from the list of custom commands.\n```\n**NOTE:** To access custom commands containing a space character, replace the space with an underscore (`_`).",
                                )
                            elif "add" in args.subcommand:
                                args.subcommand[1] = args.subcommand[1].replace(
                                    "_", " "
                                )

                                if (
                                    args.subcommand[1]
                                    in Client.Repository.config[
                                        "custom commands"
                                    ].keys()
                                ):
                                    Client.webhook_send(
                                        {
                                            "content": f"An error occured while adding the custom command **`{args.subcommand[1]}`**.",
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": f"{'Custom commands cannot be called `enabled`.' if args.subcommand[1] == 'enabled' else 'A custom command with that name already exists!'}",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        "Custom commands cannot be called `enabled`."
                                        if args.subcommand[1] == "enabled"
                                        else "A custom command with that name already exists!",
                                    )
                                else:
                                    try:
                                        cooldown = float(args.subcommand[-1])

                                        Client.Repository.config["custom commands"][
                                            args.subcommand[1]
                                        ] = {"cooldown": cooldown, "enabled": False}
                                        Client.Repository.config_write()

                                        Client.webhook_send(
                                            {
                                                "content": f"The custom command **`{args.subcommand[1]}`** was **successfully added**.",
                                                "embeds": [
                                                    {
                                                        "title": "Success!",
                                                        "description": f"The custom command  **`{args.subcommand[1]}`** was **successfully added** with a cooldown of **`{cooldown}`**.",
                                                        "color": 65423,
                                                    },
                                                    {
                                                        "title": "NOTE:",
                                                        "color": None,
                                                        "fields": [
                                                            {
                                                                "name": "To enable the command:",
                                                                "value": f"Run: `grank config.custom_commands.{args.subcommand[1].replace(' ', '_')}.enabled = True`.",
                                                            },
                                                            {
                                                                "name": "To edit the cooldown for the command:",
                                                                "value": f"Run `grank config.custom_commands.{args.subcommand[1].replace(' ', '_')}.cooldown = 0`, replacing `0` with the cooldown you want.",
                                                            },
                                                        ],
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    },
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"The custom command `{args.subcommand[1]}` was successfully added with a cooldown of `{cooldown}` to the list of custom commands.\n\n**NOTE:** To enable the custom command, run `grank config.custom_commands.{args.subcommand[1].replace(' ', '_')}.enabled = True`. To disable the custom command, run `grank config.custom_commands.{args.subcommand[1].replace(' ', '_')}.enabled = False`. To edit the cooldown for the custom command, run `grank config.custom_commands.{args.subcommand[1].replace(' ', '_')}.cooldown = 0`, replacing `0` with the cooldown you want.",
                                        )
                                    except ValueError:
                                        Client.webhook_send(
                                            {
                                                "content": f"An error occured while adding the custom command **`{args.subcommand[1]}`**.",
                                                "embeds": [
                                                    {
                                                        "title": "Error!",
                                                        "description": f"The timeout **`{args.subcommand[-1]}`** is invalid. It has to be an `integer` or a `float`.",
                                                        "color": 16711680,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    }
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"The timeout has to be an integer / float, so Grank knows how often to execute it.",
                                        )
                            elif "remove" in args.subcommand:
                                args.subcommand[1] = args.subcommand[1].replace(
                                    "_", " "
                                )

                                if (
                                    args.subcommand[1]
                                    in Client.Repository.config[
                                        "custom commands"
                                    ].keys()
                                    and args.subcommand[1] != "enabled"
                                ):
                                    del Client.Repository.config["custom commands"][
                                        args.subcommand[1]
                                    ]
                                    Client.Repository.config_write()

                                    Client.webhook_send(
                                        {
                                            "content": f"The custom command **`{args.subcommand[1]}`** was **successfully removed**.",
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The custom command  **`{args.subcommand[1]}`** was **successfully removed**.",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The custom command `{args.subcommand[1]}` was successfully removed from the list of custom commands.",
                                    )
                                else:
                                    Client.webhook_send(
                                        {
                                            "content": f"An error occured while removing the custom command **`{args.subcommand[1]}`**.",
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": f"The custom command **`{args.subcommand[1]}`** was not found.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The custom command you provided was not found.",
                                    )
                        elif args.command == "controllers":
                            if (
                                len(args.subcommand) == 0
                                and len(args.variables) == 0
                                and len(args.flags) == 0
                            ):

                                controllers = ""
                                embed = {
                                    "content": "All **controllers** for this account.",
                                    "embeds": [],
                                    "username": "Grank",
                                    "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                    "attachments": [],
                                }

                                for controller in Client.Repository.controllers[
                                    "controllers"
                                ]:
                                    info = user_info(Client.token, controller)
                                    controllers += f"\n{info.username}#{info.discriminator} - ID: {controller}"
                                    embed["embeds"].append(
                                        {
                                            "title": f"`{info.username}#{info.discriminator}`:",
                                            "color": None,
                                            "fields": [
                                                {
                                                    "name": "ID:",
                                                    "value": f"`{controller}`",
                                                },
                                            ],
                                        }
                                    )

                                embed["embeds"][-1]["footer"] = {
                                    "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                    "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                }

                                Client.webhook_send(
                                    embed,
                                    f"__**Controllers for this account:**__```yaml{controllers}```",
                                )

                            elif "help" in args.flags:
                                Client.webhook_send(
                                    {
                                        "content": "Help for the command **`controllers`**. This command is used to modify the controllers for this account. Controllers are users that can control this instance of Grank through Discord. Controllers are saved in the database file, and so are remembered even if you close Grank.",
                                        "embeds": [
                                            {
                                                "title": "Commands",
                                                "color": None,
                                                "fields": [
                                                    {
                                                        "name": "*- `controllers`*",
                                                        "value": "Shows a list of all the controllers for this account.",
                                                    },
                                                    {
                                                        "name": "*- `controllers purge 0`*",
                                                        "value": "Removes all the logged messages from the controller with the ID of `0`.",
                                                    },
                                                    {
                                                        "name": "*- `controllers info 0`*",
                                                        "value": "Provides information about the controller. This includes information such as when the controller was added, which account added the controller, and what commands the controller has run.",
                                                    },
                                                    {
                                                        "name": "*- `controllers add 0`*",
                                                        "value": "Adds the account with the ID of `0` to the list of controllers.",
                                                    },
                                                    {
                                                        "name": "*- `controllers remove 0`*",
                                                        "value": "Removes the account with the ID of `0` from the list of controllers.",
                                                    },
                                                ],
                                            },
                                            {
                                                "title": "NOTE:",
                                                "description": "You can also **`@mention`** the user instead of providing their ID.",
                                                "color": None,
                                                "footer": {
                                                    "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                    "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                },
                                            },
                                        ],
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    },
                                    f"Help for the command **`controllers`**. This command is used to modify the controllers for this account. Controllers are users that can control this instance of Grank through Discord. Controllers are saved in the database file, and so are remembered even if you close Grank.\n\n__**Commands:**__\n```yaml\ncontrollers: Shows a list of all the controllers for this account.\ncontrollers purge 0: Removes all the logged messages from the controller with the ID of `0`.\ncontrollers info 0: Provides information about the controller. This includes information such as when the controller was added, which account added the controller, and what commands the controller has run.\ncontrollers add 0: Adds the account with the ID of `0` to the list of controllers.\ncontrollers remove 0: Removes the account with the ID of `0` from the list of controllers.\n```\n**NOTE:** You can also @mention accounts instead of providing their ID's.",
                                )
                                continue

                            for index in range(len(args.subcommand)):
                                if "<@" in args.subcommand[index]:
                                    args.subcommand[index] = (
                                        args.subcommand[index]
                                        .replace("<@", "")
                                        .replace(">", "")
                                    )

                            if "info" in args.subcommand:
                                if (
                                    args.subcommand[-1]
                                    in Client.Repository.controllers["controllers"]
                                ):
                                    controller_info = Client.Repository.controllers[
                                        "controllers_info"
                                    ][args.subcommand[-1]]

                                    info = user_info(Client.token, args.subcommand[-1])
                                    adder_info = user_info(
                                        Client.token, controller_info["added_by"]
                                    )

                                    commands = ""
                                    embed = {
                                        "content": f"Information for the controller **`{info.username}#{info.discriminator}`**",
                                        "embeds": [
                                            {
                                                "title": f"`{info.username}#{info.discriminator}`",
                                                "fields": [
                                                    {
                                                        "name": "ID:",
                                                        "value": f"`{args.subcommand[-1]}`",
                                                    },
                                                    {
                                                        "name": "Added by:",
                                                        "value": f"`{adder_info.username}#{adder_info.discriminator} (ID: {controller_info['added_by']})`",
                                                    },
                                                    {
                                                        "name": "Added at:",
                                                        "value": f"`{datetime.utcfromtimestamp(controller_info['added']).strftime('%Y-%m-%d %H:%M:%S')}`",
                                                    },
                                                    {
                                                        "name": "Has been a controller since:",
                                                        "value": f"<t:{round(controller_info['added'])}:R>",
                                                    },
                                                ],
                                            },
                                            {
                                                "title": "",
                                                "fields": [],
                                            },
                                        ],
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    }

                                    for command in controller_info["commands"][::-1]:
                                        commands += f"\n{datetime.utcfromtimestamp(command[0]).strftime('%Y-%m-%d %H:%M:%S')}: {command[-1]}"
                                        embed["embeds"][-1]["fields"].append(
                                            {
                                                "name": f"`{command[-1]}`",
                                                "value": f"<t:{command[0]}:R>",
                                            }
                                        )

                                    if len(commands) > 1500:
                                        commands = "".join(
                                            f"{command}\n"
                                            for command in commands[:1500].split("\n")[
                                                :-1
                                            ]
                                        )

                                    embed["embeds"][-1][
                                        "title"
                                    ] += f"Showing {len(embed['embeds'][-1]['fields'])} commands ran."

                                    Client.webhook_send(
                                        embed,
                                        f"__**Information for the controller `{info.username}#{info.discriminator}` - ID `{args.subcommand[-1]}`:**__\n\n__**General information:**__\nAdded at: `{datetime.utcfromtimestamp(controller_info['added']).strftime('%Y-%m-%d %H:%M:%S')}`\nHas been a controller since: <t:{round(controller_info['added'])}:R>\nAdded by: `{adder_info.username}#{adder_info.discriminator}` - ID `{controller_info['added_by']}`\n\n__**Commands run - {len(controller_info['commands'])} in total (not all may bee shown)**:__```yaml{commands}```",
                                    )
                                else:
                                    Client.webhook_send(
                                        {
                                            "content": f"An error occured while removing the controller **`{args.subcommand[-1]}`**.",
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": f"The controller **`{args.subcommand[-1]}`** was not found in the list of controllers.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The ID you provided was not found in the list of controllers.",
                                    )
                            elif "purge" in args.subcommand:
                                if (
                                    args.subcommand[-1]
                                    in Client.Repository.controllers["controllers"]
                                ):
                                    Client.Repository.controllers["controllers_info"][
                                        args.subcommand[-1]
                                    ]["commands"] = []
                                    Client.Repository.controllers_write()

                                    Client.webhook_send(
                                        {
                                            "content": f"Successful purge!",
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"Successfully purged all logged messages ran by **`{args.subcommand[-1]}`**.",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"Successfully purged all logged commands ran by `{args.subcommand[-1]}`.",
                                    )
                                else:
                                    Client.webhook_send(
                                        {
                                            "content": f"An error occured while purging the logged messages for **`{args.subcommand[1]}`**.",
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": f"The ID **`{args.subcommand[-1]}`** was not found in the list of controllers.",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The ID you provided was not found in the list of controllers.",
                                    )
                            elif "add" in args.subcommand:
                                output = Client.Repository.database_handler(
                                    "write",
                                    "controller add",
                                    args.subcommand[-1],
                                    event["d"]["author"]["id"],
                                )

                                if not output[0]:
                                    if (
                                        output[1] == InvalidUserID
                                        or output[1] == ExistingUserID
                                    ):
                                        Client.webhook_send(
                                            {
                                                "content": f"An error occured while adding the controller **`{args.subcommand[-1]}`**.",
                                                "embeds": [
                                                    {
                                                        "title": "Error!",
                                                        "description": output[-1],
                                                        "color": 16711680,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    }
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"{output[-1]}",
                                        )
                                else:
                                    Client.webhook_send(
                                        {
                                            "content": f"Successfull addition!",
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The controller **`{args.subcommand[1]}`** was **successfully added**.",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The ID **`{args.subcommand[-1]}`** was successfully added to the list of controllers for this account.",
                                    )
                            elif "remove" in args.subcommand:
                                output = Client.Repository.database_handler(
                                    "write", "controller remove", args.subcommand[-1]
                                )

                                if not output[0]:
                                    if output[1] == IDNotFound:
                                        Client.webhook_send(
                                            {
                                                "content": f"An error occured while removing the controller **`{args.subcommand[-1]}`**.",
                                                "embeds": [
                                                    {
                                                        "title": "Error!",
                                                        "description": output[-1],
                                                        "color": 16711680,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    }
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"{output[-1]}",
                                        )
                                else:
                                    Client.webhook_send(
                                        {
                                            "content": f"Successfull removal!",
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The controller **`{args.subcommand[1]}`** was **successfully removed**.",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        f"The ID **`{args.subcommand[-1]}`** was successfully removed from the list of controllers for this account.",
                                    )
                        elif args.command == "start":
                            if "help" in args.flags:
                                Client.webhook_send(
                                    {
                                        "content": f"Help for the command **`start`**. This commands starts the grinder in the channel the command was run. The commands that the grinder executes can be changed through the config file, which can be manipulated through the `grank config` command (if you need help using this command, run `grank config -help`). The grinder automatically responds to special events like `Catch the fish` or `Dodge the fireball`.",
                                        "embeds": None,
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    },
                                    f"Help for the command **`start`**. This commands starts the grinder in the channel the command was run. The commands that the grinder executes can be changed through the config file, which can be manipulated through the `grank config` command (if you need help using this command, run `grank config -help`). The grinder automatically responds to special events like `Catch the fish` or `Dodge the fireball`.",
                                )
                            else:
                                if event["d"]["channel_id"] in data["running"]:
                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": "The grinder **cannot start** in this channel since it is **already running**!",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        "The grinder **cannot start** in this channel since it is **already running**!",
                                    )
                                else:
                                    if Client.channel_id not in data["channels"]:
                                        data["channels"][Client.channel_id] = {Client.token: True, "messages": []}

                                    Client.guild_id = event["d"]["guild_id"]

                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The grinder has **successfully started** in this channel!",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        "The grinder has **successfully started** in this channel!",
                                    )

                                    New_Client = copy(Client)

                                    Thread(target=run, args=[New_Client]).start()

                                    data["running"].append(Client.channel_id)
                        elif args.command == "stop":
                            if "help" in args.flags:
                                Client.webhook_send(
                                    {
                                        "content": f"Help for the command **`stop`**. This commands stops the grinder in the channel the command was run. The grinder was stop after the currently executing command has finished, so if the grinder continues running for a little longer after you run this command, be aware it is intentional behaviour.",
                                        "embeds": None,
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    },
                                    f"Help for the command **`stop`**. This commands stops the grinder in the channel the command was run. The grinder was stop after the currently executing command has finished, so if the grinder continues running for a little longer after you run this command, be aware it is intentional behaviour.",
                                )
                            else:
                                if Client.channel_id in data["running"]:
                                    data["channels"][Client.channel_id][
                                        Client.token
                                    ] = False

                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Success!",
                                                    "description": f"The grinder was **successfully stopped** in this channel!",
                                                    "color": 65423,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                },
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        "The grinder was **successfully stopped** in this channel!",
                                    )

                                    data["running"].remove(Client.channel_id)
                                else:
                                    Client.webhook_send(
                                        {
                                            "embeds": [
                                                {
                                                    "title": "Error!",
                                                    "description": "The grinder **cannot stop** in this channel since it is **not running**!",
                                                    "color": 16711680,
                                                    "footer": {
                                                        "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                        "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                    },
                                                }
                                            ],
                                            "username": "Grank",
                                            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                            "attachments": [],
                                        },
                                        "The grinder **cannot stop** in this channel since it is **not running**!",
                                    )
                        elif args.command == "config":
                            if (
                                len(args.subcommand) == 0
                                and len(args.variables) == 0
                                and len(args.flags) == 0
                            ):
                                Client.webhook_send(
                                    {
                                        "content": f"Configuration file (`/database/{Client.id}/config.yml`):\n```yaml\n{utils.Yaml.dumps(Client.Repository.config)}```",
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    },
                                    f"""Config settings.\n```yaml\n{utils.Yaml.dumps(Client.Repository.config)}```""",
                                )
                            elif "help" in args.flags:
                                Client.webhook_send(
                                    {
                                        "content": "Help for the command **`config`**. This command is used to modify and view the config for this account. The config changes how Grank behaves. For example, you can switch commands on and off using the config command. The config is saved in the config file, and is remembered even if you close Grank.\n\n**NOTE:** To access keys containing a space character, replace the space with an underscore (`_`).",
                                        "embeds": [
                                            {
                                                "title": "Commands",
                                                "color": None,
                                                "fields": [
                                                    {
                                                        "name": "*- `config`*",
                                                        "value": "Shows a list of all the config options and their values for this account.",
                                                    },
                                                    {
                                                        "name": "*- `config reset`*",
                                                        "value": "Resets the config to the default settings.",
                                                    },
                                                    {
                                                        "name": "*- `config.cooldowns.patron`*",
                                                        "value": "Displays the value of the patron key in the subconfig cooldowns.",
                                                    },
                                                    {
                                                        "name": "*- `config.cooldowns.patron = True`*",
                                                        "value": "Sets the patron key in the subconfig cooldowns to True.",
                                                    },
                                                ],
                                                "footer": {
                                                    "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                    "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                },
                                            }
                                        ],
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    },
                                    f"Help for the command **`config`**. This command is used to modify and view the config for this account. The config changes how Grank behaves. For example, you can switch commands on and off using the config command. The config is saved in the config file, and is remembered even if you close Grank.\n\n__**Commands:**__\n```yaml\nconfig: Shows a list of all the config options and their values for this account.\nconfig reset: Resets the config to the default settings.\nconfig.cooldowns.patron: Displays the value of the patron key in the subconfig cooldowns.\nconfig.cooldowns.patrons = True: Sets the patron key in the subconfig cooldowns to True.\n```\n**NOTE:** To access keys containing a space character, replace the space with an underscore (`_`).",
                                )
                            elif "reset" in args.subcommand:
                                Client.Repository.config = utils.Yaml.load(
                                    f"{Client.cwd}database/templates/config.yml"
                                )
                                Client.Repository.config_write()

                                Client.webhook_send(
                                    {
                                        "embeds": [
                                            {
                                                "title": "Success!",
                                                "description": f"The config was **reset** successfully.",
                                                "color": 65423,
                                            },
                                        ],
                                        "username": "Grank",
                                        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                        "attachments": [],
                                    },
                                    "Successfully reset the config!",
                                )
                            elif len(args.variables) > 0:
                                args.variables = [
                                    arg.replace("_", " ") for arg in args.variables
                                ]

                                args.variables = [
                                    f"['{arg}']" for arg in args.variables
                                ]

                                if args.var is None:
                                    try:
                                        value = {}
                                        exec(
                                            f"var = Client.Repository.config{''.join(arg for arg in args.variables)}",
                                            locals(),
                                            value,
                                        )
                                        Client.webhook_send(
                                            {
                                                "embeds": [
                                                    {
                                                        "title": "Success!",
                                                        "description": f"Configuration key **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** is set to **`{value['var']}`**.",
                                                        "color": 65423,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    }
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"Config value **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** is set to **`{value['var']}`**.",
                                        )
                                    except KeyError:
                                        Client.webhook_send(
                                            {
                                                "embeds": [
                                                    {
                                                        "title": "Error!",
                                                        "description": f"Configuration key **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** was **not found**.",
                                                        "color": 16711680,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    }
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"Configuration key **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** was **not found**.",
                                        )
                                else:
                                    args.variables = [
                                        arg.replace("_", " ") for arg in args.variables
                                    ]

                                    try:
                                        exec(
                                            f"Client.Repository.config{''.join(arg for arg in args.variables)} = args.var"
                                        )
                                        Client.webhook_send(
                                            {
                                                "embeds": [
                                                    {
                                                        "title": "Error!",
                                                        "description": f"Configuration value **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** was ** was successfully set** to **`{args.var}`**.",
                                                        "color": 65423,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    }
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"Configuration value **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** was ** was successfully set** to **`{args.var}`**.",
                                        )
                                        Client.Repository.config_write()
                                    except KeyError:
                                        Client.webhook_send(
                                            {
                                                "embeds": [
                                                    {
                                                        "title": "Error!",
                                                        "description": f"Configuration key **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** was **not found**.",
                                                        "color": 16711680,
                                                        "footer": {
                                                            "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                                                            "icon_url": "https://avatars.githubusercontent.com/u/94558954",
                                                        },
                                                    }
                                                ],
                                                "username": "Grank",
                                                "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBkrRNRouYU3p-FddqiIF4TCBeJC032su5Zg&usqp=CAU",
                                                "attachments": [],
                                            },
                                            f"Configuration key **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** was **not found**.",
                                        )
                else:
                    if (
                        f"pls bankrob {Client.username}" in event["d"]["content"]
                        or f"pls heist {Client.username}" in event["d"]["content"]
                        or f"pls bankrob <@{Client.id}>" in event["d"]["content"]
                        or f"pls heist <@{Client.id}>" in event["d"]["content"]
                    ):
                        Client.log(
                            "WARNING",
                            "Possible heist detected - awaiting Dank Memer confirmation.",
                        )
                        heist = True
                    elif event["d"]["author"]["id"] == "270904126974590976":
                        Client.channel_id = event["d"]["channel_id"]

                        if (
                            "Attack the boss by clicking `disinfect`"
                            in event["d"]["content"]
                        ):
                            Thread(target=event_1, args=[Client, event["d"]]).start()
                        elif (
                            "Attack the boss by clicking `windows sucks lol`"
                            in event["d"]["content"]
                        ):
                            Thread(target=event_2, args=[Client, event["d"]]).start()
                        elif (
                            "Attack the boss by clicking `why my pls rich no work?`"
                            in event["d"]["content"]
                        ):
                            Thread(target=event_3, args=[Client, event["d"]]).start()
                        if len(event["d"]["embeds"]) > 0:
                            if (
                                f"<@{Client.id}>" in event["d"]["content"]
                                and "title" in event["d"]["embeds"][0].keys()
                            ):
                                if (
                                    "Pending Confirmation"
                                    in event["d"]["embeds"][0]["title"]
                                    and Client.Repository.config["auto accept trade"][
                                        "enabled"
                                    ]
                                    and event["d"]["referenced_message"]["author"]["id"]
                                    in Client.Repository.config["auto accept trade"][
                                        "traders"
                                    ]
                                ):
                                    Thread(
                                        target=receive_trade, args=[Client, event["d"]]
                                    ).start()
                            if "description" in event["d"]["embeds"][0].keys():
                                if (
                                    "They're trying to break into"
                                    in event["d"]["embeds"][0]["description"]
                                ):
                                    Client.guild_id = guild_id(Client)

                                    if (
                                        f"**{Client.user}**'s"
                                        in event["d"]["embeds"][0]["description"]
                                        and heist
                                        and Client.Repository.config["anti heist"][
                                            "enabled"
                                        ]
                                    ):
                                        Client.log(
                                            "WARNING",
                                            "Heist detected. Calling the cops.",
                                        )

                                        reset = False

                                        if Client.channel_id not in data["channels"]:
                                            data["channels"][Client.channel_id] = {Client.token: True,
                                                "messages": []
                                            }
                                            data["running"].append(Client.channel_id)

                                            reset = True

                                        Thread(
                                            target=anti_heist,
                                            args=[Client, reset],
                                        ).start()

                                        heist = False
                                    elif Client.Repository.config["auto heist"][
                                        "enabled"
                                    ]:
                                        Thread(
                                            target=join_heist,
                                            args=[Client, event["d"]],
                                        ).start()

                    if event["d"]["channel_id"] in data["running"]:
                        data["channels"][event["d"]["channel_id"]]["messages"].append(
                            event["d"]
                        )

                        if (
                            len(data["channels"][event["d"]["channel_id"]]["messages"])
                            > 1
                        ):
                            del data["channels"][event["d"]["channel_id"]]["messages"][
                                0
                            ]
            elif (
                event["t"] == "MESSAGE_UPDATE"
                and event["d"]["channel_id"] in data["running"]
            ):
                found = False

                for index in range(
                    1, len(data["channels"][event["d"]["channel_id"]]["messages"])
                ):
                    latest_message = data["channels"][event["d"]["channel_id"]][
                        "messages"
                    ][-index]

                    if latest_message["id"] == event["d"]["id"]:
                        data["channels"][event["d"]["channel_id"]]["messages"][
                            -index
                        ] = event["d"]
                        found = True
                        break

                if not found:
                    data["channels"][event["d"]["channel_id"]]["messages"].append(
                        event["d"]
                    )

                if len(data["channels"][event["d"]["channel_id"]]["messages"]) > 1:
                    del data["channels"][event["d"]["channel_id"]]["messages"][0]
        except Exception:
            Client.log(
                "WARNING",
                f"An unexpected error occured during the websocket connection (`{exc_info()}`). Assuming gateway disconnect and creating a new connection.",
            )
            Thread(target=gateway, args=[Client]).start()
            return


def gateway(Client: Union[Instance, str]) -> Optional[str]:
    ws = WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=10&encoding=json")
    heartbeat_interval = loads(ws.recv())["d"]["heartbeat_interval"] / 1000

    if type(Client) != str:
        Thread(target=send_heartbeat, args=[ws, heartbeat_interval]).start()

    ws.send(
        dumps(
            {
                "op": 2,
                "d": {
                    "token": Client if type(Client) == str else Client.token,
                    "properties": {
                        "$os": "windows",
                        "$browser": "chrome",
                        "$device": "pc",
                    },
                },
            }
        )
    )

    if type(Client) != str and Client.Repository.config["auto trade"]["enabled"]:
        Client.trader_token_session_id = gateway(
            Client.Repository.config["auto trade"]["trader token"]
        )

    event = loads(ws.recv())

    if event["op"] == 9:
        return gateway(Client if type(Client) == str else Client.token)

    if type(Client) != str:
        Thread(target=event_handler, args=[Client, ws, event]).start()
