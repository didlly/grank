from requests import post
from utils.logger import register

def beg(channel_id, token, config, log):
    request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls beg"})
    
    if request.status_code != 200:
        if config["logging"]["warning"]:
            register(log, "WARNING", f"Failed to send command `pls beg`. Status code: {request.status_code} (expected 200).")
        return
    
    if config["logging"]["debug"]:
        register(log, "DEBUG", "Successfully sent command `pls beg`.")