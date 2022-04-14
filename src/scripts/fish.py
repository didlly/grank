def fish(Client) -> None:
	"""One of the basic 7 currency commands - `pls fish`.
 
	Required item(s): Fishing pole

	Args:
		Client (class): The Client for the user.

	Returns:
		None
	"""
 
	Client.send_message("pls fish")

	latest_message = Client.retreive_message("pls fish")

	if "Catch the fish" in latest_message["content"]:
		if Client.config["logging"]["debug"]:
			Client.log("DEBUG", "Detected catch the fish game.")
		level = latest_message["content"].split("\n")[1].replace(latest_message["content"].split("\n")[1].strip(), "").count("       ")
		Client.interact_button("pls fish", latest_message["components"][0]["components"][level]["custom_id"], latest_message)

	if latest_message["content"] == "You don't have a fishing pole, you need to go buy one. You're not good enough to catch them with your hands.":
		if Client.config["logging"]["debug"]:
			Client.log("DEBUG", "User does not have item `fishing pole`. Buying fishing pole now.")

		if Client.config["auto buy"] and Client.config["auto buy"]["fishing pole"]:
			from scripts.buy import buy
			buy(Client, "fishing pole")
			return
		elif Client.config["logging"]["warning"]:
			Client.log(
				"WARNING",
				f"A fishing pole is required for the command `pls fish`. However, since {'auto buy is off for fishing poles,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
			)
			return