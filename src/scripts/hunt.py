from utils.logger import log

def hunt(Client) -> None:
	"""One of the basic 7 currency commands - `pls hunt`.
 
	Required item(s): hunting rifle

	Args:
		Client (class): The Client for the user.

	Returns:
		None
	"""
 
	Client.send_message("pls hunt")

	latest_message = Client.retreive_message("pls hunt")

	if latest_message["content"] == "You don't have a hunting rifle, you need to go buy one. You're not good enough to shoot animals with your bare hands... I hope.":
		if Client.config["logging"]["debug"]:
			log(Client.username, "DEBUG", "User does not have item `hunting rifle`. Buying hunting rifle now.")

		if Client.config["auto buy"] and Client.config["auto buy"]["hunting rifle"]:
			from scripts.buy import buy
			buy(Client, "hunting rifle")
			return
		elif Client.config["logging"]["warning"]:
			log(
				Client.username,
				"WARNING",
				f"A hunting rifle is required for the command `pls fish`. However, since {'auto buy is off for hunting rifles,' if Client.config['auto buy']['parent'] else 'auto buy is off for all items,'} the program will not buy one. Aborting command.",
			)
			return