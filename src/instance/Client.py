from copy import copy
from datetime import datetime
from random import uniform
from threading import Thread
from time import sleep, time
from typing import Optional

from utils.Console import fore, style
from utils.Converter import DictToClass
from utils.Merge import combine
from utils.Requests import request
from utils.Shared import data


class MessageSendError(Exception):
    pass


class WebhookSendError(Exception):
    pass


class ResponseTimeout(Exception):
    pass


class ButtonInteractError(Exception):
    pass


class DropdownInteractError(Exception):
    pass


class Instance(object):
    def __init__(self, cwd: str, account: DictToClass) -> None:
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

        Thread(target=self._update).start()

    def _update(self) -> None:
        data["stats"][self.token] = {
            "commands_ran": 0,
            "buttons_clicked": 0,
            "dropdowns_selected": 0,
            "coins_gained": 0,
            "items_gained": {},
        }

        while "Repository" not in self.__dict__.keys():
            continue

        self.lifetime_commands_ran = self.Repository.info["stats"]["commands_ran"]
        self.lifetime_buttons_clicked = self.Repository.info["stats"]["buttons_clicked"]
        self.lifetime_dropdowns_selected = self.Repository.info["stats"][
            "dropdowns_selected"
        ]
        self.lifetime_coins_gained = self.Repository.info["stats"]["coins_gained"]
        self.lifetime_items_gained = self.Repository.info["stats"]["items_gained"]

        while True:
            self.Repository.info["stats"]["commands_ran"] = (
                self.lifetime_commands_ran + data["stats"][self.token]["commands_ran"]
            )
            self.Repository.info["stats"]["buttons_clicked"] = (
                self.lifetime_buttons_clicked
                + data["stats"][self.token]["buttons_clicked"]
            )
            self.Repository.info["stats"]["dropdowns_selected"] = (
                self.lifetime_dropdowns_selected
                + data["stats"][self.token]["dropdowns_selected"]
            )
            self.Repository.info["stats"]["coins_gained"] = (
                self.lifetime_coins_gained + data["stats"][self.token]["coins_gained"]
            )
            self.Repository.info["stats"]["items_gained"] = combine(
                self.lifetime_items_gained, data["stats"][self.token]["items_gained"]
            )

            self.Repository.info_write()
            sleep(10)

    def _update_coins(self, command: str, coins: int) -> bool:
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

    def _update_items(self, command: str, item: int) -> bool:
        item = item.lower()

        if item in [
            "",
            "no items",
            "your immune system is under attack from covid-19",
            "the shop sale just started!"
            or "answered first!" in item
        ]:
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

    def send_message(self, command, token=None, latest_message=None, channel_id=None):
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

    def webhook_send(self, command: dict, fallback_message: str) -> None:
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
            return

        if len(req.content) > 0:
            token = req.content[0]["token"]
            channel_id = req.content[0]["id"]
        else:
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
                json=command,
                method="POST",
            )

            if 199 < req.status_code < 300:
                if self.Repository.config["logging"]["debug"]:
                    self.log(
                        "DEBUG",
                        f"Successfully sent webhook `{command}`.",
                    )
                return
            else:
                if self.Repository.config["logging"]["warning"]:
                    self.log(
                        "WARNING",
                        f"Failed to send webhook `{command}`. Status code: {req.status_code} (expected 200 or 204).",
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
                    f"Failed to send webhook `{command}`. Status code: {req.status_code} (expected 200 or 204)."
                )

    def retreive_message(
        self, command, token=None, check=True, old_latest_message: Optional[dict] = None
    ) -> dict:
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

                if "referenced_message" in latest_message.keys():
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
                raise TimeoutError(
                    f"Timeout exceeded for response from Dank Memer ({self.Repository.config['settings']['timeout']} {'second' if self.Repository.config['settings']['timeout'] == 1 else 'seconds'}). Aborting command."
                )

            elif len(latest_message["embeds"]) > 0:
                if "description" not in latest_message["embeds"][0].keys():
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

            if "referenced_message" in latest_message.keys():
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
                if "description" in latest_message["embeds"][0].keys():
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
        self, command, custom_id, latest_message, token=None, session_id=None
    ):
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

    def interact_dropdown(self, command, custom_id, option_id, latest_message):
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
        if "Repository" in self.__dict__.keys():
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
            _ = input(
                f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}\n"
            )
            exit(1)

    def webhook_log(self, payload: dict) -> None:
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
