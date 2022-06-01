from typing import Optional

from utils.Converter import DictToClass
from utils.Requests import request


def user_info(token: str, user_id: Optional[int] = None) -> Optional[DictToClass]:
    """
    The user_info function returns a dictionary containing the user's Discord ID, username, discriminator (the 4-digit number after their username), avatar hash (a unique string of numbers and letters that identifies an image file on Discord), and email. If the user_info function is passed a token for an invalid or expired authorization code, it will return None.

    Args:
        token (str): The token that should be used when collecting the user's info.
        user_id (Optional[int]) = None: Tells the function whether to use @me instead of a user id

    Returns:
        req (Optional[DictToClass]): A class with the user's information
    """

    # Send a request to the Discord API. If the user_id is None, then we are getting information about the account linked to the token, so we do a @me request. Else, we do a request to the user's page
    req = request(
        "https://discord.com/api/v10/users/@me"
        if user_id is None
        else f"https://discord.com/api/v10/users/{user_id}",
        headers={"authorization": token},
    )

    # If the request status code is an error code...
    if not 199 < req.status_code < 300:
        # ...return None
        return None

    # Convert the account data to a class
    req = DictToClass(req.content)

    # Add the token attribute
    req.token = token

    # Return the class
    return req
