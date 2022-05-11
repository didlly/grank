from random import choice
from time import sleep


def trivia(Client) -> None:
    Client.send_message("pls trivia")

    latest_message = Client.retreive_message("pls trivia")

    try:
        answer = Client.trivia[
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

    sleep(0.5)

    latest_message = Client.retreive_message("pls trivia")

    try:
        coins = (
            int(
                "".join(
                    filter(
                        str.isdigit,
                        latest_message["content"],
                    )
                )
            )
        )
    except Exception:
        coins = "no"

    Client.log(
        "DEBUG",
        f"Received {'⏣ ' if coins != 'no' else ''}{coins} coin{'' if coins == 1 else 's'} from the `pls trivia` command.",
    )
