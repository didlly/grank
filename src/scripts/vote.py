from instance.Client import Instance
from utils.Requests import request


def vote(Client: Instance) -> bool:
    """
    The vote function is used to vote for Dank Memer on Discord Bot List.

    Args:
        Client (Instance): The Discord client

    Returns:
        bool: Indicates whether the command ran successfully or not
    """

    req = request(
        "https://discord.com/api/v10/oauth2/authorize?client_id=477949690848083968&response_type=code&scope=identify",
        headers={"authorization": Client.token},
        json={"authorize": True, "permissions": 0},
        method="POST",
    )

    code = req.content["location"].split("code=")[-1]

    req = request(f"https://discordbotlist.com/api/v1/oauth?code={code}")

    if "captcha" in req.content:
        Client.log(
            "WARNING",
            "Failed to vote for Dank Memer on Discord Bot List due to captcha.",
        )
        return False

    dbl_token = req.content["token"]

    req = request(
        "https://discordbotlist.com/api/v1/bots/270904126974590976/upvote",
        headers={"authorization": dbl_token},
        method="POST",
    )

    if req.content["success"]:
        Client.log("DEBUG", "Succesfully voted for Dank Memer on Discord Bot List")

        return True
    else:
        if req.content["message"] == "User has already voted.":
            Client.log(
                "WARNING",
                "Already voted for Dank Memer on Discord Bot List in the past 24 hours.",
            )
        else:
            Client.log(
                "WARNING",
                f"Failed to vote for Dank Memer on Discord Bot List. Status code: {req.stauts_code}. Content: `{req.content}`.",
            )
        return False
