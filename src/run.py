from scripts.beg import beg
from scripts.blackjack import blackjack
from scripts.crime import crime
from scripts.custom import custom
from scripts.daily import daily
from scripts.dig import dig
from scripts.fish import fish
from scripts.guess import guess
from scripts.highlow import highlow
from scripts.hunt import hunt
from scripts.lottery import lottery
from scripts.postmeme import postmeme
from scripts.search import search
from scripts.snakeeyes import snakeeyes
from scripts.stream import stream
from scripts.trivia import trivia
from scripts.vote import vote
from scripts.work import work

from utils.Shared import data
from datetime import datetime
from sys import exc_info


def run(Client):
    (
        last_beg,
        last_blackjack,
        last_crime,
        last_dig,
        last_fish,
        last_guess,
        last_highlow,
        last_hunt,
        last_postmeme,
        last_search,
        last_snakeeyes,
        last_trivia,
    ) = ["01/01/22-00:00:00"] * 12

    while True:
        if (
            Client.Repository.config["commands"]["beg"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_beg, "%x-%X")
                ).total_seconds()
                > 25
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_beg, "%x-%X")
            ).total_seconds() > 45:
                try:
                    beg(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls beg` command: `{exc_info()}`.",
                        )

                last_beg = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["blackjack"]["enabled"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_blackjack, "%x-%X")
                ).total_seconds()
                > 5
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_blackjack, "%x-%X")
            ).total_seconds() > 10:
                try:
                    blackjack(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls blackjack` command: `{exc_info()}`.",
                        )

                        try:
                            Client.clear_lag("pls blackjack")
                        except Exception:
                            Client.log(
                                "WARNING",
                                f"Failed to clear lag from the `pls blackjack` command failing: `{exc_info()}`. Backlash expected (if commands keep failing after this, it would be advisable to close Grank, wait a few minutues, and re-open Grank).",
                            )

                last_blackjack = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["commands"]["crime"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_crime, "%x-%X")
                ).total_seconds()
                > 15
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_crime, "%x-%X")
            ).total_seconds() > 45:
                try:
                    crime(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls crime` command: `{exc_info()}`.",
                        )

                        try:
                            Client.clear_lag("pls crime")
                        except Exception:
                            Client.log(
                                "WARNING",
                                f"Failed to clear lag from the `pls crime` command failing: `{exc_info()}`. Backlash expected (if commands keep failing after this, it would be advisable to close Grank, wait a few minutues, and re-open Grank).",
                            )

                last_crime = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["commands"]["daily"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(Client.Repository.database["daily"], "%x-%X")
            ).total_seconds() > 23400:
                try:
                    daily(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls daily` command: `{exc_info()}`.",
                        )

                Client.Repository.database["daily"] = datetime.now().strftime("%x-%X")
                Client.Repository.database_write()

                if Client.Repository.config["logging"]["debug"]:
                    Client.log(
                        "DEBUG",
                        "Successfully updated latest command run of `pls daily`.",
                    )

        if (
            Client.Repository.config["commands"]["dig"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_dig, "%x-%X")
                ).total_seconds()
                > 25
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_dig, "%x-%X")
            ).total_seconds() > 45:
                try:
                    dig(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls dig` command: `{exc_info()}`.",
                        )

                last_dig = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["commands"]["fish"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_fish, "%x-%X")
                ).total_seconds()
                > 25
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_fish, "%x-%X")
            ).total_seconds() > 45:
                try:
                    fish(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls fish` command: `{exc_info()}`.",
                        )

                last_fish = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["commands"]["guess"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_guess, "%x-%X")
            ).total_seconds() > 60:
                try:
                    guess(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls guess` command: `{exc_info()}`.",
                        )

                    Client.send_message("end")

                last_guess = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["commands"]["highlow"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_highlow, "%x-%X")
                ).total_seconds()
                > 15
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_highlow, "%x-%X")
            ).total_seconds() > 30:
                try:
                    highlow(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls highlow` command: `{exc_info()}`.",
                        )

                        try:
                            Client.clear_lag("pls highlow")
                        except Exception:
                            Client.log(
                                "WARNING",
                                f"Failed to clear lag from the `pls highlow` command failing: `{exc_info()}`. Backlash expected (if commands keep failing after this, it would be advisable to close Grank, wait a few minutues, and re-open Grank).",
                            )

                last_highlow = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["commands"]["hunt"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_hunt, "%x-%X")
                ).total_seconds()
                > 25
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_hunt, "%x-%X")
            ).total_seconds() > 40:
                try:
                    hunt(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls hunt` command: `{exc_info()}`.",
                        )

                last_hunt = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["lottery"]["enabled"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(Client.Repository.database["lottery"], "%x-%X")
            ).total_seconds() > Client.Repository.config["lottery"]["cooldown"]:
                try:
                    lottery(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls lottery` command: `{exc_info()}`.",
                        )

                        try:
                            Client.clear_lag("pls lottery")
                        except Exception:
                            Client.log(
                                "WARNING",
                                f"Failed to clear lag from the `pls lottery` command failing: `{exc_info()}`. Backlash expected (if commands keep failing after this, it would be advisable to close Grank, wait a few minutues, and re-open Grank).",
                            )

                Client.Repository.database["lottery"] = datetime.now().strftime("%x-%X")
                Client.Repository.database_write()

                if Client.Repository.config["logging"]["debug"]:
                    Client.log(
                        "DEBUG",
                        "Successfully updated latest command run of `pls lottery`.",
                    )

        if (
            Client.Repository.config["commands"]["postmeme"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_postmeme, "%x-%X")
                ).total_seconds()
                > 45
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_postmeme, "%x-%X")
            ).total_seconds() > 50:
                try:
                    postmeme(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls postmeme` command: `{exc_info()}`.",
                        )

                        try:
                            Client.clear_lag("pls postmeme")
                        except Exception:
                            Client.log(
                                "WARNING",
                                f"Failed to clear lag from the `pls postmeme` command failing: `{exc_info()}`. Backlash expected (if commands keep failing after this, it would be advisable to close Grank, wait a few minutues, and re-open Grank).",
                            )

                last_postmeme = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["commands"]["search"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_search, "%x-%X")
                ).total_seconds()
                > 15
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_search, "%x-%X")
            ).total_seconds() > 30:
                try:
                    search(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls search` command: `{exc_info()}`.",
                        )

                        try:
                            Client.clear_lag("pls search")
                        except Exception:
                            Client.log(
                                "WARNING",
                                f"Failed to clear lag from the `pls search` command failing: `{exc_info()}`. Backlash expected (if commands keep failing after this, it would be advisable to close Grank, wait a few minutues, and re-open Grank).",
                            )

                last_search = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["snakeeyes"]["enabled"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_snakeeyes, "%x-%X")
                ).total_seconds()
                > 5
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_snakeeyes, "%x-%X")
            ).total_seconds() > 10:
                try:
                    snakeeyes(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls snakeeyes` command: `{exc_info()}`.",
                        )

                last_snakeeyes = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["stream"]["enabled"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(Client.Repository.database["stream"], "%x-%X")
            ).total_seconds() > 600:
                try:
                    stream(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls stream` command: `{exc_info()}`.",
                        )

                        try:
                            Client.clear_lag("pls stream")
                        except Exception:
                            Client.log(
                                "WARNING",
                                f"Failed to clear lag from the `pls stream` command failing: `{exc_info()}`. Backlash expected (if commands keep failing after this, it would be advisable to close Grank, wait a few minutues, and re-open Grank).",
                            )

                Client.Repository.database["stream"] = datetime.now().strftime("%x-%X")
                Client.Repository.database_write()

                if Client.Repository.config["logging"]["debug"]:
                    Client.log(
                        "DEBUG",
                        "Successfully updated latest command run of `pls stream`.",
                    )

        if (
            Client.Repository.config["commands"]["trivia"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                Client.Repository.config["cooldowns"]["patron"]
                and (
                    datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                    - datetime.strptime(last_trivia, "%x-%X")
                ).total_seconds()
                > 3
            ) or (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(last_trivia, "%x-%X")
            ).total_seconds() > 5:
                try:
                    trivia(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls trivia` command: `{exc_info()}`.",
                        )

                        try:
                            Client.clear_lag("pls trivia")
                        except Exception:
                            Client.log(
                                "WARNING",
                                f"Failed to clear lag from the `pls trivia` command failing: `{exc_info()}`. Backlash expected (if commands keep failing after this, it would be advisable to close Grank, wait a few minutues, and re-open Grank).",
                            )

                last_trivia = datetime.now().strftime("%x-%X")

        if (
            Client.Repository.config["commands"]["vote"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(Client.Repository.database["vote"], "%x-%X")
            ).total_seconds() > 43200:
                try:
                    vote(Client)
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls vote` command: `{exc_info()}`.",
                        )

                Client.Repository.database["vote"] = datetime.now().strftime("%x-%X")
                Client.Repository.database_write()

                if Client.Repository.config["logging"]["debug"]:
                    Client.log(
                        "DEBUG",
                        "Successfully updated latest command run of `pls vote`.",
                    )
        if (
            Client.Repository.config["commands"]["work"]
            and data[Client.username]
            and data["channels"][Client.channel_id][Client.token]
        ):
            if (
                datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
                - datetime.strptime(Client.Repository.database["work"], "%x-%X")
            ).total_seconds() > 3600:
                try:
                    output = work(Client)

                    if output is None:
                        cooldown = datetime.now().strftime("%x-%X")
                    else:
                        cooldown = datetime.strptime(
                            output, "%Y-%m-%d %H:%M:%S"
                        ).strftime("%x-%X")
                except Exception:
                    if Client.Repository.config["logging"]["warning"]:
                        cooldown = datetime.now().strftime("%x-%X")

                        Client.log(
                            "WARNING",
                            f"An unexpected error occured during the running of the `pls work` command: `{exc_info()}`.",
                        )

                Client.Repository.database["work"] = cooldown
                Client.Repository.database_write()

                if Client.Repository.config["logging"]["debug"]:
                    Client.log(
                        "DEBUG",
                        "Successfully updated latest command run of `pls work`.",
                    )

        if Client.Repository.config["custom commands"]["enabled"]:
            for key in Client.Repository.config["custom commands"]:

                if key == "enabled":
                    continue
                if Client.Repository.config["custom commands"][key]["enabled"]:
                    try:
                        exec(
                            f"if (datetime.strptime(datetime.now().strftime('%x-%X'), '%x-%X') - datetime.strptime(custom_{key.replace(' ', '_')}, '%x-%X')).total_seconds() > Client.Repository.config['custom commands'][key]['cooldown']: custom(Client, key); custom_{key.replace(' ', '_')} = datetime.now().strftime('%x-%X')"
                        )

                    except NameError:
                        custom(Client, key)

                        exec(
                            f"custom_{key.replace(' ', '_')} = datetime.now().strftime('%x-%X')"
                        )

        while (
            not data[Client.username]
            or not data["channels"][Client.channel_id][Client.token]
        ):
            if not data["channels"][Client.channel_id][Client.token]:
                Client.Repository.info["stats"]["commands_ran"] = (
                    Client.lifetime_commands_ran
                    + data["stats"][Client.token]["commands_ran"]
                )
                Client.Repository.info["stats"]["buttons_clicked"] = (
                    Client.lifetime_buttons_clicked
                    + data["stats"][Client.token]["buttons_clicked"]
                )
                Client.Repository.info["stats"]["dropdowns_selected"] = (
                    Client.lifetime_dropdowns_selected
                    + data["stats"][Client.token]["dropdowns_selected"]
                )
                Client.Repository.info_write()
                return
