from random import randint
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def snakeeyes(Client) -> None:
	amount = Client.config['snakeeyes']['amount'] if not Client.config['snakeeyes']['random'] else randint(Client.config['snakeeyes']['minimum'], Client.config['snakeeyes']['maximum'])

	Client.send_message(f"pls snakeeyes {amount}")
	
def snakeeyes_parent(Client) -> None:
	"""One of the 3 gamble commands - `pls snakeeyes`.
 
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
			snakeeyes(Client)
		except Exception:
			if Client.config["logging"]["warning"]:
				log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls snakeeyes` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		if Client.config["cooldowns"]["patron"]:
			cooldown = 5 - (end - start)
		else:
			cooldown = 10 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)