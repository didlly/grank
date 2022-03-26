from json import load, dumps
from datetime import datetime
from random import randint, choice
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def stream(Client) -> None:
	with open(f"{Client.cwd}database.json", "r") as data:
		data = load(data)

		if "stream" not in data.keys():
			Client.send_message("pls stream")

			latest_message = Client.retreive_message("pls stream")

			if "title" in latest_message["embeds"][0].keys():
				if "Keyboard" in latest_message["embeds"][0]["description"]:
					if Client.config["logging"]["debug"]:
						log(Client.username, "DEBUG", "User does not have item `keyboard`. Buying laptop now.")

					if Client.config["auto buy"] and Client.config["auto buy"]["keyboard"]:
						from scripts.buy import buy
						buy(Client, "keyboard", Client.cwd)
						return
					elif Client.config["logging"]["warning"]:
						log(
							Client.username,
							"WARNING",
							f"A keyboard is required for the command `pls stream`. However, since {'autobuy is off for keyboards,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
						)

				if "Mouse" in latest_message["embeds"][0]["description"]:
					if Client.config["logging"]["debug"]:
						log(Client.username, "DEBUG", "User does not have item `mouse`. Buying laptop now.")

					if Client.config["auto buy"] and Client.config["auto buy"]["mouse"]:
						from scripts.buy import buy
						buy(Client, "mouse", Client.cwd)
						return
					elif Client.config["logging"]["warning"]:
						log(
							Client.username,
							"WARNING",
							f"A mouse is required for the command `pls stream`. However, since {'autobuy is off for mouses,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
						)

			if len(latest_message["components"][0]["components"]) == 3:
				Client.interact_button("pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message)

				latest_message = Client.retreive_message("pls stream")

				Client.interact_dropdown("pls stream", latest_message["components"][0]["components"][0]["custom_id"], choice(latest_message["components"][0]["components"][0]["options"])["value"], latest_message)

				Client.interact_button("pls stream", latest_message["components"][-1]["components"][0]["custom_id"], latest_message)

			latest_message = Client.retreive_message("pls stream")

			if int(latest_message["embeds"][0]["fields"][5]["value"].replace("`", "")) > 0 and Client.config["stream"]["ads"]:
				Client.interact_button("pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message)
			else:
				button = randint(1, 2) if Client.config["stream"]["chat"] and Client.config["stream"]["donations"] else 1 if Client.config["stream"]["chat"] else 2 if Client.config["stream"]["donations"] else None
    
				if button is None:
					return

				Client.interact_button("pls stream", latest_message["components"][0]["components"][button]["custom_id"], latest_message)

			Client.interact_button("pls stream", latest_message["components"][-1]["components"][-1]["custom_id"], latest_message)

			data["stream"] = datetime.now().strftime("%x-%X")

			with open(f"{Client.cwd}database.json", "w") as data_file:
				data_file.write(dumps(data))

			if Client.config["logging"]["debug"]:
				log(Client.username, "DEBUG", "Successfully updated latest command run of `pls stream`.")
		elif (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["stream"], "%x-%X")).total_seconds() > 600:
			Client.send_message("pls stream")

			latest_message = Client.retreive_message("pls stream")

			if "title" in latest_message["embeds"][0].keys():
				if "Keyboard" in latest_message["embeds"][0]["description"]:
					if Client.config["logging"]["debug"]:
						log(Client.username, "DEBUG", "User does not have item `keyboard`. Buying keyboard now.")

					if Client.config["auto buy"] and Client.config["auto buy"]["keyboard"]:
						from scripts.buy import buy
						buy(Client, "keyboard", Client.cwd)
						return
					elif Client.config["logging"]["warning"]:
						log(
							Client.username,
							"WARNING",
							f"A keyboard is required for the command `pls stream`. However, since {'autobuy is off for keyboards,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
						)

				if "Mouse" in latest_message["embeds"][0]["description"]:
					if Client.config["logging"]["debug"]:
						log(Client.username, "DEBUG", "User does not have item `mouse`. Buying mouse now.")

					if Client.config["auto buy"] and Client.config["auto buy"]["mouse"]:
						from scripts.buy import buy
						buy(Client, "mouse", Client.cwd)
						return
					elif Client.config["logging"]["warning"]:
						log(
							Client.username,
							"WARNING",
							f"A mouse is required for the command `pls stream`. However, since {'autobuy is off for mouses,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
						)

			if len(latest_message["components"][0]["components"]) == 3:
				Client.interact_button("pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message)

				latest_message = Client.retreive_message("pls stream")

				Client.interact_dropdown("pls stream", latest_message["components"][0]["components"][0]["custom_id"], choice(latest_message["components"][0]["components"][0]["options"])["value"], latest_message)

				Client.interact_button("pls stream", latest_message["components"][-1]["components"][0]["custom_id"], latest_message)

			latest_message = Client.retreive_message("pls stream")

			if int(latest_message["embeds"][0]["fields"][5]["value"].replace("`", "")) > 0 and Client.config["stream"]["ads"]:
				Client.interact_button("pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message)
			else:
				button = randint(1, 2) if Client.config["stream"]["chat"] and Client.config["stream"]["donations"] else 1 if Client.config["stream"]["chat"] else 2 if Client.config["stream"]["donations"] else None
    
				if button is None:
					return

				Client.interact_button("pls stream", latest_message["components"][0]["components"][button]["custom_id"], latest_message)

			Client.interact_button("pls stream", latest_message["components"][-1]["components"][-1]["custom_id"], latest_message)

			data["stream"] = datetime.now().strftime("%x-%X")

			with open(f"{Client.cwd}database.json", "w") as data_file:
				data_file.write(dumps(data))

			if Client.config["logging"]["debug"]:
				log(Client.username, "DEBUG", "Successfully updated latest command run of `pls stream`.")

def stream_parent(Client) -> None:
	"""A streaming command - `pls stream`.
 
	Required item(s): keyboard, mouse

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
			stream(Client)
		except Exception:
			log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls stream` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		cooldown = 610 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)