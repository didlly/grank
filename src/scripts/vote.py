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

    # Send an authorize request for Discord Bot List to the Discord API
    req = request(
        "https://discord.com/api/v10/oauth2/authorize?client_id=477949690848083968&response_type=code&scope=identify",
        headers={"authorization": Client.token},
        json={"authorize": True, "permissions": 0},
        method="POST",
    )

    # Get the code from the response
    code = req.content["location"].split("code=")[-1]

    # Request the token for the account on Discord Bot List
    req = request(f"https://discordbotlist.com/api/v1/oauth?code={code}")

    # If captcha is detected...
    if "captcha" in req.content:
        Client.log(
            "WARNING",
            "Failed to vote for Dank Memer on Discord Bot List due to captcha.",
        )
        # ...return False since currently there is no bypass for captcha
        return False

    # Get the Discord Bot List token
    dbl_token = req.content["token"]

    # Send a request to upvote Dank Memer on Discord Bot List
    req = request(
        "https://discordbotlist.com/api/v1/bots/270904126974590976/upvote",
        headers={"authorization": dbl_token},
        method="POST",
    )

    # If the request completed successfully...
    if req.content["success"]:
        Client.log("DEBUG", "Succesfully voted for Dank Memer on Discord Bot List")

        # ...return True
        return True
    # Else...
    else:
        # ...if the account has alreadty voted for Dank Memer in the past 24 hours...
        if req.content["message"] == "User has already voted.":
            # ...tell the user a ratelimit response was received
            Client.log(
                "WARNING",
                "Already voted for Dank Memer on Discord Bot List in the past 24 hours.",
            )
        # Else
        else:
            # ...tell the user an unknown error occured
            Client.log(
                "WARNING",
                f"Failed to vote for Dank Memer on Discord Bot List. Status code: {req.stauts_code}. Content: `{req.content}`.",
            )
        return False
