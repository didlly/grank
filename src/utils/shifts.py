from json import load, dumps
from datetime import datetime
from utils.shared import data
from time import sleep

def shifts(username, config, cwd):
	while True:
		with open(f"{cwd}database.json", "r+") as database:
			database = load(database)
   
			if "last active" not in database["shifts"]:
				database["shifts"]["last active"] = datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
				data[username] = True
			elif (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["shifts"]["last active"], "%x-%X")).total_seconds() > config["shifts"]["active"]:
				data[username] = False
				sleep(config["shifts"]["passive"])
				data[username] = True
				database["shifts"]["last active"] = datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")
	
			database.write(dumps(data))
   
			cooldown = (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["shifts"]["last active"], "%x-%X")).total_seconds() - config["shifts"]["active"]
   
			if cooldown > 0:
				sleep(cooldown)