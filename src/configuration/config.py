from utils.yaml import load
from utils.logger import log
from discord.gateway import gateway
from requests import get
from json import loads

def load_config(cwd):
	config = load(f"{cwd}/config.yml")

	options = ["['commands']", "['commands']['crime']", "['commands']['daily']", "['commands']['beg']", "['commands']['fish']", "['commands']['hunt']", "['commands']['dig']", "['commands']['search']", "['commands']['highlow']", "['commands']['postmeme']", "['commands']['trivia']", "['auto_buy']", "['auto_buy']['enabled']", "['auto_buy']['laptop']", "['auto_buy']['shovel']", "['auto_buy']['fishing pole']", "['auto_buy']['hunting rifle']", "['auto_trade']", "['auto_trade']['enabled']", "['auto_trade']['trader_token']", "['typing_indicator']", "['typing_indicator']['enabled']", "['typing_indicator']['minimum']", "['typing_indicator']['maximum']", "['cooldowns']", "['cooldowns']['patron']", "['cooldowns']['timeout']", "['logging']['debug']", "['logging']['warning']"]

	for option in options:
		try:
			exec(f"_ = config{option}")
		except KeyError:
			log(None, "ERROR", f"Unable to find configuration option for `{option}`. Make sure it is present.")


	if config["auto_trade"]["enabled"]:
		request = get("https://discord.com/api/v10/users/@me", headers={"authorization": config["auto_trade"]["trader_token"]})

		if request.status_code != 200:
			log(None, "ERROR", f"Invalid trader token set. Please double-check you entered a valid token in `config.yml`.")

		request = loads(request.text)

		config["auto_trade"]["trader"] = {}
		config["auto_trade"]["trader"]["username"] = f"{request['username']}#{request['discriminator']}"
		config["auto_trade"]["trader"]["user_id"] = request["id"]
		config["auto_trade"]["trader"]["session_id"] = gateway(config["auto_trade"]["trader_token"])
		
	return config