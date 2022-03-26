from random import choice
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def postmeme(Client) -> None:
	Client.send_message("pls postmeme")

	latest_message = Client.retreive_message("pls postmeme")

	Client.interact_button("pls postmeme", choice(latest_message["components"][0]["components"])["custom_id"], latest_message)

def postmeme_parent(Client) -> None:
	"""One of the basic 7 currency commands - `pls postmeme`.
 
	Required item(s): None

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
			postmeme(Client)
		except Exception:
			log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls postmeme` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		if Client.config["cooldowns"]["patron"]:
			cooldown = 45 - (end - start)
		else:
			cooldown = 50 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)