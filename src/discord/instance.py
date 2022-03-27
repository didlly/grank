from requests import post, get
from time import sleep
from random import uniform
from utils.logger import log
from json import loads
from datetime import datetime
from utils import shared

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
					log(self.username, "WARNING", f"Discord is ratelimiting the self-bot. Sleeping for {request['retry_after']} second(s).")
					sleep(request["retry_after"])
					continue
				raise MessageSendError(f"Failed to send command `{command}`. Status code: {request.status_code} (expected 200 or 204).")

	def retreive_message(self, command):
		while True:
			time = datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")

			while (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - time).total_seconds() < self.config["cooldowns"]["timeout"]:
				request = get(f"https://discord.com/api/v10/channels/{self.channel_id}/messages", headers={"authorization": self.token})

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
				if "The default cooldown is" in latest_message["embeds"][0]["description"]:
					cooldown = int("".join(filter(str.isdigit, latest_message["embeds"][0]["description"].split("**")[1].split("**")[0])))
					log(self.username, "WARNING", f"Detected cooldown in Dank Memer's response to `{command}`. Sleeping for {cooldown} {'second' if cooldown == 1 else 'seconds'}.")
					sleep(cooldown)
					Client.send_message(command)
			else:
				break

		if (len(latest_message["embeds"]) != 0
			and "title" in latest_message["embeds"][0].keys()
			and latest_message["embeds"][0]["title"] in [
				"You're currently bot banned!", "You're currently blacklisted!"
			]):
			log(self.username, "ERROR", "Exiting self-bot instance since Grank has detected the user has been bot banned / blacklisted.")


		if "Dodge the Fireball" in latest_message["content"]:
			log(self.username, "DEBUG", "Detected dodge the fireball game.")
			while True:
				request = get(f"https://discord.com/api/v10/channels/{self.channel_id}/messages", headers={"authorization": self.token})

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
				level = latest_message["content"].split("\n")[1].replace(latest_message["content"].split("\n")[1].strip(), "").count("       ")

				if level != 1:	
					continue

				Client.interact_button(command, latest_message["components"][0]["components"][1]["custom_id"], latest_message)

				break

		elif "Catch the fish" in latest_message["content"]:
			log(self.username, "DEBUG", "Detected catch the fish game.")
			level = latest_message["content"].split("\n")[1].replace(latest_message["content"].split("\n")[1].strip(), "").count("       ")
			Client.interact_button(command, latest_message["components"][0]["components"][level]["custom_id"], latest_message)

		if self.config["auto trade"]["enabled"]:
			for key in self.config["auto trade"]:
				if key == "enabled" or key == "trader token" or not self.config["auto trade"][key]:
					continue
				elif key in latest_message["content"].lower():
					Client.send_message(f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")

					latest_message = Client.retreive_message(f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")

					Client.interact_button(f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}", latest_message["components"][0]["components"][-1]["custom_id"], latest_message)

					sleep(1)

					latest_message = Client.retreive_message(f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")

					Client.interact_button(f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}", latest_message["components"][0]["components"][-1]["custom_id"], self.config["auto trade"]["trader"]["session_id"], self.config['auto trade']['trader']['self.username'])
				elif len(latest_message["embeds"]) != 0:
					if key in latest_message["embeds"][0]["description"]:
						Client.send_message(f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")

						latest_message = Client.retreive_message(f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")


						Client.interact_button(f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}", latest_message["components"][0]["components"][-1]["custom_id"], latest_message)

						sleep(1)

						latest_message = Client.retreive_message(f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}")

						Client.interact_button(f"pls trade 1 {key} {self.config['auto trade']['trader']['self.username']}", latest_message["components"][0]["components"][-1]["custom_id"], latest_message, self.config['auto trade']['trader']['self.username'])
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
					log(self.username, "WARNING", f"Discord is ratelimiting the self-bot. Sleeping for {request['retry_after']} second(s).")
					sleep(request["retry_after"])
					continue
				raise DropdownInteractError(f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {request.status_code} (expected 200 or 204).")