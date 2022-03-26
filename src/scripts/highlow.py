from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def highlow(Client) -> None:
	Client.send_message("pls highlow")

	latest_message = Client.retreive_message("pls highlow")

	number = int(latest_message["embeds"][0]["description"].split("**")[-2])
	
	Client.interact_button("pls highlow", latest_message["components"][0]["components"][0]["custom_id"] if number > 50 else latest_message["components"][0]["components"][2]["custom_id"] if number < 50 else latest_message["components"][0]["components"][1]["custom_id"], latest_message)

def highlow_parent(Client) -> None:
	"""One of the 2 guess the number commands - `pls highlow`.
 
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
			highlow(Client)
		except Exception:
			log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls highlow` command: `{exc_info()}`")

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