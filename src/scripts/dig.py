from requests import post
from utils.logger import register
from time import sleep, time
from requests import get
from json import loads
from sys import exc_info
import utils.run

def dig(username, channel_id, token, config, log, ID, cwd):
    def dig_run(username, channel_id, token, config, log, ID, cwd):
        request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls dig"})
        
        if request.status_code != 200:
            if config["logging"]["warning"]:
                register(log, username, "WARNING", f"Failed to send command `pls dig`. Status code: {request.status_code} (expected 200).")
            return
        
        if config["logging"]["debug"]:
            register(log, username, "DEBUG", "Successfully sent command `pls dig`.")
            
        latest_message = None
        
        for _ in range(0, config["cooldowns"]["timeout"] * 10):
            sleep(0.1)
            
            request = get(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token})
            
            if request.status_code != 200:
                continue

            latest_message = loads(request.text)[0]
            
            if latest_message["author"]["id"] == "270904126974590976" and latest_message["referenced_message"]["author"]["id"] == ID:
                if config["logging"]["debug"]:
                    register(log, username, "DEBUG", "Got Dank Memer's response to command `pls dig`.")
                break
            else:
                continue
        
        if latest_message is None or latest_message["author"]["id"] != "270904126974590976":
            if config["logging"]["warning"]:
                register(log, username, "WARNING", f"Timeout exceeded for response from Dank Memer ({config['cooldowns']['timeout']} second(s)). Aborting command.")
            return
        elif latest_message["content"] == "You don't have a shovel, you need to go buy one. I'd hate to let you dig with your bare hands.":
            if config["logging"]["debug"]:
                register(log, username, "DEBUG", "User does not have item `shovel`. Buying shovel now.")
            
            if config["commands"]["auto_buy"]:
                from scripts.buy import buy
                buy(username, channel_id, token, config, log, ID, cwd, "shovel")
                return
            elif config["logging"]["warning"]:
                register(log, username, "WARNING", "A shovel is required for the command `pls dig`. However, since `auto_buy` is set to false in the configuration file, the program will not buy one. Aborting command.")
                return

    while True:
        while not utils.run.run[channel_id]:
            pass

        utils.run.run[channel_id] = False

        start = time()

        try:
            dig_run(username, channel_id, token, config, log, ID, cwd)
        except Exception:
            register(log, username, "WARNING", f"An unexpected error occured during the running of the `pls dig` command: `{exc_info()}`")
        
        end = time()

        utils.run.run[channel_id] = True
        
        cooldown = 40 - (end - start)

        if cooldown > 0:
            sleep(cooldown)