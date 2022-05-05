from typing import Union, Optional
from instance.Client import Instance
from database.Handler import Database
from websocket import WebSocket
from json import loads, dumps
from threading import Thread
from utils.Shared import data
import utils.Yaml
from contextlib import suppress
from instance.ArgumentHandler import parse_args
from discord.UserInfo import user_info
from instance.Exceptions import InvalidUserID, IDNotFound, ExistingUserID
from run import run
from utils.Shared import data
from discord.GuildId import guild_id
from time import sleep
from os import remove
from database.Handler import create_config
from platform import python_version, system, release, machine
from datetime import datetime
from copy import copy
import sys


def send_heartbeat(ws, heartbeat_interval: int) -> None:
    while True:
        with suppress(Exception):
            sleep(heartbeat_interval)
            ws.send(dumps({"op": 1, "d": "null"}))


def event_handler(Client, ws, event: dict) -> None:
    Client.session_id = event["d"]["sessions"][0]["session_id"]

    while True:
        with suppress(Exception):
            event = loads(ws.recv())

            if event["t"] == "MESSAGE_CREATE":
                if (
                    event["d"]["content"][:5].lower() == "grank"
                    and len(event["d"]["content"]) > 6
                ):
                    if (
                        event["d"]["author"]["id"]
                        in Client.Repository.info["controllers"]
                    ):

                        Client.channel_id = event["d"]["channel_id"]
                        Client.Repository.log_command(event["d"]["content"], event["d"])
                        args = parse_args(event["d"]["content"])

                        # Client.send_message(f"***DEBUG:***  `{dumps(parse_args(event['d']['content']).__dict__)}`")

                        if args.command == "help":
                            Client.send_message(
                                f"**Grank** is a Discord self-bot made to automate Dank Memer commands. It supports many of Dank Memer's commands and includes many useful features such as auto-buy and anti-detection.\n\n__**Commands:**__\n```yaml\nstart: Starts the grinder. Run 'grank start -help' for more information.\nstop: Stops the grinder. Run 'grank stop -help' for more information.\ncontrollers: Edits the controllers for this account. Run 'grank controllers -help' for more information.\nconfig: Edits the config for this account. Run 'grank config -help' for more information.\ncommands: Edits the custom commands for this account. Run 'grank commands -help' for more information.```\n__**Useful Links:**__\nGithub: https://github.com/didlly/grank\nDiscord: https://discord.com/invite/X3JMC9FAgy\n\n__**System Information:**__\nOS: {system()}.\nOS Release: {release()}.\nOS Architecture: {'64-Bit' if machine().endswith('64') else '32-Bit'}.",
                                latest_message=event["d"],
                            )
                        elif args.command == "info":
                            Client.Repository.info = loads(
                                open(
                                    f"{Client.cwd}database/{Client.id}/info.json", "r"
                                ).read()
                            )

                            Client.send_message(
                                f"**Grank `{Client.current_version}`** running on **`Python {python_version()}`**.\n\n__**Grank Information:**__\nActive since: `{datetime.utcfromtimestamp(Client.startup_time).strftime('%Y-%m-%d %H:%M:%S')}`\nBecame active: <t:{round(Client.startup_time)}:R>\nRunning from source: `{False if getattr(sys, 'frozen', False) else True}`\n\n__**Client Information:**__\nUsername: `{Client.username}`\nID: `{Client.id}`\n\n__**Session Stats:**__\nCommands ran: `{data['stats'][Client.token]['commands_ran']}`\nButtons clicked: `{data['stats'][Client.token]['buttons_clicked']}`\nDropdowns selected: `{data['stats'][Client.token]['dropdowns_selected']}`\n\n__**Lifetime Stats:**__\nCommands ran: `{data['stats'][Client.token]['commands_ran'] + Client.Repository.info['stats']['commands_ran']}`\nButtons clicked: `{data['stats'][Client.token]['buttons_clicked'] + Client.Repository.info['stats']['buttons_clicked']}`\nDropdowns selected: `{data['stats'][Client.token]['dropdowns_selected'] + Client.Repository.info['stats']['dropdowns_selected']}`",
                                latest_message=event["d"],
                            )
                        elif args.command == "commands":
                            if (
                                len(args.subcommand) == 0
                                and len(args.variables) == 0
                                and len(args.flags) == 0
                            ):
                                commands = ""

                                for command in Client.Repository.config[
                                    "custom commands"
                                ]:
                                    if command == "enabled":
                                        continue

                                    commands += f"\n{command}: {'Enabled' if Client.Repository.config['custom commands'][command]['enabled'] else 'Disabled'}, Cooldown = {Client.Repository.config['custom commands'][command]['cooldown']}"

                                Client.send_message(
                                    f"__**All custom commands for this account**__\n```yaml{commands}```",
                                    latest_message=event["d"],
                                )

                            elif "help" in args.flags:
                                Client.send_message(
                                    f"Help for the command **`commands`**. This command is used to modify the custom commands for this account. Custom commands are set with a cooldown which is tells Grank how often to execute the command. Custom commands are saved in the config file, and so are remembered even if you close Grank.\n\n__**Commands:**__\n```yaml\ncommands: Shows a list of all the custom commands for this account.\ncommands add pls_help 69: Adds the custom command 'pls help' to the list of custom commands and tells Grank it needs to be run every 69 seconds.\ncommands remove pls_help: Removes the custom commands called 'pls help' from the list of custom commands.\n```\n**NOTE:** To access custom commands containing a space character, replace the space with an underscore (`_`).",
                                    latest_message=event["d"],
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
                                    Client.send_message(
                                        "Custom commands cannot be called `enabled`."
                                        if args.subcommand[1] == "enabled"
                                        else "A custom command with that name already exists!",
                                        latest_message=event["d"],
                                    )
                                else:
                                    try:
                                        cooldown = float(args.subcommand[-1])

                                        Client.Repository.config["custom commands"][
                                            args.subcommand[1]
                                        ] = {"cooldown": cooldown, "enabled": False}
                                        Client.Repository.config_write()

                                        Client.send_message(
                                            f"The custom command `{args.subcommand[1]}` was successfully added with a cooldown of `{cooldown}` to the list of custom commands.\n\n**NOTE:** To enable the custom command, run `grank config.custom_commands.{args.subcommand[1].replace(' ', '_')}.enabled = True`. To disable the custom command, run `grank config.custom_commands.{args.subcommand[1].replace(' ', '_')}.enabled = False`. To edit the cooldown for the custom command, run `grank config.custom_commands.{args.subcommand[1].replace(' ', '_')}.cooldown = 0`, replacing `0` with the cooldown you want.",
                                            latest_message=event["d"],
                                        )
                                    except TypeError:
                                        Client.send_message(
                                            f"The timeout has to be an integer / float, so Grank knows how often to execute it.",
                                            latest_message=event["d"],
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

                                    Client.send_message(
                                        f"The custom command `{args.subcommand[1]}` was successfully removed from the list of custom commands.",
                                        latest_message=event["d"],
                                    )
                                else:
                                    Client.send_message(
                                        f"The custom command you provided was not found in the list of custom commands.",
                                        latest_message=event["d"],
                                    )
                        elif args.command == "controllers":
                            if (
                                len(args.subcommand) == 0
                                and len(args.variables) == 0
                                and len(args.flags) == 0
                            ):

                                controllers = ""

                                for controller in Client.Repository.info["controllers"]:
                                    info = user_info(Client.token, controller)
                                    controllers += f"\n{info.username}#{info.discriminator} - ID: {controller}"

                                Client.send_message(
                                    f"__**Controllers for this account:**__```yaml{controllers}```",
                                    latest_message=event["d"],
                                )

                            elif "help" in args.flags:
                                Client.send_message(
                                    f"Help for the command **`controllers`**. This command is used to modify the controllers for this account. Controllers are users that can control this instance of Grank through Discord. Controllers are saved in the database file, and so are remembered even if you close Grank.\n\n__**Commands:**__\n```yaml\ncontrollers: Shows a list of all the controllers for this account.\ncontrollers purge 0: Removes all the logged messages from the controller with the ID of `0`.\ncontrollers info 0: Provides information about the controller. This includes information such as when the controller was added, which account added the controller, and what commands the controller has run.\ncontrollers add 0: Adds the account with the ID of `0` to the list of controllers.\ncontrollers remove 0: Removes the account with the ID of `0` from the list of controllers.\n```\n**NOTE:** You can also @mention accounts instead of providing their ID's.",
                                    latest_message=event["d"],
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
                                    in Client.Repository.info["controllers"]
                                ):
                                    controller_info = Client.Repository.info[
                                        "controllers_info"
                                    ][args.subcommand[-1]]

                                    info = user_info(Client.token, args.subcommand[-1])
                                    adder_info = user_info(
                                        Client.token, controller_info["added_by"]
                                    )

                                    commands = ""

                                    for command in controller_info["commands"][::-1]:
                                        commands += f"\n{datetime.utcfromtimestamp(command[0]).strftime('%Y-%m-%d %H:%M:%S')}: {command[-1]}"

                                    if len(commands) > 1500:
                                        commands = "".join(
                                            f"{command}\n"
                                            for command in commands[:1500].split("\n")[
                                                :-1
                                            ]
                                        )

                                    Client.send_message(
                                        f"__**Information for the controller `{info.username}#{info.discriminator}` - ID `{args.subcommand[-1]}`:**__\n\n__**General information:**__\nAdded at: `{datetime.utcfromtimestamp(controller_info['added']).strftime('%Y-%m-%d %H:%M:%S')}`\nHas been a controller since: <t:{round(controller_info['added'])}:R>\nAdded by: `{adder_info.username}#{adder_info.discriminator}` - ID `{controller_info['added_by']}`\n\n__**Commands run - {len(controller_info['commands'])} in total (not all may bee shown)**:__```yaml{commands}```",
                                        latest_message=event["d"],
                                    )
                                else:
                                    Client.send_message(
                                        f"The ID you provided was not found in the list of controllers.",
                                        latest_message=event["d"],
                                    )
                            elif "purge" in args.subcommand:
                                if (
                                    args.subcommand[-1]
                                    in Client.Repository.info["controllers"]
                                ):
                                    Client.Repository.info["controllers_info"][
                                        args.subcommand[-1]
                                    ]["commands"] = []
                                    Client.Repository.info_write()

                                    Client.send_message(
                                        f"Successfully purged all logged commands ran by `{args.subcommand[-1]}`.",
                                        latest_message=event["d"],
                                    )
                                else:
                                    Client.send_message(
                                        f"The ID you provided was not found in the list of controllers.",
                                        latest_message=event["d"],
                                    )
                            elif "add" in args.subcommand:
                                output = Client.Repository.database_handler(
                                    "write",
                                    "controller add",
                                    args.subcommand[-1],
                                    event["d"]["author"]["id"],
                                )

                                if not output[0]:
                                    if output[1] == InvalidUserID:
                                        Client.send_message(
                                            f"{output[-1]}", latest_message=event["d"]
                                        )
                                    elif output[1] == ExistingUserID:
                                        Client.send_message(
                                            f"{output[-1]}", latest_message=event["d"]
                                        )
                                else:
                                    Client.send_message(
                                        f"The ID **`{args.subcommand[-1]}`** was successfully added to the list of controllers for this account.",
                                        latest_message=event["d"],
                                    )
                            elif "remove" in args.subcommand:
                                output = Client.Repository.database_handler(
                                    "write", "controller remove", args.subcommand[-1]
                                )

                                if not output[0]:
                                    if output[1] == IDNotFound:
                                        Client.send_message(
                                            f"{output[-1]}", latest_message=event["d"]
                                        )
                                else:
                                    Client.send_message(
                                        f"The ID **`{args.subcommand[-1]}`** was successfully removed from the list of controllers for this account.",
                                        latest_message=event["d"],
                                    )
                        elif args.command == "start":
                            if "help" in args.flags:
                                Client.send_message(
                                    f"Help for the command **`start`**. This commands starts the grinder in the channel the command was run. The commands that the grinder executes can be changed through the config file, which can be manipulated through the `grank config` command (if you need help using this command, run `grank config -help`). The grinder automatically responds to special events like `Catch the fish` or `Dodge the fireball`.",
                                    latest_message=event["d"],
                                )
                            else:
                                if event["d"]["channel_id"] in data["running"]:
                                    Client.send_message(
                                        f"Grinder cannot start in this channel since the bot is running!",
                                        latest_message=event["d"],
                                    )
                                else:
                                    if Client.channel_id not in data["channels"]:
                                        data["channels"][Client.channel_id] = {}

                                    data["channels"][Client.channel_id][
                                        Client.token
                                    ] = True

                                    Client.guild_id = guild_id(Client)

                                    Client.send_message(
                                        f"Grinder successfully started in this channel!",
                                        latest_message=event["d"],
                                    )

                                    New_Client = copy(Client)

                                    Thread(target=run, args=[New_Client]).start()

                                    data["running"].append(event["d"]["channel_id"])

                                    data["channels"][event["d"]["channel_id"]][
                                        "messages"
                                    ] = []
                        elif args.command == "stop":
                            if "help" in args.flags:
                                Client.send_message(
                                    f"Help for the command **`stop`**. This commands stops the grinder in the channel the command was run. The grinder was stop after the currently executing command has finished, so if the grinder continues running for a little longer after you run this command, be aware it is intentional behaviour.",
                                    latest_message=event["d"],
                                )
                            else:
                                if event["d"]["channel_id"] in data["running"]:
                                    data["channels"][Client.channel_id][
                                        Client.token
                                    ] = False

                                    Client.send_message(
                                        f"Grinder successfully stopped in this channel!",
                                        latest_message=event["d"],
                                    )

                                    data["running"].remove(event["d"]["channel_id"])
                                else:
                                    Client.send_message(
                                        f"Grinder cannot stop in this channel since the bot is not running!",
                                        latest_message=event["d"],
                                    )
                        elif args.command == "config":
                            if (
                                len(args.subcommand) == 0
                                and len(args.variables) == 0
                                and len(args.flags) == 0
                            ):
                                message = f"""Config settings.\n```yaml\n{utils.Yaml.dumps(Client.Repository.config)}```"""
                                Client.send_message(message, latest_message=event["d"])
                            elif "help" in args.flags:
                                Client.send_message(
                                    f"Help for the command **`config`**. This command is used to modify and view the config for this account. The config changes how Grank behaves. For example, you can switch commands on and off using the config command. The config is saved in the config file, and is remembered even if you close Grank.\n\n__**Commands:**__\n```yaml\nconfig: Shows a list of all the config options and their values for this account.\nconfig reset: Resets the config to the default settings.\nconfig.cooldowns.patron: Displays the value of the patron key in the subconfig cooldowns.\nconfig.cooldowns.patrons = True: Sets the patron key in the subconfig cooldowns to True.\n```\n**NOTE:** To access keys containing a space character, replace the space with an underscore (`_`).",
                                    latest_message=event["d"],
                                )
                            elif "reset" in args.subcommand:
                                remove(f"{Client.cwd}database/{Client.id}/config.yml")
                                _, Client.Repository.config = create_config(
                                    Client.cwd, Client.id
                                )
                                Client.send_message(
                                    f"Successfully reset the config!",
                                    latest_message=event["d"],
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
                                        Client.send_message(
                                            f"Config value **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** is set to **`{value['var']}`**."
                                        )
                                    except KeyError:
                                        Client.send_message(
                                            f"Config value **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** was not found.",
                                            latest_message=event["d"],
                                        )
                                else:
                                    args.variables = [
                                        arg.replace("_", " ") for arg in args.variables
                                    ]

                                    try:
                                        exec(
                                            f"_ = Client.Repository.config{''.join(arg for arg in args.variables)}"
                                        )
                                        exec(
                                            f"Client.Repository.config{''.join(arg for arg in args.variables)} = {args.var}"
                                        )
                                        Client.send_message(
                                            f"Config value **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** was successfully set to **{args.var}**.",
                                            latest_message=event["d"],
                                        )
                                        Client.Repository.config_write()
                                    except KeyError:
                                        Client.send_message(
                                            f"Config value **`{'.'.join(arg[2:][:-2] for arg in args.variables)}`** was not found.",
                                            latest_message=event["d"],
                                        )
                else:
                    if event["d"]["channel_id"] in data["running"]:
                        data["channels"][event["d"]["channel_id"]]["messages"].append(
                            event["d"]
                        )

                        if (
                            len(data["channels"][event["d"]["channel_id"]]["messages"])
                            > 10
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

                if len(data["channels"][event["d"]["channel_id"]]["messages"]) > 10:
                    del data["channels"][event["d"]["channel_id"]]["messages"][0]


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

    return event["d"]["sessions"][0]["session_id"]
