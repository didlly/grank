"""
NOTE: This is an edited version of `thttp` (https://github.com/sesh/thttp).
"""

from base64 import b64encode
from collections import namedtuple
from contextlib import suppress
from gzip import decompress
from http.cookiejar import CookieJar
from json import dumps, loads
from json.decoder import JSONDecodeError
from ssl import CERT_NONE, create_default_context
from sys import exc_info
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import (
    HTTPCookieProcessor,
    HTTPRedirectHandler,
    HTTPSHandler,
    Request,
    build_opener,
)

from utils.Logger import log

Response = namedtuple(
    "Response", "request content json status_code url headers cookiejar"
)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(
    url: str,
    params: dict = {},
    json: Optional[dict] = None,
    data: Optional[str] = None,
    headers: dict = {},
    method: str = "GET",
    verify: bool = False,
    redirect: bool = True,
    cookiejar: Optional[CookieJar] = None,
    basic_auth: Optional[str] = None,
    timeout: int = 5,
):
    """
    The request function is used to make a request to the specified URL.

    Args:
        url (str): The url of the page the request will be sent to
        params (dict) = {}: The query parameters
        json (Optional[dict]) = None: The json payload (or None if there is none)
        data (Optional[str]) = None: The string payload (or None if there is none)
        headers (dict) = {}: The headers for the request
        method (str) = "GET": The request method
        verify (bool) = False: Whether or not to ignore ssl errors
        redirect (bool) = True: Whether or not to follow redirects
        cookiejar (Optional[CookieJar]) = None: Cookie container
        basic_auth (Optional[str]) = None: A username and password to be sent with the request (or None if there is none)
        timeout (int) = 5: A timeout for the request

    Returns:
        A tuple of status code, response content and the final url
    """

    method = method.upper()

    headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"

    headers = {k.lower(): v for k, v in headers.items()}

    if params:
        url += f"?{urlencode(params)}"

    if json and data:
        raise Exception("Cannot provide both json and data parameters")

    if method not in ["POST", "PATCH", "PUT"] and (json or data):
        raise Exception(
            "Request method must POST, PATCH or PUT if json or data is provided"
        )

    if json:
        headers["content-type"] = "application/json"

        data = dumps(json).encode("utf-8")
    elif data:
        data = urlencode(data).encode()

    if basic_auth and len(basic_auth) == 2 and "authorization" not in headers:
        username, password = basic_auth

        headers[
            "authorization"
        ] = f'Basic {b64encode(f"{username}:{password}".encode()).decode("ascii")}'

    if not cookiejar:
        cookiejar = CookieJar()

    ctx = create_default_context()

    if not verify:
        ctx.check_hostname = False

        ctx.verify_mode = CERT_NONE

    handlers = []

    handlers.append(HTTPSHandler(context=ctx))

    handlers.append(HTTPCookieProcessor(cookiejar=cookiejar))

    if not redirect:
        handlers.append(NoRedirect())

    opener = build_opener(*handlers)

    req = Request(url, data=data, headers=headers, method=method)

    try:
        with opener.open(req, timeout=timeout) as resp:
            status_code, content, resp_url = (
                resp.getcode(),
                resp.read().decode(),
                resp.geturl(),
            )

            headers = {k.lower(): v for k, v in list(resp.info().items())}

            if "gzip" in headers.get("content-encoding", ""):
                content = decompress(content).decode()

            json = (
                loads(content)
                if "application/json" in headers.get("content-type", "").lower()
                and content
                else None
            )
    except HTTPError as e:
        status_code, content, resp_url = (e.code, e.read().decode(), e.geturl())

        headers = {k.lower(): v for k, v in list(e.headers.items())}

        if "gzip" in headers.get("content-encoding", ""):
            content = decompress(content).decode()

        json = (
            loads(content)
            if "application/json" in headers.get("content-type", "").lower() and content
            else None
        )
    except URLError:
        log(
            None,
            "WARNING",
            f"Connecting to {url} failed - `{exc_info()}`.",
        )
        return False

    with suppress(JSONDecodeError):
        content = loads(content)

    return Response(req, content, json, status_code, resp_url, headers, cookiejar)
