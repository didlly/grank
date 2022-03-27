from requests import get, post
from json import load, loads, dumps
from json.decoder import JSONDecodeError
from utils.database import database_fixer
from utils.logger import log
from datetime import datetime
from time import time, sleep
from sys import exc_info
from utils.shared import data

def vote(Client):
	with open(f"{Client.cwd}database.json", "r") as data:
		try:
			data = load(data)
		except JSONDecodeError:
			database_fixer(Client.cwd)
			data = load(data)

		if "vote" not in data.keys():
			json = {
				"authorize": True,
				"permissions": 0
			}
   
			req = post("https://discord.com/api/v10/oauth2/authorize?client_id=477949690848083968&response_type=code&scope=identify", headers={"authorization": Client.token}, json=json)

			code = loads(req.content.decode())["location"].split("code=")[-1]

			req = get(f"https://discordbotlist.com/api/v1/oauth?code={code}")

			dbl_token = loads(req.content.decode())["token"]

			req = loads(post("https://discordbotlist.com/api/v1/bots/270904126974590976/upvote", headers={"authorization": dbl_token}).content.decode())
   
			if req["success"]:
				if Client.config["logging"]["debug"]:
					log(Client.username, "DEBUG", "Succesfully voted for Dank Memer on Discord Bot List")
			else:
				if req["message"] == "User has already voted.":
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", "Already voted for Dank Memer on Discord Bot List in the past 24 hours.")
				elif Client.config["logging"]["warning"]:
					log(Client.username, "WARNING", "Failed to vote for Dank Memer on Discord Bot List.")
				return
     
			data["vote"] = datetime.now().strftime("%x-%X")

			with open(f"{Client.cwd}database.json", "w") as data_file:
				data_file.write(dumps(data))
			
			if Client.config["logging"]["debug"]:
				log(Client.username, "DEBUG", "Successfully updated latest vote.")
		elif (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(data["vote"], "%x-%X")).total_seconds() > 43200:
			json = {
				"authorize": True,
				"permissions": 0
			}
   
			req = post("https://discord.com/api/v10/oauth2/authorize?client_id=477949690848083968&response_type=code&scope=identify", headers={"authorization": Client.token}, json=json)

			code = loads(req.content.decode())["location"].split("code=")[-1]

			req = get(f"https://discordbotlist.com/api/v1/oauth?code={code}")

			dbl_token = loads(req.content.decode())["token"]

			req = loads(post("https://discordbotlist.com/api/v1/bots/270904126974590976/upvote", headers={"authorization": dbl_token}).content.decode())
   
			if req["success"]:
				if Client.config["logging"]["debug"]:
					log(Client.username, "DEBUG", "Succesfully voted for Dank Memer on Discord Bot List")
			else:
				if req["message"] == "User has already voted.":
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", "Already voted for Dank Memer on Discord Bot List in the past 24 hours.")
				elif Client.config["logging"]["warning"]:
					log(Client.username, "WARNING", "Failed to vote for Dank Memer on Discord Bot List.")
				return

			data["vote"] = datetime.now().strftime("%x-%X")
			
			with open(f"{Client.cwd}database.json", "w") as database:
				database.write(dumps(data))
			
			if Client.config["logging"]["debug"]:
				log(Client.username, "DEBUG", "Successfully updated latest vote.")

def vote_parent(Client):
	"""A function that votes for Dank Memer on Discord Bot List.
 
	Required item(s): None

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
			vote(Client)
		except Exception:
			if Client.config["logging"]["warning"]:
				log(Client.username, "WARNING", f"An unexpected error occured during the voting process: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		cooldown = 43200 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)