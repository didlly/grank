from discord.message import send_message, retreive_message
from discord.button import interact_button
from random import choice
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def postmeme(username, channel_id, token, config, user_id, session_id, cwd):
    send_message(channel_id, token, config, username, "pls postmeme")

    latest_message = retreive_message(channel_id, token, config, username, "pls postmeme", user_id)

    if latest_message is None:
        return
    
    if latest_message["content"] == "oi you need to buy a laptop in the shop to post memes":
        if config["logging"]["debug"]:
            log(username, "DEBUG", "User does not have item `laptop`. Buying laptop now.")
        
        if config["auto_buy"] and config["auto_buy"]["laptop"]:
            from scripts.buy import buy
            buy(username, channel_id, token, config, user_id, cwd, "laptop")
            return
        elif config["logging"]["warning"]:
            log(username, "WARNING", f"A laptop is required for the command `pls postmeme`. However, since {'auto_buy is off for all items,' if not config['auto_buy']['parent'] else 'autobuy is off for laptops,'} the program will not buy one. Aborting command.")
            return
    else:
        interact_button(channel_id, token, config, username, "pls postmeme", choice(latest_message["components"][0]["components"])["custom_id"], latest_message, session_id)

def postmeme_parent(username, channel_id, token, config, user_id, session_id, cwd):
    while True:
        while not data[channel_id]:
            pass

        data[channel_id] = False

        start = time()

        try:
            postmeme(username, channel_id, token, config, user_id, session_id, cwd)
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