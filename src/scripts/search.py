from random import choice

def search(Client) -> None:
	"""One of the basic 7 currency commands - `pls search`.
 
	Required item(s): None

	Args:
		Client (class): The Client for the user.

	Returns:
		None
	"""
 
	Client.send_message("pls search")

	latest_message = Client.retreive_message("pls search")

	custom_id = None
 
	for option in latest_message["components"][0]["components"]:
		if option["label"] == "street":
			# Gives `Golden Phalic Object` / `Rare Pepe`.
			custom_id = option["custom_id"]
			break
		elif option["label"] == "dresser":
			# Gives `Bank note` / `Normie Box` / `Apple`.
			custom_id = option["custom_id"]
			break
		elif option["label"] == "mailbox":
			# Gives `Normie Box` / `Bank note`.
			custom_id = option["custom_id"]
			break
		elif option["label"] == "bushes":
			# Gives ``Normie Box`.
			custom_id = option["custom_id"]
			break
		elif option["label"] == "bank":
			# Gives `Bank note`.
			custom_id = option["custom_id"]
			break
		elif option["label"] == "laundromat":
			# Gives `Tidepod`.
			custom_id = option["custom_id"]
			break
		elif option["label"] == "hospital":
			# Gives `Life Saver` / `Apple`.
			custom_id = option["custom_id"]
			break
		elif option["label"] == "laundromat":
			# Gives `Tidepod`.
			custom_id = option["custom_id"]
			break

	Client.interact_button("pls search", choice(latest_message["components"][0]["components"])["custom_id"] if custom_id is None else custom_id, latest_message)