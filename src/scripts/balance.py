from discord.message import send_message, retreive_message

def balance(username, channel_id, token, config, user_id):
    request = send_message(channel_id, token, config, username, "pls bal")

    if request is None:
        return None
      
    return retreive_message(channel_id, token, config, username, "pls bal", user_id)