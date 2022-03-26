from random import choice
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def crime(Client) -> None:
	Client.send_message("pls crime")

	latest_message = Client.retreive_message("pls crime")

	custom_id = None
 
	for option in latest_message["components"][0]["components"]:
		if option["label"] == "tax evasion":
			# Gives Badosz's card
			custom_id = option["custom_id"]
			break
  
	Client.interact_button("pls crime", choice(latest_message["components"][0]["components"])["custom_id"] if custom_id is None else custom_id, latest_message)

def crime_parent(Client) -> None:
	"""One of the basic 7 currency commands - `pls crime`.
 
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
			crime(Client)
		except Exception:
			log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls crime` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		if Client.config["cooldowns"]["patron"]:
			cooldown = 15 - (end - start)
		else:
			cooldown = 45 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)