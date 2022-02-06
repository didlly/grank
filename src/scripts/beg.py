from requests import post
from utils.logger import register
from time import time, sleep
from sys import exc_info
import utils.run

def beg(username, channel_id, token, config, log):
    def beg_run(username, channel_id, token, config, log):
        request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls beg"})
        
        if request.status_code != 200:
            if config["logging"]["warning"]:
                register(log, username, "WARNING", f"Failed to send command `pls beg`. Status code: {request.status_code} (expected 200).")
            return
        
        if config["logging"]["debug"]:
            register(log, username, "DEBUG", "Successfully sent command `pls beg`.")

    while True:
        while not utils.run.run[channel_id]:
            pass

        utils.run.run[channel_id] = False

        start = time()

        try:
            beg_run(username, channel_id, token, config, log)
        except Exception:
            register(log, username, "WARNING", f"An unexpected error occured during the running of the `pls beg` command: `{exc_info()}`")
        
        end = time()

        utils.run.run[channel_id] = True
        
        if config["cooldowns"]["patron"]:
            cooldown = 25 - (end - start)
        else:
            cooldown = 45 - (end - start)

        if cooldown > 0:
            sleep(cooldown)