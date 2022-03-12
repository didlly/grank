from requests import post, get
from utils.logger import log
from utils.shared import data
from time import sleep
from random import uniform
from json import loads
from datetime import datetime
from discord.button import interact_button

def send_message(channel_id, token, config, username, command):
	if config["typing_indicator"]["enabled"]:
		request = post(f"https://discord.com/api/v9/channels/{channel_id}/typing", headers={"authorization": token})
		sleep(uniform(config["typing_indicator"]["minimum"], config["typing_indicator"]["maximum"]))

	while True:
		request = post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers={"authorization": token}, json={"content": command})

		if request.status_code == 200 or request.status_code == 204:
			if config["logging"]["debug"]:
					log(username, "DEBUG", f"Successfully sent command `{command}`.")
			return True
		else:
			if config["logging"]["warning"]:
				log(username, "WARNING", f"Failed to send command `{command}`. Status code: {request.status_code} (expected 200 or 204).")
			if request.status_code == 429:
				request = loads(request.content)
				log(username, "WARNING", f"Discord is ratelimiting the self-bot. Sleeping for {request['retry_after']} second(s).")
				sleep(request["retry_after"])
				continue
			return False

def retreive_message(channel_id, token, config, username, command, user_id, session_id=None):
	time = datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X")

	while (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - time).total_seconds() < config["cooldowns"]["timeout"]:
		request = get(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers={"authorization": token})
		
		if request.status_code != 200:
			continue
		
		latest_message = loads(request.text)[0]
		
		if latest_message["author"]["id"] == "270904126974590976":
			if "referenced_message" in latest_message.keys():
				if latest_message["referenced_message"]["author"]["id"] == user_id:
					if config["logging"]["debug"]:
						log(username, "DEBUG", f"Got Dank Memer's response to command `{command}`.")
					break
			else:
				if config["logging"]["debug"]:
					log(username, "DEBUG", f"Got Dank Memer's response to command `{command}`.")
				break
		else:
			continue
     
	if latest_message["author"]["id"] != "270904126974590976":
		if config["logging"]["warning"]:
			log(username, "WARNING", f"Timeout exceeded for response from Dank Memer ({config['cooldowns']['timeout']} {'second' if config['cooldowns']['timeout'] == 1 else 'seconds'}). Aborting command.")
		return None

	if len(latest_message["embeds"]) != 0:
		if "title" in latest_message["embeds"][0].keys():
			if latest_message["embeds"][0]["title"] == "You're currently bot banned!" or latest_message["embeds"][0]["title"] == "You're currently blacklisted!":
				log(username, "ERROR", "Exiting self-bot instance since Grank has detected the user has been bot banned / blacklisted.")
	
 
	if "Dodge the Fireball" in latest_message["content"]:
		log(username, "DEBUG", "Detected dodge the fireball game.")
		while True:
			request = get(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers={"authorization": token})
		
			if request.status_code != 200:
				continue
			
			latest_message = loads(request.text)[0]
			
			if latest_message["author"]["id"] == "270904126974590976":
				if "referenced_message" in latest_message.keys():
					if latest_message["referenced_message"]["author"]["id"] == user_id:
						if config["logging"]["debug"]:
							log(username, "DEBUG", f"Got Dank Memer's response to command `{command}`.")
						break
				else:
					if config["logging"]["debug"]:
						log(username, "DEBUG", f"Got Dank Memer's response to command `{command}`.")
					break
			else:
				continue
      
			level = latest_message["content"].split("\n")[1].replace(latest_message["content"].split("\n")[1].strip(), "").count("       ")
   
			if level != 1:	
				continue
      
			interact_button(channel_id, token, config, username, command, latest_message["components"][0]["components"][1]["custom_id"], latest_message, session_id)
	
			break
  
	if "Catch the fish" in latest_message["content"]:
		log(username, "DEBUG", "Detected catch the fish game.")
		level = latest_message["content"].split("\n")[1].replace(latest_message["content"].split("\n")[1].strip(), "").count("       ")
		interact_button(channel_id, token, config, username, command, latest_message["components"][0]["components"][level]["custom_id"], latest_message, session_id)
     
	if config["auto_trade"]["enabled"]:
		for key in config["auto_trade"]:
			if key == "enabled" or key == "trader_token" or not config["auto_trade"][key]:
				continue
			elif key in latest_message["content"].lower():
				send_message(channel_id, token, config, username, f"pls trade 1 {key} {config['auto_trade']['trader']['username']}")

				latest_message = retreive_message(channel_id, token, config, username, f"pls trade 1 {key} {config['auto_trade']['trader']['username']}", user_id)

				if latest_message is None:
					return

				interact_button(channel_id, token, config, username, f"pls trade 1 {key} {config['auto_trade']['trader']['username']}", latest_message["components"][0]["components"][-1]["custom_id"], latest_message, session_id)
			
				sleep(1)

				latest_message = retreive_message(channel_id, config["auto_trade"]["trader_token"], config, config["auto_trade"]["trader"]["username"], f"pls trade 1 {key} {config['auto_trade']['trader']['username']}", config["auto_trade"]["trader"]["user_id"])

				if latest_message is None:
					return

				interact_button(channel_id, config["auto_trade"]["trader_token"], config, username, f"pls trade 1 {key} {config['auto_trade']['trader']['username']}", latest_message["components"][0]["components"][-1]["custom_id"], latest_message, config["auto_trade"]["trader"]["session_id"])
			elif len(latest_message["embeds"]) != 0:
				if key in latest_message["embeds"][0]["description"]:
					send_message(channel_id, token, config, username, f"pls trade 1 {key} {config['auto_trade']['trader']['username']}")

					latest_message = retreive_message(channel_id, token, config, username, f"pls trade 1 {key} {config['auto_trade']['trader']['username']}", user_id)

					if latest_message is None:
						return

					interact_button(channel_id, token, config, username, f"pls trade 1 {key} {config['auto_trade']['trader']['username']}", latest_message["components"][0]["components"][-1]["custom_id"], latest_message, session_id)
				
					sleep(1)

					latest_message = retreive_message(channel_id, config["auto_trade"]["trader_token"], config, config["auto_trade"]["trader"]["username"], f"pls trade 1 {key} {config['auto_trade']['trader']['username']}", config["auto_trade"]["trader"]["user_id"])

					if latest_message is None:
						return

					interact_button(channel_id, config["auto_trade"]["trader_token"], config, username, f"pls trade 1 {key} {config['auto_trade']['trader']['username']}", latest_message["components"][0]["components"][-1]["custom_id"], latest_message, config["auto_trade"]["trader"]["session_id"])			
	return latest_message
