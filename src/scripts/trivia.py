from random import choice
from utils.logger import log

def trivia(Client) -> None:
	"""A trivia command - `pls trivia`.
 
	Required item(s): None

	Args:
		Client (class): The Client for the user.

	Returns:
		None
	"""
	
	Client.send_message("pls trivia")

	latest_message = Client.retreive_message("pls trivia")

	try:
		answer = Client.database["trivia"][latest_message["embeds"][0]["description"].split("\n")[0].replace("*", "").replace('"', "&quot;")]
	except KeyError:
		answer = None
		log(None, "WARNING", f"Unknown trivia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Answers: `{latest_message['components'][0]['components']}`. Please create an issue on Grank highlighting this.")

	custom_id = None

	for index, possible_answer in enumerate(latest_message["components"][0]["components"]):
		if possible_answer["label"] == answer:
			custom_id = latest_message["components"][0]["components"][index]["custom_id"]

	if custom_id is None:
		log(None, "WARNING", f"Unknown answer to trivia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Answers: `{latest_message['components'][0]['components']}`. Please create an issue on Grank highlighting this.")
		custom_id = choice(latest_message["components"][0]["components"])["custom_id"]

	Client.interact_button("pls trivia", custom_id, latest_message)