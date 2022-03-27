from json import load
from json.decoder import JSONDecodeError
from utils.database import database_fixer
from random import choice
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def trivia(Client) -> None:
	Client.send_message("pls trivia")

	latest_message = Client.retreive_message("pls trivia")

	with open(f"{Client.cwd}database.json", "r") as database:
		try:
			database = load(database)
		except JSONDecodeError:
			database_fixer(Client.cwd)
			database = load(database.read())

		try:
			answer = database["trivia"][latest_message["embeds"][0]["description"].split("\n")[0].replace("*", "").replace('"', "&quot;")]
		except KeyError:
			answer = None
			log(None, "WARNING", f"Unknown trivia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Answers: `{latest_message['components'][0]['components']}`. Please create an issue on Grank highlighting this.")

	custom_id = None

	for index, possible_answer in enumerate(latest_message["components"][0]["components"]):
		if possible_answer["label"] == answer:
			custom_id = latest_message["components"][0]["components"][index]["custom_id"]

	if custom_id is None:
		log(None, "WARNING", f"Unknown answer to trivia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Answers: `{latest_message['components'][0]['components']}`. Please create an issue on Grank highlighting this.")
		custom_id = choice(latest_message["components"][0]["components"])["custom_id"]

	Client.interact_button("pls trivia", custom_id, latest_message)

def trivia_parent(Client) -> None:
	"""A trivia command - `pls trivia`.
 
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
			trivia(Client)
		except Exception:
			if Client.config["logging"]["warning"]:
				log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls trivia` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		if Client.config["cooldowns"]["patron"]:
			cooldown = 3 - (end - start)
		else:
			cooldown = 5 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)