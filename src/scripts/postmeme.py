from discord.message import send_message, retreive_message
from discord.button import interact_button
from random import choice
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def postmeme(username, channel_id, token, config, user_id, session_id):
    send_message(channel_id, token, config, username, "pls postmeme")

    latest_message = retreive_message(channel_id, token, config, username, "pls postmeme", user_id)

    if not latest_message[0]:
        return
    
    interact_button(channel_id, token, config, username, "pls postmeme", choice(latest_message[-1]["components"][0]["components"])["custom_id"], latest_message, session_id)

def postmeme_parent(username, channel_id, token, config, user_id, session_id):
    while True:
        while not data[channel_id]:
            pass

        data[channel_id] = False

        start = time()

        try:
            postmeme(username, channel_id, token, config, user_id, session_id)
        except Exception:
            log(username, "WARNING", f"An unexpected error occured during the running of the `pls postmeme` command: `{exc_info()}`")

        end = time()   
        
        data[channel_id] = True
        
        if config["cooldowns"]["patron"]:
            cooldown = 20 - (end - start)
        else:
            cooldown = 30 - (end - start)

        if cooldown > 0:
            sleep(cooldown)