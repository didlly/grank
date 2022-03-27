from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def beg(Client) -> None:
	Client.send_message("pls beg")

def beg_parent(Client) -> None:
	"""One of the basic 7 currency commands - `pls beg`.
 
	Required item(s): None

	Args:
		Client (class): The Client for the user.

	Returns:
		None
	"""
 
	sleep(40)
	
	while True:
		while not data[Client.channel_id] or not data[Client.username]:
			pass

		data[Client.channel_id] = False

		start = time()

		try:
			beg(Client)
		except Exception:
			if Client.config["logging"]["warning"]:
				log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls beg` command: `{exc_info()}`")

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