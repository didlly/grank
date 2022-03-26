from json import load, dumps
from datetime import datetime
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def lottery(Client) -> None:
	with open(f"{Client.cwd}database.json", "r") as data:
		data = load(data)

		if "lottery" not in data.keys():
			Client.send_message("pls lottery")

			latest_message = Client.retreive_message("pls lottery")

			Client.interact_button("pls lottery", latest_message["components"][0]["components"][-1]["custom_id"], latest_message)
			
			data["lottery"] = datetime.now().strftime("%x-%X")

			with open(f"{Client.cwd}database.json", "w") as data_file:
				data_file.write(dumps(data))
			
			if Client.config["logging"]["debug"]:
				log(Client.username, "DEBUG", "Successfully updated latest command run of `pls lottery`.")
		elif (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["lottery"], "%x-%X")).total_seconds() > Client.config["lottery"]["cooldown"]:
			Client.send_message("pls lottery")

			latest_message = Client.retreive_message("pls lottery")
			
			Client.interact_button("pls lottery", latest_message["components"][0]["components"][-1]["custom_id"], latest_message)

			data["lottery"] = datetime.now().strftime("%x-%X")
			
			with open(f"{Client.cwd}database.json", "w") as database:
				database.write(dumps(data))
			
			if Client.config["logging"]["debug"]:
				log(Client.username, "DEBUG", "Successfully updated latest command run of `pls lottery`.")

def lottery_parent(Client) -> None:
	"""One of the 3 gambling commands - `pls lottery`.
 
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
			lottery(Client)
		except Exception:
			log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls lottery` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		cooldown = Client.config["lottery"]["cooldown"] - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)