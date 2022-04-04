from json import loads

from discord.gateway import gateway
from requests import get
from utils.logger import log
from utils.yaml import load


def load_config(cwd: str) -> dict:
	"""Loads the configuration file (`config.yml`) and makes sure the required configuration values are present.

	Args:
		cwd (str): The current working directory.

	Returns:
		config (dict): The dictionary version of the yaml configuration file.
	"""
	
	config = load(f"{cwd}config.yml")

	options = ["['commands']", "['commands']['crime']", "['commands']['daily']", "['commands']['beg']", "['commands']['fish']", "['commands']['guess']", "['commands']['hunt']", "['commands']['dig']", "['commands']['search']", "['commands']['highlow']", "['commands']['postmeme']", "['commands']['trivia']", "['commands']['vote']", "['lottery']", "['lottery']['enabled']", "['lottery']['cooldown']", "['stream']", "['stream']['ads']", "['stream']['chat']", "['stream']['donations']", "['blackjack']", "['blackjack']['random']", "['blackjack']['enabled']", "['blackjack']['amount']", "['blackjack']['minimum']",  "['blackjack']['maximum']", "['custom commands']", "['custom commands']['enabled']", "['shifts']", "['shifts']['enabled']", "['shifts']['active']", "['shifts']['passive']", "['auto buy']", "['auto buy']['enabled']", "['auto buy']['shovel']", "['auto buy']['fishing pole']", "['auto buy']['hunting rifle']", "['auto buy']['keyboard']", "['auto buy']['mouse']", "['auto trade']", "['auto trade']['enabled']", "['auto trade']['trader token']", "['typing indicator']", "['typing indicator']['enabled']", "['typing indicator']['minimum']", "['typing indicator']['maximum']", "['cooldowns']", "['cooldowns']['patron']", "['cooldowns']['timeout']", "['auto update']", "['auto update']['enabled']", "['auto update']['config']", "['logging']['debug']", "['logging']['warning']"]

	for option in options:
		try:
			exec(f"_ = config{option}")
		except KeyError:
			log(None, "ERROR", f"Unable to find configuration option for `{option}`. Make sure it is present.")


	if config["auto trade"]["enabled"]:
		request = get("https://discord.com/api/v10/users/@me", headers={"authorization": config["auto trade"]["trader token"]})

		if request.status_code != 200:
			log(None, "ERROR", "Invalid trader token set. Please double-check you entered a valid token in `config.yml`.")

		request = loads(request.text)

		config["auto trade"]["trader"] = {}
		config["auto trade"]["trader"]["username"] = f"{request['username']}#{request['discriminator']}"
		config["auto trade"]["trader"]["user_id"] = request["id"]
		config["auto trade"]["trader"]["session_id"] = gateway(config["auto trade"]["trader token"])
		
	return config