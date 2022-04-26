from json import dumps, loads

from scripts.buy import buy
from typing import Union
from websocket import WebSocket
from threading import Thread
from time import sleep
from utils.shared import data
from contextlib import suppress

def anti_heist(Client) -> None:
    sleep(1)
    
    Client.send_message("pls use phone")
    latest_message = Client.retreive_message("pls use phone")
    
    if "You don't own this item??" in latest_message:
        buy(Client, "phone")
        
    Client.send_message("p")

def send_heartbeat(ws, heartbeat_interval: int) -> None:
    while True:
        with suppress(Exception):
            sleep(heartbeat_interval)
            ws.send(dumps({"op": 1, "d": "null"}))


def receive_messages(Client, ws, event: dict) -> None:
    if "messages" not in data.keys():
        data["messages"] = {}

    if Client.channel_id not in data["messages"].keys():
        data["messages"][Client.channel_id] = []

    str_channel_id = str(Client.channel_id)

    Client.session_id = event["d"]["sessions"][0]["session_id"]

    while True:
        with suppress(Exception):
            event = loads(ws.recv())

            if event["op"] == 6:
                data["messages"][Client.channel_id].append({"op": 6})
                Client.log(
                    "WARNING",
                    "Websocket connection closed (Received opcode `6`). Resuming connection.",
                )
                gateway(Client)
                ws.send(
                    dumps(
                        {
                            "op": 6,
                            "d": {
                                "token": Client.token,
                                "session_id": Client.session_id,
                                "seq": "null",
                            },
                        }
                    )
                )
                return

            elif event["op"] == 7:
                data["messages"][Client.channel_id].append({"op": 7})
                Client.log(
                    "WARNING",
                    "Websocket connection closed (Received opcode `7`). Re-connecting.",
                )
                gateway(Client)
                return

            if event["t"] == "MESSAGE_CREATE":
                if event["d"]["channel_id"] == str_channel_id:
                    data["messages"][Client.channel_id].append(event["d"])
                
                if event["d"]["content"].lower() in [f"pls bankrob <@{Client.user_id}>", f"pls bankrob {Client.username.lower()}", f"pls heist <@{Client.user_id}>", f"pls heist {Client.username}".lower()]:
                    Thread(target=anti_heist, args=[Client]).start()

            elif event["t"] == "MESSAGE_UPDATE":
                if event["d"]["channel_id"] == str_channel_id:
                    found = False

                    for index in range(1, len(data["messages"][Client.channel_id][0])):
                        latest_message = data["messages"][Client.channel_id][-index]

                        if latest_message["id"] == event["d"]["id"]:
                            data["messages"][Client.channel_id][-index] = event["d"]
                            found = True
                            break

                    if not found:
                        data["messages"][Client.channel_id].append(event["d"])

            if len(data["messages"][Client.channel_id]) > 10:
                del data["messages"][Client.channel_id][0]


def gateway(Client, token: Union[None, str] = None) -> str:
    """Gets the first `session_id` received from Discord during the websocket connection process.

    Args:
            token (str): The token of the account the `session_id` should be found for.

    Returns:
            session_id (str): The `session_id` for the account specified by the token passed to this function.
    """

    ws = WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=10&encoding=json")
    heartbeat_interval = loads(ws.recv())["d"]["heartbeat_interval"] / 1000

    if token is None:
        Thread(target=send_heartbeat, args=[ws, heartbeat_interval]).start()

    ws.send(
        dumps(
            {
                "op": 2,
                "d": {
                    "token": Client.token if Client is not None else token,
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

    if event["op"] == 9:
        return gateway(Client)

    if token is None:
        Thread(target=receive_messages, args=[Client, ws, event]).start()

    return event["d"]["sessions"][0]["session_id"]
