from json import dumps, loads

from utils.logger import log
from websocket import WebSocket


def gateway(token):
    """Gets the first `session_id` received from Discord during the websocket connection process.

    Args:
            token (str): The token of the account the `session_id` should be found for.

    Returns:
            session_id (str): The `session_id` for the account specified by the token passed to this function.
    """

    for index in range(1, 6):
        ws = WebSocket()
        ws.connect("wss://gateway.discord.gg/?v=10&encoding=json")
        loads(ws.recv())

        ws.send(
            dumps(
                {
                    "op": 2,
                    "d": {
                        "token": token,
                        "properties": {
                            "$os": "windows",
                            "$browser": "chrome",
                            "$device": "pc",
                        },
                    },
                }
            )
        )

        res = ws.recv()

        try:
            return loads(res)["d"]["sessions"][0]["session_id"]
        except TypeError:
            log(None, "WARNING", "Failed to get `session_id`. Re-trying again.")

    if index == 5:
        log(
            None,
            "ERROR",
            "Failed to get `session_id` after max retries. Please wait a few minutes and re-open Grank.",
        )
