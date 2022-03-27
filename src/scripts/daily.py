from json import load, dumps
from json.decoder import JSONDecodeError
from utils.database import database_fixer
from utils.logger import log
from datetime import datetime
from time import time, sleep
from sys import exc_info
from utils.shared import data

def daily(Client) -> None:
	with open(f"{Client.cwd}database.json", "r") as data:
		try:
			data = load(data)
		except JSONDecodeError:
			database_fixer(Client.cwd)
			data = load(data)

		if "daily" not in data.keys():
			Client.send_message("pls daily")
			
			data["daily"] = datetime.now().strftime("%x-%X")

			with open(f"{Client.cwd}database.json", "w") as data_file:
				data_file.write(dumps(data))
			
			if Client.config["logging"]["debug"]:
				log(Client.username, "DEBUG", "Successfully updated latest command run of `pls daily`.")
		elif (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["daily"], "%x-%X")).total_seconds() > 23400:
			Client.send_message("pls daily")

			data["daily"] = datetime.now().strftime("%x-%X")
			
			with open(f"{Client.cwd}database.json", "w") as database:
				database.write(dumps(data))
			
			if Client.config["logging"]["debug"]:
				log(Client.username, "DEBUG", "Successfully updated latest command run of `pls daily`.")

def daily_parent(Client):
	"""One of the reward commands - `pls daily`.
 
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
			daily(Client)
		except Exception:
			if Client.config["logging"]["warning"]:
				log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls daily` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		cooldown = 23400 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)