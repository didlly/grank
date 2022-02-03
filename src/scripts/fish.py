from requests import post, get
from utils.logger import register
from time import sleep 
from json import loads

def fish(channel_id, token, config, log, ID):
    request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls fish"})
    
    if request.status_code != 200:
        if config["logging"]["warning"]:
            register(log, "WARNING", f"Failed to send command `pls fish`. Status code: {request.status_code} (expected 200).")
        return
    
    if config["logging"]["debug"]:
        register(log, "DEBUG", "Successfully sent command `pls fish`.")
        
    latest_message = None
      
    for _ in range(0, config["cooldowns"]["timeout"]):
        sleep(1)
        
        request = get(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token})
        
        if request.status_code != 200:
            continue

        latest_message = loads(request.text)[0]
        
        if latest_message["author"]["id"] == "270904126974590976" and latest_message["referenced_message"]["author"]["id"] == ID:
            if config["logging"]["debug"]:
                register(log, "DEBUG", "Got Dank Memer's response to command `pls fish`.")
            break
        else:
            continue
       
    if latest_message is None or latest_message["author"]["id"] != "270904126974590976":
        if config["logging"]["warning"]:
            register(log, "WARNING", f"Timeout exceeded for response from Dank Memer ({config['cooldowns']['timeout']} second(s)). Aborting command.")
        return
    elif latest_message["content"].lower() == "you don't have a fishing pole, you need to go buy one. you're not good enough to catch them with your hands.":
        if config["logging"]["debug"]:
            register(log, "DEBUG", "User does not have item `fishing pole`. Buying fishing pole now.")
        
        if config["commands"]["auto_buy"]:
            from scripts.buy import buy
            buy(channel_id, token, config, log, ID, "fishing")
            return
        elif config["logging"]["warning"]:
            register(log, "WARNING", "A fishing pole is required for the command `pls fish`. However, since `auto_buy` is set to false in the configuration file, the program will not buy one. Aborting command.")
            return