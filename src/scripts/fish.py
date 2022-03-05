from discord.message import send_message, retreive_message
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def fish(username, channel_id, token, config, user_id, cwd, session_id):
	send_message(channel_id, token, config, username, "pls fish")

	latest_message = retreive_message(channel_id, token, config, username, "pls fish", user_id, session_id)

	if latest_message is None:
		return

	if latest_message["content"] == "You don't have a fishing pole, you need to go buy one. You're not good enough to catch them with your hands.":
		if config["logging"]["debug"]:
			log(username, "DEBUG", "User does not have item `fishing pole`. Buying fishing pole now.")
		
		if config["auto_buy"] and config["auto_buy"]["fishing pole"]:
			from scripts.buy import buy
			buy(username, channel_id, token, config, user_id, cwd, "fishing pole")
			return
		elif config["logging"]["warning"]:
			log(username, "WARNING", f"A fishing pole is required for the command `pls fish`. However, since {'auto_buy is off for all items,' if not config['auto_buy']['parent'] else 'autobuy is off for fishing poles,'} the program will not buy one. Aborting command.")
			return

def fish_parent(username, channel_id, token, config, user_id, cwd, session_id):
	while True:
		while not data[channel_id]:
			pass

		data[channel_id] = False

		start = time()

		try:
			fish(username, channel_id, token, config, user_id, cwd, session_id)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls fish` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		if config["cooldowns"]["patron"]:
			cooldown = 25 - (end - start)
		else:
			cooldown = 45 - (end - start)

		if cooldown > 0:
			sleep(cooldown)