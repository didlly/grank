from json import load, dumps
from discord.message import send_message
from utils.logger import log
from datetime import datetime
from time import time, sleep
from sys import exc_info
from utils.shared import data

def daily(username, channel_id, token, config, cwd):
	with open(f"{cwd}/database.json", "r") as data:
		data = load(data)

		if data["daily"] == "None":
			send_message(channel_id, token, config, username, "pls daily")
			
			data["daily"] = datetime.now().strftime("%x-%X")

			with open(f"{cwd}/database.json", "w") as data_file:
				data_file.write(dumps(data))
			
			if config["logging"]["debug"]:
				log(username, "DEBUG", "Successfully updated latest command run of `pls daily`.")
		elif (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["daily"], "%x-%X")).total_seconds() > 23400:
			send_message(channel_id, token, config, username, "pls daily")

			data["daily"] = datetime.now().strftime("%x-%X")
			
			with open(f"{cwd}/database.json", "w") as database:
				database.write(dumps(data))
			
			if config["logging"]["debug"]:
				log(username, "DEBUG", "Successfully updated latest command run of `pls daily`.")

def daily_parent(username, channel_id, token, config, cwd):
	while True:
		while not data[channel_id]:
			pass

		data[channel_id] = False

		start = time()

		try:
			daily(username, channel_id, token, config, cwd)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls daily` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		cooldown = 23400 - (end - start)

		if cooldown > 0:
			sleep(cooldown)