from discord.message import send_message
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def custom(username, channel_id, token, config, command):
	send_message(channel_id, token, config, username, command)

def custom_parent(username, channel_id, token, config, command, cooldown, patron_cooldown):
	while True:
		while not data[channel_id] or not data[username]:
			pass

		data[channel_id] = False

		start = time()

		try:
			custom(username, channel_id, token, config, command)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `{command}` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		if config["cooldowns"]["patron"]:
			cooldown = patron_cooldown - (end - start)
		else:
			cooldown = cooldown - (end - start)

		if cooldown > 0:
			sleep(cooldown)