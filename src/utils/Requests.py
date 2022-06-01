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

    # Make the method uppercase
    method = method.upper()

    # Add a legitimate `User-Agent` header so Discord doesn't block us
    headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"

    # Make all headers lowercase
    headers = {k.lower(): v for k, v in headers.items()}

    # If there are query parameters...
    if params:
        # ..add them onto the end of the URL
        url += f"?{urlencode(params)}"

    # If a json and data payload have both been provided...
    if json and data:
        # ...raise an Exception
        raise Exception("Cannot provide both json and data parameters")

    # If json / data is provided and the method isn't `POST` or `PATCH` or `PUT`...
    if method not in ["POST", "PATCH", "PUT"] and (json or data):
        # ...raise an Exception
        raise Exception(
            "Request method must POST, PATCH or PUT if json or data is provided"
        )

    # If a json payload was supplied...
    if json:
        # ...add the json header to the request
        headers["content-type"] = "application/json"

        # Convert the json into a string and encode it in `utf-8`
        data = dumps(json).encode("utf-8")
    # Else if a data payload was supplied...
    elif data:
        # ...encode the data
        data = urlencode(data).encode()

    # If basic_auth is set to True and a username and password have been supplied...
    if basic_auth and len(basic_auth) == 2 and "authorization" not in headers:
        # ...unpack the username and password from the variable basic_auth
        username, password = basic_auth

        # Add the username and password to the headers
        headers[
            "authorization"
        ] = f'Basic {b64encode(f"{username}:{password}".encode()).decode("ascii")}'

    # If a cookiejar wasn't supplied...
    if not cookiejar:
        # ...create a new one
        cookiejar = CookieJar()

    # Create a SSLContext object and assign it to the variable ctx
    ctx = create_default_context()

    # If verify is set to False...
    if not verify:
        # Disable checking the hostname on request send
        ctx.check_hostname = False

        # Disable verify the request with a certificate
        ctx.verify_mode = CERT_NONE

    # Initialize handlers to an empty list
    handlers = []

    # Append a HTTPSHandler class to handlers
    handlers.append(HTTPSHandler(context=ctx))

    # Append a HTTPCookiePorcessor class to handlers
    handlers.append(HTTPCookieProcessor(cookiejar=cookiejar))

    # If redirecting is disabled...
    if not redirect:
        # ...append a NoRedirect class to handlers
        handlers.append(NoRedirect())

    # Create an opener object
    opener = build_opener(*handlers)

    # Initialize the request
    req = Request(url, data=data, headers=headers, method=method)

    try:
        # Open the request...
        with opener.open(req, timeout=timeout) as resp:
            # ...unpack the response status code, content etc.
            status_code, content, resp_url = (
                resp.getcode(),
                resp.read().decode(),
                resp.geturl(),
            )

            # Get the response headers
            headers = {k.lower(): v for k, v in list(resp.info().items())}

            # If gzip is in the request headers...
            if "gzip" in headers.get("content-encoding", ""):
                # ...decompress the content using gzip
                content = decompress(content).decode()

            # Parse the json response if there is one
            json = (
                loads(content)
                if "application/json" in headers.get("content-type", "").lower()
                and content
                else None
            )
    # ...except HTTPError...
    except HTTPError as e:
        # ...unpack the response status code, content etc.
        status_code, content, resp_url = (e.code, e.read().decode(), e.geturl())

        # Get the response headers
        headers = {k.lower(): v for k, v in list(e.headers.items())}

        # If gzip is in the request headers...
        if "gzip" in headers.get("content-encoding", ""):
            # ...decompress the content using gzip
            content = decompress(content).decode()

        # Parse the json response if there is one
        json = (
            loads(content)
            if "application/json" in headers.get("content-type", "").lower() and content
            else None
        )
    # ...except URLError (no WiFi connection)...
    except URLError:
        # ...tell the user of ;-)
        log(
            None,
            "ERROR",
            "In case you didn't realise, Sherlock, you need an internet connection to run Grank ;-).",
        )

    # ...suppress a JSONDecodeError...
    with suppress(JSONDecodeError):
        # ...parse the response as json if possible
        content = loads(content)

    # Return the tuple of request, content etc.
    return Response(req, content, json, status_code, resp_url, headers, cookiejar)
