from random import choice, randint

def stream(Client) -> None:
	"""A streaming command - `pls stream`.
 
	Required item(s): keyboard, mouse

	Args:
		Client (class): The Client for the user.

	Returns:
		None
	"""
 
	while True:
		Client.send_message("pls stream")

		latest_message = Client.retreive_message("pls stream")

		if "title" not in latest_message["embeds"][0].keys():
			break

		if "Keyboard" in latest_message["embeds"][0]["description"]:
			if Client.config["logging"]["debug"]:
				Client.log("DEBUG", "User does not have item `keyboard`. Buying keyboard now.")

			if Client.config["auto buy"] and Client.config["auto buy"]["keyboard"]:
				from scripts.buy import buy
				bought = buy(Client, "keyboard")
				if not bought:
					return
			elif Client.config["logging"]["warning"]:
				Client.log(
					"WARNING",
					f"A keyboard is required for the command `pls stream`. However, since {'autobuy is off for keyboards,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
				)

		if "Mouse" in latest_message["embeds"][0]["description"]:
			if Client.config["logging"]["debug"]:
				Client.log("DEBUG", "User does not have item `mouse`. Buying mouse now.")

			if Client.config["auto buy"] and Client.config["auto buy"]["mouse"]:
				bought = buy(Client, "mouse")
				if not bought:
					return
			elif Client.config["logging"]["warning"]:
				Client.log(
					"WARNING",
					f"A mouse is required for the command `pls stream`. However, since {'autobuy is off for mouses,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
				)
	if len(latest_message["components"][0]["components"]) == 3:
		Client.interact_button("pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message)

		latest_message = Client.retreive_message("pls stream")

		Client.interact_dropdown("pls stream", latest_message["components"][0]["components"][0]["custom_id"], choice(latest_message["components"][0]["components"][0]["options"])["value"], latest_message)

		Client.interact_button("pls stream", latest_message["components"][-1]["components"][0]["custom_id"], latest_message)

	latest_message = Client.retreive_message("pls stream")

	if int(latest_message["embeds"][0]["fields"][5]["value"].replace("`", "")) > 0 and Client.config["stream"]["ads"]:
		Client.interact_button("pls stream", latest_message["components"][0]["components"][0]["custom_id"], latest_message)
	else:
		button = randint(1, 2) if Client.config["stream"]["chat"] and Client.config["stream"]["donations"] else 1 if Client.config["stream"]["chat"] else 2 if Client.config["stream"]["donations"] else None

		if button is None:
			return

		Client.interact_button("pls stream", latest_message["components"][0]["components"][button]["custom_id"], latest_message)

	Client.interact_button("pls stream", latest_message["components"][-1]["components"][-1]["custom_id"], latest_message)