from requests import post, get
from utils.logger import register
from time import sleep
from json import loads
from random import choice

def search(channel_id, token, config, log, ID):
    request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls search"})
    
    if request.status_code != 200:
        if config["logging"]["warning"]:
            register(log, "WARNING", f"Failed to send command `pls search`. Status code: {request.status_code} (expected 200). Aborting command.")
        return
    
    if config["logging"]["debug"]:
        register(log, "DEBUG", "Successfully sent command `pls search`.")
    
    latest_message = None
    
    for _ in range(0, config["cooldowns"]["timeout"]):
        sleep(1)
        
        request = get(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token})
        
        if request.status_code != 200:
            continue

        latest_message = loads(request.text)[0]
        
        if latest_message["author"]["id"] == "270904126974590976" and latest_message["referenced_message"]["author"]["id"] == ID:
            if config["logging"]["debug"]:
                register(log, "DEBUG", "Got Dank Memer's response to command `pls search`.")
            break
        else:
            continue 
    
    if latest_message is None or latest_message["author"]["id"] != "270904126974590976":
        if config["logging"]["warning"]:
            register(log, "WARNING", f"Timeout exceeded for response from Dank Memer ({config['cooldowns']['timeout']} second(s)). Aborting command.")
        return
        
    data = {
        "application_id": 270904126974590976,
        "channel_id": channel_id,
        "type": 3,
        "data": {
            "component_type": 2,
            "custom_id": choice(latest_message["components"][0]["components"])["custom_id"]
        },
        "guild_id": latest_message["message_reference"]["guild_id"],
        "message_flags": 0,
        "message_id": latest_message["id"]
    }
    
    request = post(f"https://discord.com/api/v9/interactions", headers={"authorization": token}, json=data)
    
    if request.status_code == 200 or request.status_code == 204:
        if config["logging"]["debug"]:
            register(log, "DEBUG", "Successfully interacted with button on Dank Memer's response to command `pls search`.")
    elif config["logging"]["warning"]:
        register(log, "WARNING", f"Failed to interact with button on Dank Memer's response to command `pls search`. Status code: {request.status_code} (expected 200 or 204).")