from websocket import WebSocket
from json import loads, dumps

def gateway(token):
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