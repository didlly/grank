from requests import get
from json import loads
from discord.message import send_message, retreive_message
from utils.shared import data

def guild_id(username, channel_id, token, config, user_id, session_id):
	response = loads(get(f" https://discord.com/api/v10/channels/{channel_id}/messages?limit=50", headers={"authorization": token}).content.decode())
	
	found = False
  
	if len(response) != 0:
		for latest_message in response:
			if "message_reference" in latest_message.keys():
				found = True
				data[f"{channel_id}_guild"] = latest_message["message_reference"]["guild_id"]
				break
	elif not found:
		send_message(channel_id, token, config, username, "pls beg")
	
		while True:
			latest_message = retreive_message(channel_id, token, config, username, "pls beg", user_id, session_id)

			if latest_message is not None:
				break

		data[f"{channel_id}_guild"] = latest_message["message_reference"]["guild_id"]