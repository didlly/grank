from json import dumps, loads

from websocket import WebSocket
from threading import Thread
from time import sleep
from utils.shared import data
from contextlib import suppress


def send_heartbeat(ws, heartbeat_interval: int) -> None:
    while True:
        with suppress(Exception):
            sleep(heartbeat_interval)
            ws.send(dumps({"op": 1, "d": "null"}))


def receive_messages(ws, event: dict, channel_id: int) -> None:
    if channel_id not in data["messages"].keys():
        data["messages"][channel_id] = []

    str_channel_id = str(channel_id)

    while True:
        with suppress(Exception):
            event = loads(ws.recv())

            if event["t"] == "MESSAGE_CREATE":
                if event["d"]["channel_id"] == str_channel_id:
                    data["messages"][channel_id].append(event["d"])
                
            if event["t"] == "MESSAGE_UPDATE":
                if event["d"]["channel_id"] == str_channel_id:
                    found = False
                    
                    for index in range(1, len(data["messages"][channel_id][0])):
                        latest_message = data["messages"][channel_id][-index]
                        
                        if latest_message["id"] == event["d"]["id"]:
                            data["messages"][channel_id][-index] = event["d"]
                            found = True
                            break
                        
                    if not found:
                        data["messages"][channel_id].append(event["d"])
                    
            if len(data["messages"][channel_id]) > 10:
                del data["messages"][channel_id][0]
                


def gateway(token: str, channel_id: int) -> str:
    """Gets the first `session_id` received from Discord during the websocket connection process.

    Args:
            token (str): The token of the account the `session_id` should be found for.

    Returns:
            session_id (str): The `session_id` for the account specified by the token passed to this function.
    """

    if "messages" not in data.keys():
        data["messages"] = {}

    ws = WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=10&encoding=json")
    heartbeat_interval = loads(ws.recv())["d"]["heartbeat_interval"] / 1000

    Thread(target=send_heartbeat, args=[ws, heartbeat_interval]).start()

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

    event = loads(ws.recv())

    if channel_id is not None:
        Thread(target=receive_messages, args=[ws, event, channel_id]).start()

    return event["d"]["sessions"][0]["session_id"]
