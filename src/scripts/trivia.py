from discord.message import send_message, retreive_message
from json import load
from discord.button import interact_button
from random import choice
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def trivia(username, channel_id, token, config, user_id, session_id, cwd):
	send_message(channel_id, token, config, username, "pls trivia")

	latest_message = retreive_message(channel_id, token, config, username, "pls trivia", user_id)

	if latest_message is None:
		return

	try:
		answer = load(open(f"{cwd}database.json", "r"))["trivia"][latest_message["embeds"][0]["description"].split("\n")[0].replace("*", "").replace('"', "&quot;")]
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

	interact_button(channel_id, token, config, username, "pls trivia", custom_id, latest_message, session_id)

def trivia_parent(username, channel_id, token, config, user_id, session_id, cwd):
	while True:
		while not data[channel_id] or not data[username]:
			pass

		data[channel_id] = False

		start = time()

		try:
			trivia(username, channel_id, token, config, user_id, session_id, cwd)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls trivia` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		if config["cooldowns"]["patron"]:
			cooldown = 3 - (end - start)
		else:
			cooldown = 5 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)