from discord.message import send_message, retreive_message
from utils.logger import log
from random import randint
from time import time, sleep
from sys import exc_info
from utils.shared import data

def guess(username, channel_id, token, config, user_id, session_id):
	send_message(channel_id, token, config, username, "pls guess")

	latest_message = retreive_message(channel_id, token, config, username, "pls guess", user_id, session_id)

	if latest_message is None:
		return

	send_message(channel_id, token, config, username, "10")

	latest_message = retreive_message(channel_id, token, config, username, "10", user_id, session_id)

	if latest_message is None:
		return
	
	if latest_message["content"] == "not this time, `3` attempts left and `2` hints left.":
		send_message(channel_id, token, config, username, "hint")

		latest_message = retreive_message(channel_id, token, config, username, "hint", user_id, session_id)

		if latest_message is None:
			return

		if latest_message["content"] == "Your last number (**10**) was too low\nYou've got `3` attempts left and `1` hint left.":
			send_message(channel_id, token, config, username, "15")
			
			latest_message = retreive_message(channel_id, token, config, username, "15", user_id, session_id)

			if latest_message is None:
				return

			if latest_message["content"] == "not this time, `2` attempts left and `1` hint left.":
				send_message(channel_id, token, config, username, "hint")

				latest_message = retreive_message(channel_id, token, config, username, "hint", user_id, session_id)

				if latest_message is None:
					return

				if latest_message["content"] == "Your last number (**15**) was too low\nYou've got `2` attempts left and `0` hints left.":
					num = randint(16, 20)
	 
					send_message(channel_id, token, config, username, num)

					latest_message = retreive_message(channel_id, token, config, username, num, user_id, session_id)

					if latest_message is None:
						return

					if latest_message["content"] == "not this time, `1` attempt left and `0` hints left.":
						num = randint(16, 20)

						send_message(channel_id, token, config, username, num)

						return
				elif latest_message["content"] == "Your last number (**15**) was too high\nYou've got `2` attempts left and `0` hints left.":
					num = randint(11, 14)

					send_message(channel_id, token, config, username, num)

					latest_message = retreive_message(channel_id, token, config, username, num, user_id, session_id)

					if latest_message is None:
						return

					if latest_message["content"] == "not this time, `1` attempt left and `0` hints left.":
						num = randint(11, 14)

						send_message(channel_id, token, config, username, num)

						return
  
		elif latest_message["content"] == "Your last number (**10**) was too high\nYou've got `3` attempts left and `1` hint left.":
			send_message(channel_id, token, config, username, "5")
			
			latest_message = retreive_message(channel_id, token, config, username, "5", user_id, session_id)

			if latest_message is None:
				return

			if latest_message["content"] == "not this time, `2` attempts left and `1` hint left.":
				send_message(channel_id, token, config, username, "hint")

				latest_message = retreive_message(channel_id, token, config, username, "hint", user_id, session_id)

				if latest_message is None:
					return

				if latest_message["content"] == "Your last number (**5**) was too low\nYou've got `2` attempts left and `0` hints left.":
					num = randint(6, 9)
	 
					send_message(channel_id, token, config, username, num)

					latest_message = retreive_message(channel_id, token, config, username, num, user_id, session_id)

					if latest_message is None:
						return

					if latest_message["content"] == "not this time, `1` attempt left and `0` hints left.":
						num = randint(6, 9)

						send_message(channel_id, token, config, username, num)

						return
				elif latest_message["content"] == "Your last number (**5**) was too high\nYou've got `2` attempts left and `0` hints left.":
					num = randint(1, 4)

					send_message(channel_id, token, config, username, num)

					latest_message = retreive_message(channel_id, token, config, username, num, user_id, session_id)

					if latest_message is None:
						return

					if latest_message["content"] == "not this time, `1` attempt left and `0` hints left.":
						num = randint(1, 4)

						send_message(channel_id, token, config, username, num)

						return

def guess_parent(username, channel_id, token, config, user_id, session_id):
	while True:
		while not data[channel_id] or not data[username]:
			pass

		data[channel_id] = False

		start = time()

		try:
			guess(username, channel_id, token, config, user_id, session_id)
		except Exception:
			log(username, "WARNING", f"An unexpected error occured during the running of the `pls guess` command: `{exc_info()}`")

		end = time()   
		
		data[channel_id] = True
		
		cooldown = 60 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
