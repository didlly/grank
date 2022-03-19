from discord.message import send_message
from random import randint
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def snakeeyes(username, channel_id, token, config):
	amount = config['snakeeyes']['amount'] if not config['snakeeyes']['random'] else randint(config['snakeeyes']['minimum'], config['snakeeyes']['maximum'])

	send_message(channel_id, token, config, username, f"pls snakeeyes {amount}")
	
	

def snakeeyes_parent(username, channel_id, token, config):
	while True:
		while not data[channel_id] or not data[username]:
			pass

		data[channel_id] = False

		start = time()

		try:
			snakeeyes(username, channel_id, token, config)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls snakeeyes` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		if config["cooldowns"]["patron"]:
			cooldown = 5 - (end - start)
		else:
			cooldown = 10 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)