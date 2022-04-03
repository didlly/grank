from random import choice

def crime(Client) -> None:
	"""One of the basic 7 currency commands - `pls crime`.
 
	Required item(s): None

	Args:
		Client (class): The Client for the user.

	Returns:
		None
	"""
 
	Client.send_message("pls crime")

	latest_message = Client.retreive_message("pls crime")

	custom_id = None
 
	for option in latest_message["components"][0]["components"]:
		if option["label"] == "tax evasion":
			# Gives Badosz's card
			custom_id = option["custom_id"]
			break
  
	Client.interact_button("pls crime", choice(latest_message["components"][0]["components"])["custom_id"] if custom_id is None else custom_id, latest_message)