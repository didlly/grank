from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def hunt(Client, cwd: str) -> None:
	Client.send_message("pls hunt")

	latest_message = Client.retreive_message("pls hunt")

	if latest_message is None:
		return

	if latest_message["content"] == "You don't have a hunting rifle, you need to go buy one. You're not good enough to shoot animals with your bare hands... I hope.":
		if Client.config["logging"]["debug"]:
			log(Client.username, "DEBUG", "User does not have item `hunting rifle`. Buying hunting rifle now.")

		if Client.config["auto buy"] and Client.config["auto buy"]["hunting rifle"]:
			from scripts.buy import buy
			buy(Client, "hunting rifle", cwd)
			return
		elif Client.config["logging"]["warning"]:
			log(
			    Client.username,
			    "WARNING",
			    f"A hunting rifle is required for the command `pls fish`. However, since {'auto buy is off for hunting rifles,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
			)
			return

def hunt_parent(Client, cwd: str) -> None:
	while True:
		while not data[Client.channel_id] or not data[Client.username]:
			pass

		data[Client.channel_id] = False

		start = time()

		try:
			hunt(Client, cwd)
		except Exception:
			log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls hunt` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		if Client.config["cooldowns"]["patron"]:
			cooldown = 25 - (end - start)
		else:
			cooldown = 40 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)