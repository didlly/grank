from websocket import WebSocket
from json import loads, dumps

def gateway(token):
	"""Gets the first `session_id` received from Discord during the websocket connection process.
 
	Args:
		token (str): The token of the account the `session_id` should be found for.

	Returns:
		session_id (str): The `session_id` for the account specified by the token passed to this function.
	"""
	
	ws = WebSocket()
	ws.connect("wss://gateway.discord.gg/?v=10&encoding=json")
	loads(ws.recv())

	ws.send(dumps({
		"op": 2,
		"d": {
			"token": token,
			"properties": {
				"$os": "windows",
				"$browser": "chrome",
				"$device": "pc"
			}
		}
	}))
	
	return loads(ws.recv())["d"]["sessions"][0]["session_id"]