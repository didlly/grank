from datetime import datetime
from json import dumps

from utils.shared import data


def shifts(Client) -> None:
	"""A function which controls shifts.

	Args:
		username (str): The username of the account.
		config (dict): The dictionary version of the configuration file.
		cwd (str): The current working directory.
	"""
 
	while True:
		if not data[Client.username] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(Client.database["shifts"]["passive"], "%x-%X")).total_seconds() >= Client.config["shifts"]["passive"]:
			data[Client.username] = True
			Client.database["shifts"]["passive"] = datetime.now().strftime("%x-%X")
			Client.database["shifts"]["active"] = datetime.now().strftime("%x-%X")
			Client.database_file.write(dumps(Client.database))
			Client.log("DEBUG", "Beginning active phase.")
		elif data[Client.username] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(Client.database["shifts"]["active"], "%x-%X")).total_seconds() >= Client.config["shifts"]["active"]:
			data[Client.username] = False
			Client.database["shifts"]["active"] = datetime.now().strftime("%x-%X")
			Client.database["shifts"]["passive"] = datetime.now().strftime("%x-%X")
			Client.database_file.write(dumps(Client.database))
			Client.log("DEBUG", "Beginning passive phase.")