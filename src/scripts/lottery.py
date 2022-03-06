from json import load, dumps
from datetime import datetime
from discord.message import send_message, retreive_message
from discord.button import interact_button
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def lottery(username, channel_id, token, config, user_id, cwd, session_id):
	with open(f"{cwd}/database.json", "r") as data:
		data = load(data)

		if "lottery" not in data.keys():
			send_message(channel_id, token, config, username, "pls lottery")

			latest_message = retreive_message(channel_id, token, config, username, "pls lottery", user_id)

			if latest_message is None:
				return

			interact_button(channel_id, token, config, username, "pls lottery", latest_message["components"][0]["components"][-1]["custom_id"], latest_message, session_id)
			
			data["lottery"] = datetime.now().strftime("%x-%X")

			with open(f"{cwd}/database.json", "w") as data_file:
				data_file.write(dumps(data))
			
			if config["logging"]["debug"]:
				log(username, "DEBUG", "Successfully updated latest command run of `pls lottery`.")
		elif (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["lottery"], "%x-%X")).total_seconds() > config["lottery"]["cooldown"]:
			send_message(channel_id, token, config, username, "pls lottery")

			latest_message = retreive_message(channel_id, token, config, username, "pls lottery", user_id)

			if latest_message is None:
				return
			
			interact_button(channel_id, token, config, username, "pls lottery", latest_message["components"][0]["components"][-1]["custom_id"], latest_message, session_id)

			data["lottery"] = datetime.now().strftime("%x-%X")
			
			with open(f"{cwd}/database.json", "w") as database:
				database.write(dumps(data))
			
			if config["logging"]["debug"]:
				log(username, "DEBUG", "Successfully updated latest command run of `pls lottery`.")

def lottery_parent(username, channel_id, token, config, user_id, cwd, session_id):
	while True:
		while not data[channel_id]:
			pass

		data[channel_id] = False

		start = time()

		try:
			lottery(username, channel_id, token, config, user_id, cwd, session_id)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls lottery` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		cooldown = config["lottery"]["cooldown"] - (end - start)

		if cooldown > 0:
			sleep(cooldown)