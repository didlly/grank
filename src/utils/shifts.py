from json import load, dumps
from json.decoder import JSONDecodeError
from utils.database import database_fixer
from datetime import datetime
from utils.logger import log
from utils.shared import data
from time import sleep

def shifts(username: str, config: dict, cwd: str) -> None:
	"""A function which controls shifts.

	Args:
		username (str): The username of the account.
		config (dict): The dictionary version of the configuration file.
		cwd (str): The current working directory.
	"""
 
	while True:
		with open(f"{cwd}database.json", "r") as database_file:
			try:
				database = load(database_file)
			except JSONDecodeError:
				database_fixer(cwd)
				database = load(database_file.read())
   
			if "last active" not in database["shifts"]:
				database["shifts"]["last active"] = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
				data[username] = True
			elif (datetime.strptime(datetime.now().strftime("%Y:%m:%d-%H:%M:%S"), "%Y:%m:%d-%H:%M:%S") - datetime.strptime(database["shifts"]["last active"], "%Y:%m:%d-%H:%M:%S")).total_seconds() > config["shifts"]["active"]:
				data[username] = False
				log(username, "DEBUG", "Beginning sleep phase.")
				sleep(config["shifts"]["passive"])
				data[username] = True
				log(username, "DEBUG", "Beginning active phase.")
				database["shifts"]["last active"] = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")

		with open(f"{cwd}database.json", "w") as database_file:
			database_file.write(dumps(database))
  
		cooldown = (datetime.strptime(datetime.now().strftime("%Y:%m:%d-%H:%M:%S"), "%Y:%m:%d-%H:%M:%S") - datetime.strptime(database["shifts"]["last active"], "%Y:%m:%d-%H:%M:%S")).total_seconds() - config["shifts"]["active"]
   
		if cooldown > 0:
			sleep(cooldown)