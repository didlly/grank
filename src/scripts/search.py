from discord.message import send_message, retreive_message
from discord.button import interact_button
from random import choice
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def search(username, channel_id, token, config, user_id, session_id):
	send_message(channel_id, token, config, username, "pls search")

	latest_message = retreive_message(channel_id, token, config, username, "pls search", user_id)

	if latest_message is None:
		return
	
	interact_button(channel_id, token, config, username, "pls search", choice(latest_message["components"][0]["components"])["custom_id"], latest_message, session_id)

def search_parent(username, channel_id, token, config, user_id, session_id):
	while True:
		while not data[channel_id] or not data[username]:
			pass

		data[channel_id] = False

		start = time()

		try:
			search(username, channel_id, token, config, user_id, session_id)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls search` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		if config["cooldowns"]["patron"]:
			cooldown = 15 - (end - start)
		else:
			cooldown = 30 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)