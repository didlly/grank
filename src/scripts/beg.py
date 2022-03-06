from discord.message import send_message
from utils.logger import log
from time import time, sleep
from sys import exc_info
from utils.shared import data

def beg(username, channel_id, token, config):
	send_message(channel_id, token, config, username, "pls beg")

def beg_parent(username, channel_id, token, config):
    sleep(40)
    
	while True:
		while not data[channel_id]:
			pass

		data[channel_id] = False

		start = time()

		try:
			beg(username, channel_id, token, config)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls beg` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		if config["cooldowns"]["patron"]:
			cooldown = 25 - (end - start)
		else:
			cooldown = 45 - (end - start)

		if cooldown > 0:
			sleep(cooldown)