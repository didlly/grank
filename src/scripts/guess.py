from utils.logger import log
from random import randint
from time import time, sleep
from sys import exc_info
from utils.shared import data

def guess(Client) -> None:
	Client.send_message("pls guess")

	latest_message = Client.retreive_message("pls guess")

	Client.send_message("10")

	latest_message = Client.retreive_message("10")
	
	if latest_message["content"] == "not this time, `3` attempts left and `2` hints left.":
		Client.send_message("hint")

		latest_message = Client.retreive_message("hint")

		if latest_message["content"] == "Your last number (**10**) was too low\nYou've got `3` attempts left and `1` hint left.":
			Client.send_message("15")
			
			latest_message = Client.retreive_message("15")

			if latest_message["content"] == "not this time, `2` attempts left and `1` hint left.":
				Client.send_message("hint")

				latest_message = Client.retreive_message("hint")

				if latest_message["content"] == "Your last number (**15**) was too low\nYou've got `2` attempts left and `0` hints left.":
					num = randint(16, 20)
	 
					Client.send_message(num)

					latest_message = Client.retreive_message(num)
     
					if latest_message["content"] == "not this time, `1` attempt left and `0` hints left.":
						num = randint(16, 20)

						Client.send_message(num)

						return
				elif latest_message["content"] == "Your last number (**15**) was too high\nYou've got `2` attempts left and `0` hints left.":
					num = randint(11, 14)

					Client.send_message(num)

					latest_message = Client.retreive_message(num)

					if latest_message["content"] == "not this time, `1` attempt left and `0` hints left.":
						num = randint(11, 14)

						Client.send_message(num)

						return
  
		else:
			Client.send_message("5")
			
			latest_message = Client.retreive_message("5")

			if latest_message["content"] == "not this time, `2` attempts left and `1` hint left.":
				Client.send_message("hint")

				latest_message = Client.retreive_message("hint")

				if latest_message["content"] == "Your last number (**5**) was too low\nYou've got `2` attempts left and `0` hints left.":
					num = randint(6, 9)
	 
					Client.send_message(num)

					latest_message = Client.retreive_message(num)


					if latest_message["content"] == "not this time, `1` attempt left and `0` hints left.":
						num = randint(6, 9)

						Client.send_message(num)

						return
				elif latest_message["content"] == "Your last number (**5**) was too high\nYou've got `2` attempts left and `0` hints left.":
					num = randint(1, 4)

					Client.send_message(num)

					latest_message = Client.retreive_message(num)

					if latest_message["content"] == "not this time, `1` attempt left and `0` hints left.":
						num = randint(1, 4)

						Client.send_message(num)

						return

def guess_parent(Client) -> None:
	"""One of the 2 guess the number commands - `pls guess`.
 
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
			guess(Client)
		except Exception:
			if Client.config["logging"]["warning"]:
				log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls guess` command: `{exc_info()}`")

		end = time()   
		
		data[Client.channel_id] = True
		
		cooldown = 60 - (end - start)

		if cooldown > 0:
			sleep(cooldown)
		else:
			sleep(1)