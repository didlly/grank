def dig(Client):
	"""One of the basic 7 currency commands - `pls dig`.
 
	Required item(s): shovel

	Args:
		Client (class): The Client for the user.

	Returns:
		None
	"""
 
	Client.send_message("pls dig")

	latest_message = Client.retreive_message("pls dig")

	if latest_message["content"] == "You don't have a shovel, you need to go buy one. I'd hate to let you dig with your bare hands.":
		if Client.config["logging"]["debug"]:
			Client.log("DEBUG", "User does not have item `shovel`. Buying shovel now.")

		if Client.config["auto buy"] and Client.config["auto buy"]["shovel"]:
			from scripts.buy import buy
			buy(Client, "shovel")
			return
		elif Client.config["logging"]["warning"]:
			Client.log(
				"WARNING",
				f"A shovel is required for the command `pls dig`. However, since {'auto buy is off for shovels,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
			)
			return