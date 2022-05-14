from utils.Converter import DictToClass
from datetime import datetime
from utils.Console import fore, style
from utils.Shared import data
from requests import get, post
from json import loads
from random import uniform
from time import sleep, time
from threading import Thread
from copy import copy


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
    def __init__(self, cwd: str, account: DictToClass, current_version) -> None:
        self.cwd = cwd
        self.token = account.token
        self.id = account.id
        self.username = f"{account.username}#{account.discriminator}"
        self.user = account.username
        self.discriminator = account.discriminator
        self.startup_time = int(time())
        self.current_version = current_version
        self.log_file = open(
            f"{cwd}logs/{account.token}/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
            "a",
            errors="ignore",
        )

        self.trivia = loads(
            get(
                "https://raw.githubusercontent.com/didlly/grank/main/src/trivia.json",
                allow_redirects=True,
            ).content
        )

        with open(f"{cwd}current_version", "r") as f:
            self.current_version = f.read()

        Thread(target=self.update).start()

    def update(self) -> None:
        data["stats"][self.token] = {
            "commands_ran": 0,
            "buttons_clicked": 0,
            "dropdowns_selected": 0,
        }

        while "Repository" not in self.__dict__.keys():
            continue

        self.lifetime_commands_ran = self.Repository.info["stats"]["commands_ran"]
        self.lifetime_buttons_clicked = self.Repository.info["stats"]["buttons_clicked"]
        self.lifetime_dropdowns_selected = self.Repository.info["stats"][
            "dropdowns_selected"
        ]

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
            self.Repository.info_write()
            sleep(10)

    def send_message(self, command, token=None, latest_message=None, channel_id=None):
        command = str(command)

        if self.Repository.config["typing indicator"]["enabled"]:
            request = post(
                f"https://discord.com/api/v9/channels/{self.channel_id if channel_id is None else channel_id}/typing",
                headers={"authorization": self.token if token is None else token},
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
            request = post(
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
            )

            if request.status_code in [200, 204]:
                if self.Repository.config["logging"]["debug"]:
                    if "pls" in command:
                        data["stats"][self.token]["commands_ran"] += 1

                    self.log(
                        "DEBUG",
                        f"Successfully sent {'command' if 'pls' in command else 'message'} `{command}`.",
                    )
                return
            else:
                if self.Repository.config["logging"]["warning"]:
                    self.log(
                        "WARNING",
                        f"Failed to send {'command' if 'pls' in command else 'message'} `{command}`. Status code: {request.status_code} (expected 200 or 204).",
                    )
                if request.status_code == 429:
                    request = loads(request.content)
                    if self.Repository.config["logging"]["warning"]:
                        self.log(
                            "WARNING",
                            f"Discord is ratelimiting the self-bot. Sleeping for {request['retry_after']} second(s).",
                        )
                    sleep(request["retry_after"])
                    continue
                raise MessageSendError(
                    f"Failed to send {'command' if 'pls' in command else 'message'} `{command}`. Status code: {request.status_code} (expected 200 or 204)."
                )

    def webhook_send(self, command: dict, fallback_message: str) -> None:
        request = get(
            f"https://discord.com/api/v9/channels/{self.channel_id}/webhooks",
            headers={"authorization": self.token},
        )

        if request.status_code not in [200, 204]:
            self.log(
                "WARNING",
                f"Cannot send webhook in channel {self.channel_id} - Missing Permissions. Resorting to normal message.",
            )
            self.send_message(fallback_message)
            return

        response = loads(request.content)

        if len(response) > 0:
            token = response[0]["token"]
            channel_id = response[0]["id"]
        else:
            request = post(
                f"https://discord.com/api/v9/channels/{self.channel_id}/webhooks",
                headers={"authorization": self.token},
                json={"name": "Spidey Bot"},
            )
            token = loads(request.content)["token"]

            request = get(
                f"https://discord.com/api/v9/channels/{self.channel_id}/webhooks",
                headers={"authorization": self.token},
            )
            channel_id = loads(request.content)[0]["id"]

        while True:
            request = post(
                f"https://discord.com/api/webhooks/{channel_id}/{token}",
                headers={"authorization": self.token},
                json=command,
            )

            if request.status_code in [200, 204]:
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
                        f"Failed to send webhook `{command}`. Status code: {request.status_code} (expected 200 or 204).",
                    )
                if request.status_code == 429:
                    request = loads(request.content)
                    if self.Repository.config["logging"]["warning"]:
                        self.log(
                            "WARNING",
                            f"Discord is ratelimiting the self-bot. Sleeping for {request['retry_after']} second(s).",
                        )
                    sleep(request["retry_after"])
                    continue
                raise WebhookSendError(
                    f"Failed to send webhook `{command}`. Status code: {request.status_code} (expected 200 or 204)."
                )

    def retreive_message(self, command, token=None, check=True):
        while True:
            time = datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
            
            while (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - time
            ).total_seconds() < self.Repository.config["settings"]["timeout"]:
                latest_message = data["channels"][self.channel_id]["messages"][-1]

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
            request = post(
                "https://discord.com/api/v10/interactions",
                headers={"authorization": self.token if token is None else token},
                json=payload,
            )

            if request.status_code in [200, 204]:
                if self.Repository.config["logging"]["debug"]:
                    data["stats"][self.token]["buttons_clicked"] += 1

                    self.log(
                        "DEBUG",
                        f"Successfully interacted with button on Dank Memer's response to command `{command}`.",
                    )
                return
            else:
                if self.Repository.config["logging"]["warning"]:
                    self.log(
                        "WARNING",
                        f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {request.status_code} (expected 200 or 204).",
                    )
                if request.status_code == 429:
                    request = loads(request.content)
                    if self.Repository.config["logging"]["warning"]:
                        self.log(
                            "WARNING",
                            f"Discord is ratelimiting the self-bot. Sleeping for {request['retry_after']} second(s).",
                        )
                    sleep(request["retry_after"])
                    continue

                raise ButtonInteractError(
                    f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {request.status_code} (expected 200 or 204)."
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
            request = post(
                "https://discord.com/api/v10/interactions",
                headers={"authorization": self.token},
                json=payload,
            )

            if request.status_code in [200, 204]:
                if self.Repository.config["logging"]["debug"]:
                    data["stats"][self.token]["dropdowns_selected"] += 1

                    self.log(
                        "DEBUG",
                        f"Successfully interacted with dropdown on Dank Memer's response to command `{command}`.",
                    )
                return
            else:
                if self.Repository.config["logging"]["warning"]:
                    self.log(
                        "WARNING",
                        f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {request.status_code} (expected 200 or 204).",
                    )
                if request.status_code == 429:
                    request = loads(request.content)
                    if self.Repository.config["logging"]["warning"]:
                        self.log(
                            "WARNING",
                            f"Discord is ratelimiting the self-bot. Sleeping for {request['retry_after']} second(s).",
                        )
                    sleep(request["retry_after"])
                    continue
                raise DropdownInteractError(
                    f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {request.status_code} (expected 200 or 204)."
                )

    def clear_lag(self, command: str) -> None:
        """clear_lag()

        - Attempts to stop backlash from failed interactive commands by interacting with the `End Interaction` button on the embed.

        Args:
            command (str): The command that failed to successfully execute.

        Returns:
            interacted (bool): A boolean value that tells Grank whether the button was successfully interacted with or not.
        """

        messages = data["channels"][self.channel_id]["messages"]

        latest_message = messages[0]

        for index in range(1, len(messages)):
            latest_message = messages[-index]

            if latest_message["author"]["id"] == "270904126974590976":
                break

        custom_id = latest_message["components"][0]["components"][-1]["custom_id"]

        return self.interact_button(command, custom_id, latest_message)

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
                f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}"
            )
            exit(1)
