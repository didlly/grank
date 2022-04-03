from requests import post

token = "mfa.8OYKYvnEmd5TOH0ix4bhC9BbB7zhiolOR92kgw35cnie-Dud2piyZG8pZ02oEX2zaxP9WTeWu5R2y9-5sbXT"

data = {
    "type": 2,
    "application_id": 270904126974590976,
    "guild_id": 931581907462934569,
    "channel_id": 931581907941064747,
    "session_id": "5b9c47abfad42e7a7f018716aeee29b6",
    "data": {
        "version": 824708709178671145,
        "id": 824708709178671144,
        "name": "roast",
        "type": 1,
    }
}


req = post("https://discord.com/api/v9/interactions", headers={"authorization": token}, json=data)

print(f"{req.status_code}\n{req.content.decode()}")