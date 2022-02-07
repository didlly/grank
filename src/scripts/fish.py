from requests import post, get
from utils.logger import register
from time import sleep 
from json import loads
from time import time, sleep
from sys import exc_info
import utils.run

def fish(username, channel_id, token, config, log, ID, cwd):
    def fish_run(username, channel_id, token, config, log, ID, cwd):
        request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls fish"})
        
        if request.status_code != 200:
            if config["logging"]["warning"]:
                register(log, username, "WARNING", f"Failed to send command `pls fish`. Status code: {request.status_code} (expected 200).")
            return
        
        if config["logging"]["debug"]:
            register(log, username, "DEBUG", "Successfully sent command `pls fish`.")
            
        latest_message = None
        
        for _ in range(0, config["cooldowns"]["timeout"] * 10):
            sleep(0.1)
            
            request = get(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token})
            
            if request.status_code != 200:
                continue

            latest_message = loads(request.text)[0]
            
            if latest_message["author"]["id"] == "270904126974590976" and latest_message["referenced_message"]["author"]["id"] == ID:
                if config["logging"]["debug"]:
                    register(log, username, "DEBUG", "Got Dank Memer's response to command `pls fish`.")
                break
            else:
                continue
        
        if latest_message is None or latest_message["author"]["id"] != "270904126974590976":
            if config["logging"]["warning"]:
                register(log, username, "WARNING", f"Timeout exceeded for response from Dank Memer ({config['cooldowns']['timeout']} {'second' if config['cooldowns']['timeout'] == 1 else 'seconds'}). Aborting command.")
            return
        elif latest_message["content"] == "You don't have a fishing pole, you need to go buy one. You're not good enough to catch them with your hands.":
            if config["logging"]["debug"]:
                register(log, username, "DEBUG", "User does not have item `fishing pole`. Buying fishing pole now.")
            
            if config["auto_buy"]["parent"] and config["auto_buy"]["fishing pole"]:
                from scripts.buy import buy
                buy(username, channel_id, token, config, log, ID, cwd, "fishing pole")
                return
            elif config["logging"]["warning"]:
                register(log, username, "WARNING", f"A fishing pole is required for the command `pls fish`. However, since {'auto_buy is off for all items,' if not config['auto_buy']['parent'] else 'autobuy is off for fishing poles,'} the program will not buy one. Aborting command.")
                return
    
    while True:
        while not utils.run.run[channel_id]:
            pass

        utils.run.run[channel_id] = False

        start = time()

        try:
            fish_run(username, channel_id, token, config, log, ID, cwd)
        except Exception:
            register(log, username, "WARNING", f"An unexpected error occured during the running of the `pls fish` command: `{exc_info()}`")
        
        end = time()

        utils.run.run[channel_id] = True

        if config["cooldowns"]["patron"]:
            cooldown = 25 - (end - start)
        else:
            cooldown = 45 - (end - start)

        if cooldown > 0:
            sleep(cooldown)