from json import load, dumps
from requests import post
from utils.logger import register
from datetime import datetime

def daily(channel_id, token, config, log, cwd):
    data = load(open(f"{cwd}/data.json", "r"))
    
    if data["daily"] == "None":
        request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls daily"})
    
        if request.status_code != 200:
            if config["logging"]["warning"]:
                register(log, "WARNING", f"Failed to send command `pls daily`. Status code: {request.status_code} (expected 200).")
            return
        
        if config["logging"]["debug"]:
            register(log, "DEBUG", "Successfully sent command `pls daily`.")
        
        data["daily"] = datetime.now().strftime("%x-%X")

        with open(f"{cwd}/data.json", "w") as data_file:
            data_file.write(dumps(data))
        
        if config["logging"]["debug"]:
            register(log, "DEBUG", "Successfully updated latest command run of `pls daily`.")
    elif (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["daily"], "%x-%X")).total_seconds() > 23400:
        request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls daily"})
    
        if request.status_code != 200:
            if config["logging"]["warning"]:
                register(log, "WARNING", f"Failed to send command `pls daily`. Status code: {request.status_code} (expected 200).")
            return
        
        if config["logging"]["debug"]:
            register(log, "DEBUG", "Successfully sent command `pls daily`.")
        
        data["daily"] = datetime.now().strftime("%x-%X")
           
        with open(f"{cwd}/data.json", "w") as data_file:
            data_file.write(dumps(data))
        
        if config["logging"]["debug"]:
            register(log, "DEBUG", "Successfully updated latest command run of `pls daily`.") 