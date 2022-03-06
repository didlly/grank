from discord.message import send_message, retreive_message
from discord.button import interact_button
from discord.dropdown import interact_dropdown
from random import choice, randint
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def stream(username, channel_id, token, config, user_id, cwd, session_id):
	send_message(channel_id, token, config, username, "pls stream")

	latest_message = retreive_message(channel_id, token, config, username, "pls stream", user_id)

	if latest_message is None:
		return
	
	if "title" in latest_message["embeds"][0].keys():
		if "Keyboard" in latest_message["embeds"][0]["description"]:
			if config["logging"]["debug"]:
				log(username, "DEBUG", "User does not have item `keyboard`. Buying laptop now.")
				
			if config["auto_buy"] and config["auto_buy"]["keyboard"]:
				from scripts.buy import buy
				buy(username, channel_id, token, config, user_id, cwd, "keyboard")
				return
			elif config["logging"]["warning"]:
				log(username, "WARNING", f"A keyboard is required for the command `pls postmeme`. However, since {'auto_buy is off for all items,' if not config['auto_buy']['parent'] else 'autobuy is off for keyboards,'} the program will not buy one. Aborting command.")
				return

		if "Mouse" in latest_message["embeds"][0]["description"]:
			if config["logging"]["debug"]:
				log(username, "DEBUG", "User does not have item `mouse`. Buying laptop now.")
				
			if config["auto_buy"] and config["auto_buy"]["mouse"]:
				from scripts.buy import buy
				buy(username, channel_id, token, config, user_id, cwd, "mouse")
				return
			elif config["logging"]["warning"]:
				log(username, "WARNING", f"A mouse is required for the command `pls postmeme`. However, since {'auto_buy is off for all items,' if not config['auto_buy']['parent'] else 'autobuy is off for mouses,'} the program will not buy one. Aborting command.")
				return

	if len(latest_message["components"][0]["components"]) == 3:
		interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message, session_id)
	
		latest_message = retreive_message(channel_id, token, config, username, "pls stream", user_id)

		if latest_message is None:
			return

		interact_dropdown(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][0]["custom_id"], choice(latest_message["components"][0]["components"][0]["options"])["value"], latest_message, session_id)
		
		interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][-1]["components"][0]["custom_id"], latest_message, session_id)
  
	latest_message = retreive_message(channel_id, token, config, username, "pls stream", user_id)
 
	if int(latest_message["embeds"][0]["fields"][5]["value"].replace("`", "")) > 0:
		interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message, session_id)
	else:
		if randint(1, 2) == 1:
			interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][1]["custom_id"], latest_message, session_id)
		else:
			interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][2]["custom_id"], latest_message, session_id)
   
	interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][-1]["components"][-1]["custom_id"], latest_message, session_id)

def stream_parent(username, channel_id, token, config, user_id, cwd, session_id):
	while True:
		while not data[channel_id]:
			pass

		data[channel_id] = False

		start = time()

		try:
			stream(username, channel_id, token, config, user_id, cwd, session_id)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls stream` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		cooldown = 610 - (end - start)

		if cooldown > 0:
			sleep(cooldown)