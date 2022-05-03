from json import loads

from requests import get, post


def vote(Client) -> None:
    json = {"authorize": True, "permissions": 0}

    req = post(
        "https://discord.com/api/v10/oauth2/authorize?client_id=477949690848083968&response_type=code&scope=identify",
        headers={"authorization": Client.token},
        json=json,
    )

    code = loads(req.content.decode())["location"].split("code=")[-1]

    req = get(f"https://discordbotlist.com/api/v1/oauth?code={code}")

    if "captcha" in req.content.decode():
        Client.log(
            "WARNING",
            "Failed to vote for Dank Memer on Discord Bot List due to captcha.",
        )
        return False

    dbl_token = loads(req.content.decode())["token"]

    req = loads(
        post(
            "https://discordbotlist.com/api/v1/bots/270904126974590976/upvote",
            headers={"authorization": dbl_token},
        ).content.decode()
    )

    if req["success"]:
        if Client.Repository.config["logging"]["debug"]:
            Client.log("DEBUG", "Succesfully voted for Dank Memer on Discord Bot List")
    else:
        if req["message"] == "User has already voted.":
            if Client.Repository.config["logging"]["warning"]:
                Client.log(
                    "WARNING",
                    "Already voted for Dank Memer on Discord Bot List in the past 24 hours.",
                )
        elif Client.Repository.config["logging"]["warning"]:
            Client.log("WARNING", "Failed to vote for Dank Memer on Discord Bot List.")
        return
