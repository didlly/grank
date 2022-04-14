from datetime import datetime
from json import loads, dumps
from json.decoder import JSONDecodeError
from utils.console import fore, style
from random import uniform
from time import sleep

from requests import get, post
from utils import shared
from utils.logger import log


class MessageSendError(Exception):
	pass

class ResponseTimeout(Exception):
	pass

class ButtonInteractError(Exception):
	pass

class DropdownInteractError(Exception):
	pass

class Client(object):
	"""The Class containing all the code for the self-bot to interact with Discord.

	Procedures:
		retreive_message()
  
			- Retreives the latest message from Dank Memer.
			Args:
				command (str): The command that the message is being retreived for.

			Returns:
				latest_message (dict / None): The dictionary version of Dank Memer's latest message (or NoneType if it couldn't be found).

	Functions:
		send_message()
			- Sends a message.
   
			Args:
				command (str): The command that the message is being retreived for.

			Returns:
				sent (bool): A boolean value that tells Grank whether the message was sent succesfully or not.
	
		interact_button()
			- Interacts with a button.
   
			Args:
				command (str): The command that the message is being retreived for.
				custom_id (str): The ID of the button to be clicked.
				latest_message (dict): The dictionary version of Dank Memer's message that contains the button. 
				token (str) [OPTIONAL]: The token of the account that should interact with the button if it should not be the one initialized in the __init__ function of this Class.

			Returns:
				interacted (bool): A boolean value that tells Grank whether the button was successfully interacted with or not.
	
		interact_dropdown()
 			 - Interacts with a dropdown.
	 
			Args:
				command (str): The command that the message is being retreived for.
				custom_id (str): The ID of the dropdown to be interacted with.
	   			custom_id (str): The ID of the dropdown choice to be selected.
				latest_message (dict): The dictionary version of Dank Memer's message that contains the dropdown. 

			Returns:
				interacted (bool): A boolean value that tells Grank whether the dropdown was successfully interacted with or not.
	"""
	
	def __init__(self, config, user_id, username, session_id, channel_id, token, cwd):
		self.config = config
		self.user_id = user_id
		self.username = username
		self.session_id = session_id
		self.channel_id = channel_id
		self.token = token
		self.cwd = cwd
		self.log_file = open(f"{cwd}logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log", "a")
  
		data = open(f"{cwd}database.json", "r+", errors="ignore")

		for count in range(1, 6):
			try:
				self.database = loads(data.read())
				break
			except JSONDecodeError:
				log(None, "WARNING", "Database file is corrupted. Re-downloading now.")

				req = loads(get("https://raw.githubusercontent.com/didlly/grank/main/src/database.json", allow_redirects=True).content)
				req["shifts"]["active"] = datetime.now().strftime("%x-%X")
				req["shifts"]["passive"] = datetime.now().strftime("%x-%X")

				log(None, "DEBUG", "Retreived new database file.")
				
				with open(f"{cwd}database.json", "w") as db:
					log(None, "DEBUG", f"Opened `{cwd}database.json`.")
					db.seek(0)
					db.truncate()
					db.write(dumps(req))
					log(None, "DEBUG", f"Wrote new database to `{cwd}database.json`.")
					
				log(None, "DEBUG", f"Closed `{cwd}database.json`.")
		
		if count == 5:
			log(None, "ERROR", "Database error. Please close and re-open Grank.")
   
		class database:
			def write(content: str):
				data.seek(0)
				data.truncate()
				data.write(content)
    
		self.database_file = database
	
	def send_message(self, command):
		if self.config["typing indicator"]["enabled"]:
			request = post(f"https://discord.com/api/v9/channels/{self.channel_id}/typing", headers={"authorization": self.token})
			sleep(uniform(self.config["typing indicator"]["minimum"], self.config["typing indicator"]["maximum"]))

		while True:
			request = post(f"https://discord.com/api/v10/channels/{self.channel_id}/messages?limit=1", headers={"authorization": self.token}, json={"content": command})

			if request.status_code in [200, 204]:
				if self.config["logging"]["debug"]:
						log(self.username, "DEBUG", f"Successfully sent command `{command}`.")
				return
			else:
				if self.config["logging"]["warning"]:
					log(self.username, "WARNING", f"Failed to send command `{command}`. Status code: {request.status_code} (expected 200 or 204).")
				if request.status_code == 429:
					request = loads(request.content)
					if self.config["logging"]["warning"]:
						log(self.username, "WARNING", f"Discord is ratelimiting the self-bot. Sleeping for {request['retry_after']} second(s).")
					sleep(request["retry_after"])
					continue
				raise MessageSendError(f"Failed to send command `{command}`. Status code: {request.status_code} (expected 200 or 204).")

	def retreive_message(self, command):
		while True:
			time = datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")

			while (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - time).total_seconds() < self.config["cooldowns"]["timeout"]:
				request = get(f"https://discord.com/api/v10/channels/{self.channel_id}/messages?limit=1", headers={"authorization": self.token})

				if request.status_code != 200:
					continue

				latest_message = loads(request.text)[0]

				if latest_message["author"]["id"] != "270904126974590976":
					continue

				if "referenced_message" in latest_message.keys():
					if latest_message["referenced_message"]["author"]["id"] == self.user_id:
						if self.config["logging"]["debug"]:
							log(self.username, "DEBUG", f"Got Dank Memer's response to command `{command}`.")
						break
				else:
					if self.config["logging"]["debug"]:
						log(self.username, "DEBUG", f"Got Dank Memer's response to command `{command}`.")
					break

			if latest_message["author"]["id"] != "270904126974590976":
				raise TimeoutError(f"Timeout exceeded for response from Dank Memer ({self.config['cooldowns']['timeout']} {'second' if self.config['cooldowns']['timeout'] == 1 else 'seconds'}). Aborting command.")
			elif len(latest_message["embeds"]) > 0:
				if "description" not in latest_message["embeds"][0].keys():
					break
				if ("The default cooldown is" not in latest_message["embeds"][0]
				    ["description"]):
					break
				cooldown = int("".join(filter(str.isdigit, latest_message["embeds"][0]["description"].split("**")[1].split("**")[0])))
				if self.config["logging"]["warning"]:
					log(self.username, "WARNING", f"Detected cooldown in Dank Memer's response to `{command}`. Sleeping for {cooldown} {'second' if cooldown == 1 else 'seconds'}.")
				sleep(cooldown)
				Client.send_message(self, command)
			else:
				break

		if (len(latest_message["embeds"]) != 0
			and "title" in latest_message["embeds"][0].keys()
			and latest_message["embeds"][0]["title"] in [
				"You're currently bot banned!", "You're currently blacklisted!"
			]):
			log(self.username, "ERROR", "Exiting self-bot instance since Grank has detected the user has been bot banned / blacklisted.")


		if self.config["auto trade"]["enabled"]:
			for key in self.config["auto trade"]:
				if key == "enabled" or key == "trader token" or not self.config["auto trade"][key]:
					continue
				elif key in latest_message["content"].lower():
					Client.send_message(self, f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")

					latest_message = Client.retreive_message(self, f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")

					Client.interact_button(self, f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}", latest_message["components"][0]["components"][-1]["custom_id"], latest_message)

					sleep(1)

					latest_message = Client.retreive_message(self, f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")

					Client.interact_button(self, f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}", latest_message["components"][0]["components"][-1]["custom_id"], self.config["auto trade"]["trader"]["session_id"], self.config['auto trade']['trader']['self.username'])
				elif len(latest_message["embeds"]) != 0:
					if key in latest_message["embeds"][0]["description"]:
						Client.send_message(self, f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")

						latest_message = Client.retreive_message(self, f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")


						Client.interact_button(self, f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}", latest_message["components"][0]["components"][-1]["custom_id"], latest_message)

						sleep(1)

						latest_message = Client.retreive_message(self, f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")

						Client.interact_button(self, f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}", latest_message["components"][0]["components"][-1]["custom_id"], latest_message, self.config['auto trade']['trader']['self.username'])
		return latest_message

	def interact_button(self, command, custom_id, latest_message, token=None):
		data = {
			"application_id": 270904126974590976,
			"channel_id": self.channel_id,
			"type": 3,
			"data": {
				"component_type": 2,
				"custom_id": custom_id
			},
			"guild_id": latest_message["message_reference"]["guild_id"] if "message_reference" in latest_message.keys() else shared.data[f"{self.channel_id}_guild"],
			"message_flags": 0,
			"message_id": latest_message["id"],
			"session_id": self.session_id
		}

		while True:
			request = post("https://discord.com/api/v10/interactions", headers={"authorization": self.token if token is None else token}, json=data)

			if request.status_code in [200, 204]:
				if self.config["logging"]["debug"]:
					log(self.username, "DEBUG", f"Successfully interacted with button on Dank Memer's response to command `{command}`.")
				return
			else:
				if self.config["logging"]["warning"]:
					log(self.username, "WARNING", f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {request.status_code} (expected 200 or 204).")
				if request.status_code == 429:
					request = loads(request.content)
					if self.config["logging"]["warning"]:
						log(self.username, "WARNING", f"Discord is ratelimiting the self-bot. Sleeping for {request['retry_after']} second(s).")
					sleep(request["retry_after"])
					continue
				raise ButtonInteractError(f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {request.status_code} (expected 200 or 204).")

	def interact_dropdown(self, command, custom_id, option_id, latest_message):
		data = {
			"application_id": 270904126974590976,
			"channel_id": self.channel_id,
			"type": 3,
			"data": {
				"component_type": 3,
				"custom_id": custom_id,
				"type": 3,
				"values": [option_id]
					},
			"guild_id": latest_message["message_reference"]["guild_id"] if "message_reference" in latest_message.keys() else shared.data[f"{self.channel_id}_guild"],
			"message_flags": 0,
			"message_id": latest_message["id"],
			"session_id": self.session_id
			}

		while True:
			request = post("https://discord.com/api/v10/interactions", headers={"authorization": self.token}, json=data)
   
			if request.status_code in [200, 204]:
				if self.config["logging"]["debug"]:
					log(self.username, "DEBUG", f"Successfully interacted with dropdown on Dank Memer's response to command `{command}`.")
				return
			else:
				if self.config["logging"]["warning"]:
					log(self.username, "WARNING", f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {request.status_code} (expected 200 or 204).")
				if request.status_code == 429:
					request = loads(request.content)
					if self.config["logging"]["warning"]:
						log(self.username, "WARNING", f"Discord is ratelimiting the self-bot. Sleeping for {request['retry_after']} second(s).")
					sleep(request["retry_after"])
					continue
				raise DropdownInteractError(f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {request.status_code} (expected 200 or 204).")
 
	def log(self, level: str, text: str) -> None:
		"""A function which logs messages to the console and to the log file.

		Args:
			level (str): The type of message to be logged.
			text (str): The message to be logged.

		Returns:
			None
		"""
    
		time = datetime.now().strftime("[%x-%X]")

		print(f"{time}{f' - {fore.Bright_Magenta}{self.username}{style.RESET_ALL}' if self.username is not None else ''} - {style.Italic}{fore.Bright_Red if level == 'ERROR' else fore.Bright_Blue if level == 'DEBUG' else fore.Bright_Yellow}[{level}]{style.RESET_ALL} | {text}")

		self.log_file.write(f"{time} - {self.username} - {level} | {text}\n")
		self.log_file.flush()
  
		if level == "ERROR":
			_ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
			exit(1)
		