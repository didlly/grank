from discord.message import send_message, retreive_message
from discord.button import interact_button
from random import randint
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def blackjack(username, channel_id, token, config, user_id, session_id):
	amount = (randint(config['blackjack']['minimum'],
	                  config['blackjack']['maximum'])
	          if config['blackjack']['random'] else config['blackjack']['amount'])

	send_message(channel_id, token, config, username, f"pls bj {amount}")

	while True:
		latest_message = retreive_message(channel_id, token, config, username, f"pls bj {amount}", user_id, session_id)

		if latest_message is None:
			return

		if "coins, dont try and lie to me hoe." in latest_message["content"] or "You have no coins in your wallet to gamble with lol." in latest_message["content"]:
			log(username, "WARNING", f"Insufficient funds to run the command `pls bj {amount}`. Aborting command.")
			return

		if ("description" in latest_message["embeds"][0].keys()
		    and "You lost" in latest_message["embeds"][0]["description"]):
			return

		total = int("".join(filter(str.isdigit, latest_message["embeds"][0]["fields"][0]["value"].split("\n")[-1])))

		if total < 19:
			interact_button(channel_id, token, config, username, f"pls bj {amount}", latest_message["components"][0]["components"][0]["custom_id"], latest_message, session_id)
		else:
			interact_button(channel_id, token, config, username, f"pls bj {amount}", latest_message["components"][0]["components"][1]["custom_id"], latest_message, session_id)
			break
	
	

def blackjack_parent(username, channel_id, token, config, user_id, session_id):
	while True:
		while not data[channel_id] or not data[username]:
			pass

		data[channel_id] = False

		start = time()

		try:
			blackjack(username, channel_id, token, config, user_id, session_id)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls blackjack` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		if config["cooldowns"]["patron"]:
			cooldown = 5 - (end - start)
		else:
			cooldown = 10 - (end - start)

		if cooldown > 0:
			sleep(cooldown)