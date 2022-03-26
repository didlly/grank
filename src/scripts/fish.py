from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def fish(Client) -> None:
	Client.send_message("pls fish")

	latest_message = Client.retreive_message("pls fish")

	if latest_message["content"] == "You don't have a fishing pole, you need to go buy one. You're not good enough to catch them with your hands.":
		if Client.config["logging"]["debug"]:
			log(Client.username, "DEBUG", "User does not have item `fishing pole`. Buying fishing pole now.")

		if Client.config["auto buy"] and Client.config["auto buy"]["fishing pole"]:
			from scripts.buy import buy
			buy(Client, "fishing pole")
			return
		elif Client.config["logging"]["warning"]:
			log(
				Client.username,
				"WARNING",
				f"A fishing pole is required for the command `pls fish`. However, since {'auto buy is off for fishing poles,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
			)
			return

def fish_parent(Client) -> None:
	"""One of the basic 7 currency commands - `pls fish`.
 
	Required item(s): Fishing pole

	Args:
		Client (class): The Client for the user.

	Returns:
		None
	"""
 
	while True:
		while not data[Client.channel_id] or not data[Client.username]:
			pass

		data[Client.channel_id] = False

		start = time()

		try:
			fish(Client)
		except Exception:
			log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls fish` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		if Client.config["cooldowns"]["patron"]:
			cooldown = 25 - (end - start)
		else:
			cooldown = 45 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)