from typing import Optional

from utils.Converter import DictToClass
from utils.Requests import request


def user_info(token: str, user_id: Optional[int] = None) -> Optional[dict]:
    req = request(
        "https://discord.com/api/v10/users/@me"
        if user_id is None
        else f"https://discord.com/api/v10/users/{user_id}",
        headers={"authorization": token},
    )

    if not 199 < req.status_code < 300:
        return None

    req = DictToClass(req.content)
    req.token = token
    return req
