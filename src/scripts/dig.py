from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def dig(Client, cwd):
	Client.send_message("pls dig")

	latest_message = Client.retreive_message("pls dig")

	if latest_message is None:
		return

	if latest_message["content"] == "You don't have a shovel, you need to go buy one. I'd hate to let you dig with your bare hands.":
		if Client.config["logging"]["debug"]:
			log(Client.username, "DEBUG", "User does not have item `shovel`. Buying shovel now.")

		if Client.config["auto buy"] and Client.config["auto buy"]["shovel"]:
			from scripts.buy import buy
			buy(Client, "shovel", cwd)
			return
		elif Client.config["logging"]["warning"]:
			log(
			    Client.username,
			    "WARNING",
			    f"A shovel is required for the command `pls dig`. However, since {'auto buy is off for shovels,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
			)
			return

def dig_parent(Client, cwd):
	while True:
		while not data[Client.channel_id] or not data[Client.username]:
			pass

		data[Client.channel_id] = False

		start = time()

		try:
			dig(Client, cwd)
		except Exception:
			log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls dig` command: `{exc_info()}`")

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