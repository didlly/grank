from random import randint
from utils.logger import log

def blackjack(Client) -> None:
	"""One of the 3 gamble commands - `pls blackjack`.
 
	Required item(s): None

	Args:
		Client (class): The Client for the user.

	Returns:
		None
	"""
 
	amount = Client.config['blackjack']['amount'] if not Client.config['blackjack']['random'] else randint(Client.config['blackjack']['minimum'], Client.config['blackjack']['maximum'])

	Client.send_message(f"pls bj {amount}")

	while True:
		latest_message = Client.retreive_message(f"pls bj {amount}")

		if "coins, dont try and lie to me hoe." in latest_message["content"] or "You have no coins in your wallet to gamble with lol." in latest_message["content"]:
			log(Client.username, "WARNING", f"Insufficient funds to run the command `pls bj {amount}`. Aborting command.")
			return

		if "description" in latest_message["embeds"][0].keys():
			if "You lost" in latest_message["embeds"][0]["description"]:
				return

		total = int("".join(filter(str.isdigit, latest_message["embeds"][0]["fields"][0]["value"].split("\n")[-1])))

		if total < 18:
			Client.interact_button(f"pls bj {amount}", latest_message["components"][0]["components"][0]["custom_id"], latest_message)
		else:
			Client.interact_button(f"pls bj {amount}", latest_message["components"][0]["components"][1]["custom_id"], latest_message)
			break