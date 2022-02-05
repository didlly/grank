from json import load, dumps
from requests import post
from utils.logger import register
from datetime import datetime
from time import time, sleep
from sys import exc_info
import utils.run

def daily(username, channel_id, token, config, log, cwd):
    def daily_run(username, channel_id, token, config, log, cwd):
        data = load(open(f"{cwd}/data.json", "r"))
        
        if data["daily"] == "None":
            request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls daily"})
        
            if request.status_code != 200:
                if config["logging"]["warning"]:
                    register(log, username, "WARNING", f"Failed to send command `pls daily`. Status code: {request.status_code} (expected 200).")
                return
            
            if config["logging"]["debug"]:
                register(log, username, "DEBUG", "Successfully sent command `pls daily`.")
            
            data["daily"] = datetime.now().strftime("%x-%X")

            with open(f"{cwd}/data.json", "w") as data_file:
                data_file.write(dumps(data))
            
            if config["logging"]["debug"]:
                register(log, username, "DEBUG", "Successfully updated latest command run of `pls daily`.")
        elif (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["daily"], "%x-%X")).total_seconds() > 23400:
            request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls daily"})
        
            if request.status_code != 200:
                if config["logging"]["warning"]:
                    register(log, username, "WARNING", f"Failed to send command `pls daily`. Status code: {request.status_code} (expected 200).")
                return
            
            if config["logging"]["debug"]:
                register(log, username, "DEBUG", "Successfully sent command `pls daily`.")
            
            data["daily"] = datetime.now().strftime("%x-%X")
            
            with open(f"{cwd}/data.json", "w") as data_file:
                data_file.write(dumps(data))
            
            if config["logging"]["debug"]:
                register(log, username, "DEBUG", "Successfully updated latest command run of `pls daily`.")

    while True:
        while not utils.run.run[channel_id]:
            pass

        utils.run.run[channel_id] = False

        start = time()

        try:
            daily_run(username, channel_id, token, config, log, cwd)
        except Exception:
            register(log, username, "WARNING", f"An unexpected error occured during the running of the `pls daily` command: `{exc_info()}`")

        end = time()   
        
        utils.run.run[channel_id] = True
        
        cooldown = 23400 - (end - start)

        if cooldown > 0:
            sleep(cooldown)