from random import choice

from utils.Shared import data


def trivia(Client) -> None:
    Client.send_message("pls trivia")

    latest_message = Client.retreive_message("pls trivia")

    try:
        answer = data["trivia"][
            latest_message["embeds"][0]["description"]
            .split("\n")[0]
            .replace("*", "")
            .replace('"', "&quot;")
        ].replace("&quot;", '"')
    except KeyError:
        answer = None
        Client.log(
            "WARNING",
            f"Unknown trivia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Answers: `{latest_message['components'][0]['components']}`.",
        )

    custom_id = None

    for index, possible_answer in enumerate(
        latest_message["components"][0]["components"]
    ):
        if possible_answer["label"] == answer:
            custom_id = latest_message["components"][0]["components"][index][
                "custom_id"
            ]

    if custom_id is None:
        Client.log(
            "WARNING",
            f"Unknown answer to trivia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Answers: `{latest_message['components'][0]['components']}`.",
        )
        custom_id = choice(latest_message["components"][0]["components"])["custom_id"]

    Client.interact_button("pls trivia", custom_id, latest_message)

    latest_message = Client.retreive_message("pls trivia", old_latest_message=latest_message)

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
        coins = "no"

    Client.log(
        "DEBUG",
        f"Received {'⏣ ' if coins != 'no' else ''}{coins} coin{'' if coins == 1 else 's'} from the `pls trivia` command.",
    )
