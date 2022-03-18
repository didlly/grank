from json import load, dumps
from datetime import datetime
from discord.message import send_message, retreive_message
from discord.button import interact_button
from discord.dropdown import interact_dropdown
from random import randint, choice
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def stream(username, channel_id, token, config, user_id, cwd, session_id):
	with open(f"{cwd}database.json", "r") as data:
		data = load(data)

		if "stream" not in data.keys():
			send_message(channel_id, token, config, username, "pls stream")

			latest_message = retreive_message(channel_id, token, config, username, "pls stream", user_id)

			if latest_message is None:
				return

			if "title" in latest_message["embeds"][0].keys():
				if "Keyboard" in latest_message["embeds"][0]["description"]:
					if config["logging"]["debug"]:
						log(username, "DEBUG", "User does not have item `keyboard`. Buying laptop now.")

					if config["auto buy"] and config["auto buy"]["keyboard"]:
						from scripts.buy import buy
						buy(username, channel_id, token, config, user_id, cwd, "keyboard")
						return
					elif config["logging"]["warning"]:
						log(
						    username,
						    "WARNING",
						    f"A keyboard is required for the command `pls stream`. However, since {'autobuy is off for keyboards,' if config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
						)
						return

				if "Mouse" in latest_message["embeds"][0]["description"]:
					if config["logging"]["debug"]:
						log(username, "DEBUG", "User does not have item `mouse`. Buying laptop now.")

					if config["auto buy"] and config["auto buy"]["mouse"]:
						from scripts.buy import buy
						buy(username, channel_id, token, config, user_id, cwd, "mouse")
						return
					elif config["logging"]["warning"]:
						log(
						    username,
						    "WARNING",
						    f"A mouse is required for the command `pls stream`. However, since {'autobuy is off for mouses,' if config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
						)
						return

			if len(latest_message["components"][0]["components"]) == 3:
				interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message, session_id)

				latest_message = retreive_message(channel_id, token, config, username, "pls stream", user_id)

				if latest_message is None:
					return

				interact_dropdown(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][0]["custom_id"], choice(latest_message["components"][0]["components"][0]["options"])["value"], latest_message, session_id)

				interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][-1]["components"][0]["custom_id"], latest_message, session_id)

			latest_message = retreive_message(channel_id, token, config, username, "pls stream", user_id)

			if int(latest_message["embeds"][0]["fields"][5]["value"].replace("`", "")) > 0 and config["stream"]["ads"]:
				interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message, session_id)
			else:
				button = randint(1, 2) if config["stream"]["chat"] and config["stream"]["donations"] else 1 if config["stream"]["chat"] else 2 if config["stream"]["donations"] else None
				if button is None:
					return

				interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][button]["custom_id"], latest_message, session_id)

			interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][-1]["components"][-1]["custom_id"], latest_message, session_id)

			data["stream"] = datetime.now().strftime("%x-%X")

			with open(f"{cwd}database.json", "w") as data_file:
				data_file.write(dumps(data))

			if config["logging"]["debug"]:
				log(username, "DEBUG", "Successfully updated latest command run of `pls stream`.")
		elif (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["stream"], "%x-%X")).total_seconds() > 600:
			send_message(channel_id, token, config, username, "pls stream")

			latest_message = retreive_message(channel_id, token, config, username, "pls stream", user_id)

			if latest_message is None:
				return

			if "title" in latest_message["embeds"][0].keys():
				if "Keyboard" in latest_message["embeds"][0]["description"]:
					if config["logging"]["debug"]:
						log(username, "DEBUG", "User does not have item `keyboard`. Buying laptop now.")

					if config["auto buy"] and config["auto buy"]["keyboard"]:
						from scripts.buy import buy
						buy(username, channel_id, token, config, user_id, cwd, "keyboard")
						return
					elif config["logging"]["warning"]:
						log(
						    username,
						    "WARNING",
						    f"A keyboard is required for the command `pls stream`. However, since {'autobuy is off for keyboards,' if config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
						)
						return

				if "Mouse" in latest_message["embeds"][0]["description"]:
					if config["logging"]["debug"]:
						log(username, "DEBUG", "User does not have item `mouse`. Buying laptop now.")

					if config["auto buy"] and config["auto buy"]["mouse"]:
						from scripts.buy import buy
						buy(username, channel_id, token, config, user_id, cwd, "mouse")
						return
					elif config["logging"]["warning"]:
						log(
						    username,
						    "WARNING",
						    f"A mouse is required for the command `pls stream`. However, since {'autobuy is off for mouses,' if config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
						)
						return

			if len(latest_message["components"][0]["components"]) == 3:
				interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message, session_id)

				latest_message = retreive_message(channel_id, token, config, username, "pls stream", user_id)

				if latest_message is None:
					return

				interact_dropdown(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][0]["custom_id"], choice(latest_message["components"][0]["components"][0]["options"])["value"], latest_message, session_id)

				interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][-1]["components"][0]["custom_id"], latest_message, session_id)

			latest_message = retreive_message(channel_id, token, config, username, "pls stream", user_id)

			if int(latest_message["embeds"][0]["fields"][5]["value"].replace("`", "")) > 0 and config["stream"]["ads"]:
				interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message, session_id)
			else:
				button = randint(1, 2) if config["stream"]["chat"] and config["stream"]["donations"] else 1 if config["stream"]["chat"] else 2 if config["stream"]["donations"] else None

				if button is None:
					return

				interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][0]["components"][button]["custom_id"], latest_message, session_id)

			interact_button(channel_id, token, config, username, "pls stream", latest_message["components"][-1]["components"][-1]["custom_id"], latest_message, session_id)

			data["stream"] = datetime.now().strftime("%x-%X")

			with open(f"{cwd}database.json", "w") as database:
				database.write(dumps(data))

			if config["logging"]["debug"]:
				log(username, "DEBUG", "Successfully updated latest command run of `pls stream`.")

def stream_parent(username, channel_id, token, config, user_id, cwd, session_id):
	while True:
		while not data[channel_id] or not data[username]:
			pass

		data[channel_id] = False

		start = time()

		try:
			stream(username, channel_id, token, config, user_id, cwd, session_id)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls stream` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		cooldown = 610 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)