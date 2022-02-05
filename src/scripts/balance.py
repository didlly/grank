from requests import post, get
from utils.logger import register
from time import sleep
from json import loads

def balance(username, channel_id, token, config, log, ID):
    request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls bal"})
    
    if request.status_code != 200 and config["logging"]["warning"]:
        register(log, username, "WARNING", f"Failed to send command `pls bal`. Status code: {request.status_code} (expected 200). Aborting command.")
        return
    
    if config["logging"]["debug"]:
        register(log, username, "DEBUG", "Successfully sent command `pls bal`.")
    
    latest_message = None
    
    for _ in range(0, config["cooldowns"]["timeout"] * 10):
        sleep(0.1)
        
        request = get(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token})
        
        if request.status_code != 200:
            continue
        
        latest_message = loads(request.text)[0]
        
        if latest_message["author"]["id"] == "270904126974590976" and latest_message["referenced_message"]["author"]["id"] == ID:
            if config["logging"]["debug"]:
                register(log, username, "DEBUG", "Got Dank Memer's response to command `pls bal`.")
            break
        else:
            continue
       
    if latest_message is None or latest_message["author"]["id"] != "270904126974590976":
        if config["logging"]["warning"]:
            register(log, username, "WARNING", f"Timeout exceeded for response from Dank Memer ({config['cooldowns']['timeout']} second(s)). Aborting command.")
        return
        
    return True, latest_message