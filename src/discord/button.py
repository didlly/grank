from requests import post
from utils.logger import log

def interact_button(channel_id, token, config, username, command, custom_id, latest_message, session_id):
    data = {
        "application_id": 270904126974590976,
        "channel_id": channel_id,
        "type": 3,
        "data": {
            "component_type": 2,
            "custom_id": custom_id
        },
        "guild_id": latest_message["message_reference"]["guild_id"],
        "message_flags": 0,
        "message_id": latest_message["id"],
        "session_id": session_id
    }
    
    request = post(f"https://discord.com/api/v10/interactions", headers={"authorization": token}, json=data)
    
    if request.status_code== 200 or request.status_code == 204:
        if config["logging"]["debug"]:
             log(username, "DEBUG", f"Successfully interacted with button on Dank Memer's response to command `{command}`.")
        return True
    else:
        if config["logging"]["warning"]:
            log(username, "WARNING", f"Failed to interact with button on Dank Memer's response to command `{command}`. Status code: {request.getcode()} (expected 200 or 204).")
        return False