from random import choice

from instance.Client import Instance
from utils.Shared import data


def trivia(Client: Instance) -> bool:
    """
    The trivia function is used to interact with the trivia command

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    Client.send_message("pls trivia")

    latest_message = Client.retreive_message("pls trivia")

    if "description" not in latest_message["embeds"][0]:
        latest_message = Client.fallback_retreive_message("pls trivia")
    elif "seconds to answer" not in latest_message["embeds"][0]["description"]:
        latest_message = Client.fallback_retreive_message("pls trivia")

    try:
        answer = data["trivia"][
            latest_message["embeds"][0]["description"]
            .split("\n")[0]
            .replace("*", "")
            .replace('"', "&quot;")
        ].replace("&quot;", '"')
    except KeyError:
        answer = None

    if answer is None:
        Client.log(
            "WARNING",
            f"Unknown trivia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Answers: `{latest_message['components'][0]['components']}`.",
        )

        custom_id = choice(latest_message["components"][0]["components"])["custom_id"]
    else:
        custom_id = None

        for button in latest_message["components"][0]["components"]:
            if button["label"] == answer:
                custom_id = button["custom_id"]

                break

        if custom_id is None:
            Client.log(
                "WARNING",
                f"Unknown answer to known trivia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Answers: `{latest_message['components'][0]['components']}`.",
            )

            custom_id = choice(latest_message["components"][0]["components"])[
                "custom_id"
            ]

    Client.interact_button("pls trivia", custom_id, latest_message)

    latest_message = Client.retreive_message(
        "pls trivia", old_latest_message=latest_message
    )

    try:
        coins = int(
            "".join(
                filter(
                    str.isdigit,
                    latest_message["content"],
                )
            )
        )
    except Exception:
        coins = 0

    Client.log(
        "DEBUG",
        f"Received {coins} coin{'' if coins == 1 else 's'} from the `pls trivia` command.",
    )

    Client._update_coins("pls trivia", coins)

    return True
