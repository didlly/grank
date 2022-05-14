from typing import Optional
from requests import get
from json import loads
from utils.Converter import DictToClass


def user_info(token: str, user_id: Optional[int] = None) -> Optional[dict]:
    req = get(
        "https://discord.com/api/v10/users/@me"
        if user_id is None
        else f"https://discord.com/api/v10/users/{user_id}",
        headers={"authorization": token},
    )
    
    if not req.ok:
        return None

    req = DictToClass(loads(req.content))
    req.token = token
    return req
