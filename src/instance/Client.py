from copy import copy
from datetime import datetime
from random import uniform
from time import sleep, time
from typing import Optional

from instance.Exceptions import (
    ButtonInteractError,
    DropdownInteractError,
    MessageSendError,
    ResponseTimeout,
    WebhookSendError,
)
from utils.Console import fore, style
from utils.Converter import DictToClass
from utils.Merge import combine
from utils.Requests import request
from utils.Shared import data


class Instance(object):
    def __init__(self, cwd: str, account: DictToClass) -> None:
        """
        The __init__ function is called when an instance of a class is created.
        It initializes the attributes of the class.

        Args:
            self: Gives access to the class' attributes and methods.
            cwd (str): The current working directory of the program
            account (DictToClass): The account's data class

        Returns:
            NoneType: __init__ functions for classes aren't allowed to return anything, don't ask me why
        """

        self.cwd = cwd
        self.avatar = account.avatar
        self.token = account.token
        self.id = account.id
        self.username = f"{account.username}#{account.discriminator}"
        self.user = account.username
        self.discriminator = account.discriminator

        self.startup_time = int(time())

        self.log_file = open(
            f"{cwd}logs/{data['version']}/{account.token}/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
            "a",
            errors="ignore",
        )

        data["stats"][self.token] = {
            "commands_ran": 0,
            "buttons_clicked": 0,
            "dropdowns_selected": 0,
            "coins_gained": 0,
            "items_gained": {},
        }

    def _update(self) -> bool:
        """
        The _update function is called every 10 seconds when the bot is being run. It updates the lifetime stats of the account, and adds their current session's stats to them.

        Args:
            self: Gives access to the class' attributes and methods.

        Returns:
            bool: Indicates whether the subprogram executed successfully or not
        """

        self.Repository.info["stats"]["commands_ran"] += data["stats"][self.token][
            "commands_ran"
        ]

        self.Repository.info["stats"]["buttons_clicked"] += data["stats"][self.token][
            "buttons_clicked"
        ]

        self.Repository.info["stats"]["dropdowns_selected"] += data["stats"][
            self.token
        ]["dropdowns_selected"]

        self.Repository.info["stats"]["coins_gained"] += data["stats"][self.token][
            "coins_gained"
        ]

        self.Repository.info["stats"]["items_gained"] = combine(
            self.Repository.info["stats"]["items_gained"],
            data["stats"][self.token]["items_gained"],
        )

        self.Repository.info_write()

        return True

    def _update_coins(self, command: str, coins: int) -> bool:
        """
        The _update_coins function is used to update the coins_gained integer in the info file
        It takes two arguments, command and coins. Command is the name of the command that was run, while coins is an integer representing how many coins were gained or lost by running said command.

        Args:
            self: Gives access to the class' attributes and methods.
            command (str): The command ran which was used to gain the coins
            coins (int): The amount of coins received from the command

        Returns:
            True if the coins received from the command is a number and less than 10000, else False
        """

        try:
            coins = int(coins.replace(",", "")) if type(coins) != int else coins
        except ValueError:
            self.log(
                "WARNING",
                f"An error occured while parsing the coins received from the `{command}` command - `{coins}` is not a number.",
            )
            return False

        if coins > 10000 and command != "pls blackjack":
            self.log(
                "WARNING",
                f"A possible error was encountered while parsing the coins received from the `{command}` command - `{coins}` is a large amount.",
            )
            return False

        if coins < 1:
            return False

        data["stats"][self.token]["coins_gained"] += coins

        return True

    def _update_items(self, command: str, item: str) -> bool:
        """
        The _update_items function is used to update the `items_gained` dictionary in the info file.
        It takes two arguments: command and item.
        command is a string that represents what command was run (e.g., `beg` or `crime`).
        item is a string representing which item was gained (e.g., `apple`, `fish`).

        Args:
            self: Gives access to the class' attributes and methods.
            command (str): The command ran which was used to gain the item
            item (int): The item received from that command.

        Returns:
            False if the item is an empty string, has `answered first` in it, is `no items` or is `the shop sale just started!`, else True
        """

        item = item.lower()

        if (
            item
            in [
                "",
                "no items",
                "your immune system is under attack from covid-19",
                "skype is trying to beat discord again!",
                "the shop sale just started!",
                "trivia night",
            ]
            or "answered first" in item
        ):
            return False

        if item.count(" ") > 2:
            self.log(
                "WARNING",
                f"A possible error was encountered while parsing the items received from the `{command}` command - `{item}` seems to be more than 3 words.",
            )
            return False

        if any(char in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] for char in item):
            self.log(
                "WARNING",
                f"A possible error was encountered while parsing the items received from the `{command}` command - `{item}` seems to contain digits.",
            )
            return False

        if item in data["stats"][self.token]["items_gained"]:
            data["stats"][self.token]["items_gained"][item] += 1
        else:
            data["stats"][self.token]["items_gained"][item] = 1

        return True

    def send_message(
        self,
        command: str,
        token: Optional[str] = None,
        latest_message: Optional[dict] = None,
        channel_id: Optional[int] = None,
    ) -> None:
        """
        The send_message function sends a message to the Discord channel.

        Args:
            self: Gives access to the class' attributes and methods.
            command (str): The command to send
            token (Optional[sr]) = None: The token used the send the message (or None if it should be the token in self)
            latest_message (Optional[dict]) = None: Used if the message should reply to another message.
            channel_id (Optional[int]) = None: The channel id used the send the message (or None if it should be the channel id in self)

        Returns:
            None
        """
        command = str(command)

        if self.Repository.config["typing indicator"]["enabled"]:
            req = request(
                f"https://discord.com/api/v9/channels/{self.channel_id if channel_id is None else channel_id}/typing",
                headers={"authorization": self.token if token is None else token},
                method="POST",
            )
            sleep(
                uniform(
                    self.Repository.config["typing indicator"]["minimum"],
                    self.Repository.config["typing indicator"]["maximum"],
                )
            )

        if self.Repository.config["message delay"]["enabled"]:
            sleep(
                uniform(
                    self.Repository.config["message delay"]["minimum"],
                    self.Repository.config["message delay"]["maximum"],
                )
            )

        while True:
            req = request(
                f"https://discord.com/api/v10/channels/{self.channel_id if channel_id is None else channel_id}/messages?limit=1",
                headers={"authorization": self.token if token is None else token},
                json={"content": command}
                if latest_message is None
                else {
                    "content": command,
                    "message_reference": {
                        "guild_id": latest_message["guild_id"],
                        "channel_id": latest_message["channel_id"],
                        "message_id": latest_message["id"],
                    },
                },
                method="POST",
            )

            if 199 < req.status_code < 300:
                if self.Repository.config["logging"]["debug"]:
                    if "pls" in command:
                        data["stats"][self.token]["commands_ran"] += 1

                    self.log(
                        "DEBUG",
                        f"Successfully sent {'command' if 'pls' in command else 'message'} `{command}`.",
                    )
                return
            else:
                if req.status_code == 429:
                    self.log(
                        "WARNING",
                        f"Discord is ratelimiting the self-bot. Sleeping for {req.content['retry_after']} {'second' if req.content['retry_after'] == 1 else 'seconds'}.",
                    )
                    sleep(req.content["retry_after"])
                    continue

                self.log(
                    "WARNING",
                    f"Failed to send {'command' if 'pls' in command else 'message'} `{command}`. Status code: {req.status_code} (expected 200 or 204).",
                )
                raise MessageSendError(
                    f"Failed to send {'command' if 'pls' in command else 'message'} `{command}`. Status code: {req.status_code} (expected 200 or 204)."
                )

    def webhook_send(self, payload: dict, fallback_message: str) -> bool:
        """
        The webhook_send function sends a webhook to the channel specified by self.channel_id with the given payload.
        If Discord is ratelimiting the bot, it will sleep for `req.content['retry_after'] / 1000` seconds and then try again.

        Args:
            self: Gives access to the class' attributes and methods.
            payload (dict): The webhook to be sent
            fallback_message (str): The message to be sent if there is an error sending the webhook (usually if missing permissions). This may be removed in future versions

        Returns:
            bool: Indicates whether the subprogram executed successfully or not
        """

        req = request(
            f"https://discord.com/api/v9/channels/{self.channel_id}/webhooks",
            headers={"authorization": self.token},
        )

        if req.status_code not in [200, 204]:
            self.log(
                "WARNING",
                f"Cannot send webhook in channel {self.channel_id} - Missing Permissions. Resorting to normal message.",
            )
            self.send_message(fallback_message)
            return True

        if "embeds" in payload:
            payload["embeds"][-1]["footer"] = {
                "text": "Bot made by didlly#0302 - https://www.github.com/didlly",
                "icon_url": "https://avatars.githubusercontent.com/u/94558954",
            }

        token = None

        if len(req.content) > 0:
            if "token" in req.content[0]:
                token = req.content[0]["token"]
                channel_id = req.content[0]["id"]

        if token is None:
            req = request(
                f"https://discord.com/api/v9/channels/{self.channel_id}/webhooks",
                headers={"authorization": self.token},
                json={"name": "Spidey Bot"},
                method="POST",
            )
            token = req.content["token"]

            req = request(
                f"https://discord.com/api/v9/channels/{self.channel_id}/webhooks",
                headers={"authorization": self.token},
            )
            channel_id = req.content[0]["id"]

        while True:
            req = request(
                f"https://discord.com/api/webhooks/{channel_id}/{token}",
                headers={"authorization": self.token},
                json=payload,
                method="POST",
            )

            if 199 < req.status_code < 300:
                if self.Repository.config["logging"]["debug"]:
                    self.log(
                        "DEBUG",
                        f"Successfully sent webhook `{payload}`.",
                    )
                return True
            else:
                if self.Repository.config["logging"]["warning"]:
                    self.log(
                        "WARNING",
                        f"Failed to send webhook `{payload}`. Status code: {req.status_code} (expected 200 or 204).",
                    )
                if req.status_code == 429:
                    if self.Repository.config["logging"]["warning"]:
                        self.log(
                            "WARNING",
                            f"Discord is ratelimiting the self-bot. Sleeping for {req.content['retry_after'] / 1000} {'second' if req.content['retry_after'] / 1000 == 1 else 'seconds'}.",
                        )
                    sleep(req.content["retry_after"] / 1000)
                    continue
                raise WebhookSendError(
                    f"Failed to send webhook `{payload}`. Status code: {req.status_code} (expected 200 or 204)."
                )

    def retreive_message(
        self,
        command: str,
        token: Optional[str] = None,
        check: bool = True,
        old_latest_message: Optional[dict] = None,
    ) -> dict:
        """
        The retreive_message function is used to retrieve the latest message from a Discord channel.

        Parameters:

            command (str): The command that was sent to Dank Memer.

            token (Optional[str]): The token used to retreive the message (or None if if it should be the token in self)

            check (bool): Whether or not this function should check for cooldowns and other restrictions in Dank Memer's response before returning it as a dict. Defaults to True, which means it will check for these restrictions and return an error if they are detected; False means no checks will be performed on the response at all, allowing you more control over what is returned by this function without having to manually parse each message yourself.

        Args:
            self: Gives access to the class' attributes and methods.
            command (str): The command the latest message is being retreived for.
            token (Optional[str]) = None: The token used to retreive the message (or None if if it should be the token in self)
            check (bool) = True: Determine whether or not the function should check for restrictions in the response from Dank Memer
            old_latest_message (Optional[dict]) = None: Prevent the bot from getting stuck in an infinite loop or getting the wrong latest message if it can't find a response to its request

        Returns:
            The latest message in the channel
        """

        while True:
            time = datetime.now()
            old_latest_message = (
                copy(data["channels"][self.channel_id]["message"])
                if old_latest_message == None
                else old_latest_message
            )

            while (datetime.now() - time).total_seconds() < self.Repository.config[
                "settings"
            ]["timeout"]:
                latest_message = copy(data["channels"][self.channel_id]["message"])

                if old_latest_message == latest_message:
                    sleep(self.Repository.config["settings"]["timeout"] / 10)
                    continue

                if "referenced_message" in latest_message:
                    if latest_message["referenced_message"] != None:
                        if (
                            latest_message["referenced_message"]["author"]["id"]
                            == self.id
                            and latest_message["author"]["id"] == "270904126974590976"
                            and latest_message["referenced_message"]["content"]
                            == command
                        ):
                            if self.Repository.config["logging"]["debug"]:
                                self.log(
                                    "DEBUG",
                                    f"Got Dank Memer's response to command `{command}`.",
                                )
                            break
                    elif latest_message["author"]["id"] == "270904126974590976":
                        if self.Repository.config["logging"]["debug"]:
                            self.log(
                                "DEBUG",
                                f"Got Dank Memer's response to command `{command}`.",
                            )
                        break
                elif latest_message["author"]["id"] == "270904126974590976":
                    if self.Repository.config["logging"]["debug"]:
                        self.log(
                            "DEBUG",
                            f"Got Dank Memer's response to command `{command}`.",
                        )
                    break

                sleep(self.Repository.config["settings"]["timeout"] / 10)
                old_latest_message = copy(latest_message)

            if latest_message["author"]["id"] != "270904126974590976":
                raise ResponseTimeout(
                    f"Timeout exceeded for response from Dank Memer ({self.Repository.config['settings']['timeout']} {'second' if self.Repository.config['settings']['timeout'] == 1 else 'seconds'}). Aborting command."
                )

            elif len(latest_message["embeds"]) > 0:
                if "description" not in latest_message["embeds"][0]:
                    break

                if (
                    "The default cooldown is"
                    not in latest_message["embeds"][0]["description"]
                ):
                    break

                cooldown = int(
                    "".join(
                        filter(
                            str.isdigit,
                            latest_message["embeds"][0]["description"]
                            .split("**")[1]
                            .split("**")[0],
                        )
                    )
                )
                if self.Repository.config["logging"]["warning"]:
                    self.log(
                        "WARNING",
                        f"Detected cooldown in Dank Memer's response to `{command}`. Sleeping for {cooldown} {'second' if cooldown == 1 else 'seconds'}.",
                    )
                sleep(cooldown)
                self.send_message(command, token if token is not None else None)
                latest_message = self.retreive_message(
                    command, token, check, old_latest_message
                )
            else:
                break

        if (
            len(latest_message["embeds"]) != 0
            and "title" in latest_message["embeds"][0].keys()
            and latest_message["embeds"][0]["title"]
            in ["You're currently bot banned!", "You're currently blacklisted!"]
        ):
            self.log(
                "ERROR",
                "Exiting self-bot instance since Grank has detected the user has been bot banned / blacklisted.",
            )

        if self.Repository.config["auto trade"]["enabled"] and check:
            old_latest_message = copy(latest_message)

            for key in self.Repository.config["auto trade"]:
                if (
                    key == "enabled"
                    or key == "trader token"
                    or not self.Repository.config["auto trade"][key]
                ):
                    continue

                found = False

                if key.lower() in latest_message["content"].lower():
                    found = True
                elif len(latest_message["embeds"]) > 0:
                    if (
                        key.lower()
                        in latest_message["embeds"][0]["description"].lower()
                    ):
                        found = True

                if found:
                    self.log("DEBUG", "Received an item to be autotraded.")

                    self.send_message(
                        f"pls trade 1, 1 {key} <@{self.id}>",
                        self.Repository.config["auto trade"]["trader token"],
                    )

                    latest_message = self.retreive_message(
                        f"pls trade 1, 1 {key} <@{self.id}>",
                        self.Repository.config["auto trade"]["trader token"],
                        False,
                    )

                    if (
                        latest_message["content"]
                        == "You have 0 coins, you can't give them 1."
                    ):
                        self.send_message(
                            f"pls with 1",
                            self.Repository.config["auto trade"]["trader token"],
                        )

                        self.send_message(
                            f"pls trade 1, 1 {key} <@{self.id}>",
                            self.Repository.config["auto trade"]["trader token"],
                        )

                        latest_message = self.retreive_message(
                            f"pls trade 1, 1 {key} <@{self.id}>",
                            self.Repository.config["auto trade"]["trader token"],
                            False,
                        )

                    self.interact_button(
                        f"pls trade 1, 1 {key} <@{self.id}>",
                        latest_message["components"][0]["components"][-1]["custom_id"],
                        latest_message,
                        self.Repository.config["auto trade"]["trader token"],
                        self.trader_token_session_id,
                    )

                    sleep(1)

                    latest_message = self.retreive_message(
                        f"pls trade 1, 1 {key} <@{self.id}>", check=False
                    )

                    self.interact_button(
                        f"pls trade 1, 1 {key} <@{self.id}>",
                        latest_message["components"][0]["components"][-1]["custom_id"],
                        latest_message,
                    )

            return old_latest_message

        elif self.Repository.config["auto sell"]["enabled"] and check:
            for key in self.Repository.config["auto sell"]:
                if key == "enabled" or not self.Repository.config["auto sell"][key]:
                    continue

                found = False

                if key.lower() in latest_message["content"].lower():
                    found = True
                elif len(latest_message["embeds"]) > 0:
                    if (
                        key.lower()
                        in latest_message["embeds"][0]["description"].lower()
                    ):
                        found = True

                if found:
                    self.send_message(f"pls sell {key}")

        return latest_message

    def fallback_retreive_message(self, command: str) -> dict:
        """
        The fallback_retreive_message function is a helper function that is used to retreive the latest message sent by Dank Memer from the Discord channel.
        It does this by making an API call to Discord's servers, and then parsing through all of the messages in order to find one that matches our criteria.
        The criteria for this function is as follows:

            1) The message must be sent by Dank Memer. This ensures we don't get any false positives from other bots or users.
            2) The command must be referenced in the embed title field of said message (e.g., `pls stream`). This ensures we don't get any false negatives from other commands with similar names or unrelated errors/warnings/notifications.

        Args:
            self: Gives access to the class' attributes and methods.
            command (str): The command the latest message is being retreived for

        Returns:
            The latest message sent by Dank Memer in the channel
        """

        req = request(
            f"https://discord.com/api/v10/channels/{self.channel_id}/messages",
            headers={"authorization": self.token},
        )

        for latest_message in req.content:
            if latest_message["author"]["id"] != "270904126974590976" or (
                command != "pls stream"
                and "referenced_message" not in latest_message.keys()
            ):
                continue

            if "referenced_message" in latest_message:
                if (
                    latest_message["referenced_message"]["author"]["id"] != self.id
                    or latest_message["referenced_message"]["content"] != command
                ):
                    continue
            if (
                len(latest_message["embeds"]) != 0
                and "title" in latest_message["embeds"][0].keys()
                and latest_message["embeds"][0]["title"]
                in ["You're currently bot banned!", "You're currently blacklisted!"]
            ):
                self.log(
                    "ERROR",
                    "Exiting self-bot instance since Grank has detected the user has been bot banned / blacklisted.",
                )

            if len(latest_message["embeds"]) > 0:
                if "description" in latest_message["embeds"][0]:
                    if (
                        "The default cooldown is"
                        in latest_message["embeds"][0]["description"]
                    ):
                        cooldown = int(
                            "".join(
                                filter(
                                    str.isdigit,
                                    latest_message["embeds"][0]["description"]
                                    .split("**")[1]
                                    .split("**")[0],
                                )
                            )
                        )
                        self.log(
                            "WARNING",
                            f"Detected cooldown in Dank Memer's response to `{command}`. Sleeping for {cooldown} {'second' if cooldown == 1 else 'seconds'}.",
                        )
                        sleep(cooldown)
                        self.send_message(command)
                        latest_message = self.retreive_message(command)

            return latest_message

    def interact_button(
        self,
        command: str,
        custom_id: int,
        latest_message: dict,
        token: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        """
        The interact_button function sends a POST request to the Discord API, which interacts with a button on Dank Memer's response.

        Parameters:

            command (str): The name of the command that was sent to Discord. This is used for logging purposes only.

            custom_id (int): The ID of the button that should be interacted with on Dank Memer's response message.

            latest_message (dict): The message the button to be interacted with is on.

            token (Optional[str]): The token used to retreive the message (or None if if it should be the token in self)

        Args:
            self: Gives access to the class' attributes and methods.
            command (str): The command is being interacted with
            custom_id (int): The ID of the button that should be interacted with
            latest_message (dict): The message the button to be interacted with is on.
            token (Optional[str]) = None: Pass the token to the function
            session_id (Optional[str]) = None: The sesion id of the account that is interacting with the button.

        Returns:
            Nothing
        """

        payload = {
            "application_id": 270904126974590976,
            "channel_id": self.channel_id,
            "type": 3,
            "data": {"component_type": 2, "custom_id": custom_id},
            "guild_id": latest_message["message_reference"]["guild_id"]
            if "message_reference" in latest_message.keys()
            else self.guild_id,
            "message_flags": 0,
            "message_id": latest_message["id"],
            "session_id": self.session_id if session_id is None else session_id,
        }

        if self.Repository.config["button delay"]["enabled"]:
            sleep(
                uniform(
                    self.Repository.config["button delay"]["minimum"],
                    self.Repository.config["button delay"]["maximum"],
                )
            )

        while True:
            req = request(
                "https://discord.com/api/v10/interactions",
                headers={"authorization": self.token if token is None else token},
                json=payload,
                method="POST",
            )

            if 199 < req.status_code < 300:
                if self.Repository.config["logging"]["debug"]:
                    data["stats"][self.token]["buttons_clicked"] += 1

                    self.log(
                        "DEBUG",
                        f"Successfully interacted with button on Dank Memer's response to command `{command}`.",
                    )
                return
            else:
                if req.status_code == 429:
                    if self.Repository.config["logging"]["warning"]:
                        self.log(
                            "WARNING",
                            f"Discord is ratelimiting the self-bot. Sleeping for {req.content['retry_after']} {'second' if req.content['retry_after'] == 1 else 'seconds'}.",
                        )
                    sleep(req.content["retry_after"])

                    continue

                raise ButtonInteractError(
                    f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {req.status_code} (expected 200 or 204)."
                )

    def interact_dropdown(
        self, command: str, custom_id: int, option_id: str, latest_message: dict
    ):
        """
        The interact_dropdown function is used to interact with a dropdown menu on Dank Memer's response to a command.

        Parameters:

            self (DiscordSelfbot): The DiscordSelfbot instance that is calling the function.

            command (str): The name of the command that was called

            custom_id (int): A unique ID of the dropdown to be selected.

        Args:
            self: Gives access to the class' attributes and methods.
            command (str): The command is being interacted with
            custom_id (int): The ID of the button that should be interacted with
            option_id (str): The ID of the dropdown that should be selected
            latest_message (dict): The message the button to be interacted with is on.

        Returns:
            None
        """

        payload = {
            "application_id": 270904126974590976,
            "channel_id": self.channel_id,
            "type": 3,
            "data": {
                "component_type": 3,
                "custom_id": custom_id,
                "type": 3,
                "values": [option_id],
            },
            "guild_id": latest_message["message_reference"]["guild_id"]
            if "message_reference" in latest_message.keys()
            else self.guild_id,
            "message_flags": 0,
            "message_id": latest_message["id"],
            "session_id": self.session_id,
        }

        if self.Repository.config["dropdown delay"]["enabled"]:
            sleep(
                uniform(
                    self.Repository.config["dropdown delay"]["minimum"],
                    self.Repository.config["dropdown delay"]["maximum"],
                )
            )

        while True:
            req = request(
                "https://discord.com/api/v10/interactions",
                headers={"authorization": self.token},
                json=payload,
                method="POST",
            )

            if 199 < req.status_code < 300:
                if self.Repository.config["logging"]["debug"]:
                    data["stats"][self.token]["dropdowns_selected"] += 1

                    self.log(
                        "DEBUG",
                        f"Successfully interacted with dropdown on Dank Memer's response to command `{command}`.",
                    )
                return
            else:
                if req.status_code == 429:
                    if self.Repository.config["logging"]["warning"]:
                        self.log(
                            "WARNING",
                            f"Discord is ratelimiting the self-bot. Sleeping for {req.content['retry_after']} {'second' if req.content['retry_after'] == 1 else 'seconds'}.",
                        )
                    sleep(req.content["retry_after"])

                    continue
                raise DropdownInteractError(
                    f"Failed to interact with dropdown on Dank Memer's response to command `{command}`. Status code: {req.status_code} (expected 200 or 204)."
                )

    def clear_lag(self, command: str, index1: int = 0, index2: int = -1) -> None:
        """
        The clear_lag function is used to stop possible backlash from Dank Memer commands. It does this
        by finding the latest message from Dank Memer and interacting with the last button on the first row,
        although this can be changed

        Args:
            self: Gives access to the class' attributes and methods.
            command (str): Specify which button to interact with
            index1 (int) = 0: Specify the index of the first component in a message
            index2 (int) = -1: Specify the index of the button in the message

        Returns:
            None
        """

        req = request(
            f"https://discord.com/api/v10/channels/{self.channel_id}/messages",
            headers={"authorization": self.token},
        )

        for message in req.content:
            if (
                message["author"]["id"] != "270904126974590976"
                or len(message["components"]) == 0
            ):
                continue

            for _ in range(0, 2):
                try:
                    custom_id = message["components"][index1]["components"][index2][
                        "custom_id"
                    ]
                    self.interact_button(command, custom_id, message)
                    break
                except ButtonInteractError:
                    continue

    def log(self, level: str, text: str) -> None:
        """
        The log function is used to log messages.

        Args:
            self: Gives access to the class' attributes and methods.
            level (str): The level of the log message
            text (str): The log message

        Returns:
            None
        """

        if "Repository" in self.__dict__:
            if level == "DEBUG" and not self.Repository.config["logging"]["debug"]:
                return
            elif (
                level == "WARNING" and not self.Repository.config["logging"]["warning"]
            ):
                return

        time = datetime.now().strftime("[%x-%X]")

        print(
            f"{time}{f' - {fore.Bright_Magenta}{self.username}{style.RESET_ALL}' if self.username is not None else ''} - {style.Italic}{fore.Bright_Red if level == 'ERROR' else fore.Bright_Blue if level == 'DEBUG' else fore.Bright_Yellow}[{level}]{style.RESET_ALL} | {text}"
        )

        self.log_file.write(
            f"{time}{f' - {self.username}' if self.username is not None else ''} - [{level}] | {text}\n"
        )
        self.log_file.flush()

        if level == "ERROR":
            input(
                f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}\n"
            )
            exit(1)

    def webhook_log(self, payload: dict) -> None:
        """
        The webhook_log function is used to send a webhook log to the webhook logging URL

        Args:
            self: Gives access to the class' attributes and methods.
            payload (dict): The data to be sent to the webhook

        Returns:
            None
        """

        if not self.Repository.config["logging"]["webhook logging"]["enabled"]:
            return

        while True:
            req = request(
                self.Repository.config["logging"]["webhook logging"]["url"],
                json=payload,
                method="POST",
            )

            if 199 < req.status_code < 300:
                if self.Repository.config["logging"]["debug"]:
                    self.log(
                        "DEBUG",
                        f"Successfully sent webhook `{payload}`.",
                    )
                return
            else:
                if self.Repository.config["logging"]["warning"]:
                    self.log(
                        "WARNING",
                        f"Failed to send webhook `{payload}`. Status code: {req.status_code} (expected 200 or 204).",
                    )
                if req.status_code == 429:
                    if self.Repository.config["logging"]["warning"]:
                        self.log(
                            "WARNING",
                            f"Discord is ratelimiting the self-bot. Sleeping for {req.content['retry_after'] / 1000} {'second' if req.content['retry_after'] / 1000 == 1 else 'seconds'}.",
                        )
                    sleep(req.content["retry_after"] / 1000)
                    continue
                raise WebhookSendError(
                    f"Failed to send webhook `{payload}`. Status code: {req.status_code} (expected 200 or 204)."
                )
