from requests import post, get
from utils.logger import log
from time import sleep
from json import loads

def send_message(channel_id, token, config, username, command):
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
    latest_message = None
    
    for index in range(0, config["cooldowns"]["timeout"]):
        sleep(0.1)
        
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
       
    if latest_message is None or latest_message["author"]["id"] != "270904126974590976":
        if config["logging"]["warning"]:
            log(username, "WARNING", f"Timeout exceeded for response from Dank Memer ({config['cooldowns']['timeout']} {'second' if config['cooldowns']['timeout'] == 1 else 'seconds'}). Aborting command.")
        return False, None
    
    return True, latest_message