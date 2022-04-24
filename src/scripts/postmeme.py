from random import choice
from time import sleep


def postmeme(Client) -> None:
    """One of the basic 7 currency commands - `pls postmeme`.

    Required item(s): None

    Args:
            Client (class): The Client for the user.

    Returns:
            None
    """

    Client.send_message("pls postmeme")

    latest_message = Client.retreive_message("pls postmeme")

    Client.interact_button(
        "pls postmeme",
        choice(latest_message["components"][0]["components"])["custom_id"],
        latest_message,
    )

    sleep(0.5)

    latest_message = Client.retreive_message("pls postmeme")

    if "also a fan of your memes" in latest_message:
        try:
            coins = int(
                "".join(
                    filter(
                        str.isdigit,
                        latest_message["embeds"][0]["description"].split(
                            "also a fan of your memes"
                        )[0],
                    )
                )
            )
        except Exception:
            coins = "no"

        try:
            items = latest_message["embeds"][0]["description"].split("**")[-2]
        except Exception:
            items = "no items"
    else:
        try:
            coins = int(
                "".join(
                    filter(
                        str.isdigit,
                        latest_message["embeds"][0]["description"],
                    )
                )
            )
        except Exception:
            coins = "no"

        items = "no items"

        Client.log(
            "DEBUG",
            f"Received {'⏣ ' if coins != 'no' else ''}{coins} coin{'' if coins == 1 else 's'} &{' an' if items[0] in ['a', 'e', 'i', 'o', 'u'] else '' if items == 'no items' else ' a'} {items} from the `pls crime` command.",
        )
