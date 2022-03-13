from discord.message import send_message, retreive_message
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def hunt(username, channel_id, token, config, user_id, cwd, session_id):
	send_message(channel_id, token, config, username, "pls hunt")

	latest_message = retreive_message(channel_id, token, config, username, "pls hunt", user_id, session_id)

	if latest_message is None:
		return

	if latest_message["content"] == "You don't have a hunting rifle, you need to go buy one. You're not good enough to shoot animals with your bare hands... I hope.":
		if config["logging"]["debug"]:
			log(username, "DEBUG", "User does not have item `hunting rifle`. Buying hunting rifle now.")

		if config["auto buy"] and config["auto buy"]["hunting rifle"]:
			from scripts.buy import buy
			buy(username, channel_id, token, config, user_id, cwd, "hunting rifle")
			return
		elif config["logging"]["warning"]:
			log(
			    username,
			    "WARNING",
			    f"A hunting rifle is required for the command `pls fish`. However, since {'auto buy is off for hunting rifles,' if config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
			)
			return

def hunt_parent(username, channel_id, token, config, user_id, cwd, session_id):
	while True:
		while not data[channel_id] or not data[username]:
			pass

		data[channel_id] = False

		start = time()

		try:
			hunt(username, channel_id, token, config, user_id, cwd, session_id)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls hunt` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		if config["cooldowns"]["patron"]:
			cooldown = 25 - (end - start)
		else:
			cooldown = 40 - (end - start)

		if cooldown > 0:
			sleep(cooldown)