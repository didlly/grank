from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def custom(Client, command):
	Client.send_message(command)

def custom_parent(Client, command, cooldown, patron_cooldown):
	while True:
		while not data[Client.channel_id] or not data[Client.username]:
			pass

		data[Client.channel_id] = False

		start = time()

		try:
			custom(Client, command)
		except Exception:
			log(Client.username, "WARNING", f"An unexpected error occured during the running of the `{command}` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		if Client.config["cooldowns"]["patron"]:
			cooldown = patron_cooldown - (end - start)
		else:
			cooldown = cooldown - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)