from random import choice
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def search(Client) -> None:
	Client.send_message("pls search")

	latest_message = Client.retreive_message("pls search")

	if latest_message is None:
		return

	Client.interact_button("pls search", choice(latest_message["components"][0]["components"])["custom_id"], latest_message)

def search_parent(Client) -> None:
	while True:
		while not data[Client.channel_id] or not data[Client.username]:
			pass

		data[Client.channel_id] = False

		start = time()

		try:
			search(Client)
		except Exception:
			log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls search` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		if Client.config["cooldowns"]["patron"]:
			cooldown = 15 - (end - start)
		else:
			cooldown = 30 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)