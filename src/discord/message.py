from requests import post, get
from utils.logger import log
from time import sleep
from random import uniform
from json import loads
from datetime import datetime

def send_message(channel_id, token, config, username, command):
    if config["typing_indicator"]["enabled"]:
        request = post(f"https://discord.com/api/v9/channels/{channel_id}/typing", headers={"authorization": token})
        sleep(uniform(config["typing_indicator"]["minimum"], config["typing_indicator"]["maximum"]))

    request = post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers={"authorization": token}, json={"content": command})

    if request.status_code == 200 or request.status_code == 204:
        if config["logging"]["debug"]:
             log(username, "DEBUG", f"Successfully sent command `{command}`.")
        return True
    else:
        if config["logging"]["warning"]:
            log(username, "WARNING", f"Failed to send command `{command}`. Status code: {request.getcode()} (expected 200 or 204).")
        return False

def retreive_message(channel_id, token, config, username, command, user_id):   
    time = datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")

    while (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - time).total_seconds() < config["cooldowns"]["timeout"]:
        request = get(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers={"authorization": token})
        
        if request.status_code != 200:
            continue
        
        latest_message = loads(request.text)[0]
        
        if latest_message["author"]["id"] == "270904126974590976" and latest_message["referenced_message"]["author"]["id"] == user_id:
            if config["logging"]["debug"]:
                log(username, "DEBUG", f"Got Dank Memer's response to command `{command}`.")
            break
        else:
            continue
       
    if latest_message["author"]["id"] != "270904126974590976":
        if config["logging"]["warning"]:
            log(username, "WARNING", f"Timeout exceeded for response from Dank Memer ({config['cooldowns']['timeout']} {'second' if config['cooldowns']['timeout'] == 1 else 'seconds'}). Aborting command.")
        return None

    for key in config["auto_trade"]:
        if key == "enabled" and key == "trader":
            continue
        elif key in latest_message["content"].lower():
            send_message(channel_id, token, config, username, f"pls trade 1 {key} {config['auto_trade']['trader']}")
        else:
            try:
                _ = latest_message["embeds"][0]["description"]
                if key in latest_message["embeds"][0]["description"]:
                    send_message(channel_id, token, config, username, f"pls trade 1 {key} {config['auto_trade']['trader']}")
            except IndexError:
                pass
   
    return latest_message