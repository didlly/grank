from requests import post
from utils import shared
from utils.logger import log

def interact_dropdown(channel_id, token, config, username, command, custom_id, option_id, latest_message, session_id):
	data = {
		"application_id": 270904126974590976,
		"channel_id": channel_id,
		"type": 3,
		"data": {
			"component_type": 3,
			"custom_id": custom_id,
	"type": 3,
	"values": [option_id]
		},
		"guild_id": latest_message["message_reference"]["guild_id"] if "message_reference" in latest_message.keys() else shared.data[f"{channel_id}_guild"],
		"message_flags": 0,
		"message_id": latest_message["id"],
		"session_id": session_id
	}

	request = post("https://discord.com/api/v10/interactions", headers={"authorization": token}, json=data)

	if request.status_code in [200, 204]:
		if config["logging"]["debug"]:
			log(username, "DEBUG", f"Successfully interacted with dropdown on Dank Memer's response to command `{command}`.")
		return True
	else:
		if config["logging"]["warning"]:
			log(username, "WARNING", f"Failed to interact with dropdown on Dank Memer's response to command `{command}`. Status code: {request.status_code} (expected 200 or 204).")
		return False
