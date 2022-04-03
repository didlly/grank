from json import dumps
from datetime import datetime
from utils.logger import log
from utils.shared import data
from time import sleep

def shifts(Client) -> None:
	"""A function which controls shifts.

	Args:
		username (str): The username of the account.
		config (dict): The dictionary version of the configuration file.
		cwd (str): The current working directory.
	"""
 
	while True:
		if (datetime.strptime(datetime.now().strftime("%Y:%m:%d-%H:%M:%S"), "%Y:%m:%d-%H:%M:%S") - datetime.strptime(Client.database["shifts"]["last active"], "%Y:%m:%d-%H:%M:%S")).total_seconds() > Client.config["shifts"]["active"]:
			data[Client.username] = False
			log(Client.username, "DEBUG", "Beginning sleep phase.")
			sleep(Client.config["shifts"]["passive"])
			data[Client.username] = True
			log(Client.username, "DEBUG", "Beginning active phase.")
			Client.database["shifts"]["last active"] = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
		
		Client.database_file.write(dumps(Client.database))

		cooldown = (datetime.strptime(datetime.now().strftime("%Y:%m:%d-%H:%M:%S"), "%Y:%m:%d-%H:%M:%S") - datetime.strptime(Client.database["shifts"]["last active"], "%Y:%m:%d-%H:%M:%S")).total_seconds() - Client.config["shifts"]["active"]

		if cooldown > 0:
			sleep(cooldown)