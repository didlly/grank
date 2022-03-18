from discord.message import send_message, retreive_message
from discord.button import interact_button
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def highlow(username, channel_id, token, config, user_id, session_id):
	send_message(channel_id, token, config, username, "pls highlow")

	latest_message = retreive_message(channel_id, token, config, username, "pls highlow", user_id, session_id)

	if latest_message is None:
		return

	number = int(latest_message["embeds"][0]["description"].split("**")[-2])
	
	interact_button(channel_id, token, config, username, "pls highlow", latest_message["components"][0]["components"][0]["custom_id"] if number > 50 else latest_message["components"][0]["components"][2]["custom_id"] if number < 50 else latest_message["components"][0]["components"][1]["custom_id"], latest_message, session_id)

def highlow_parent(username, channel_id, token, config, user_id, session_id):
	while True:
		while not data[channel_id] or not data[username]:
			pass

		data[channel_id] = False

		start = time()

		try:
			highlow(username, channel_id, token, config, user_id, session_id)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls highlow` command: `{exc_info()}`")

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