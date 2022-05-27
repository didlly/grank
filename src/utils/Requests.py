"""
UNLICENSED
This is free and unencumbered software released into the public domain.

https://github.com/sesh/thttp

NOTE: This is an edited version of `thttp`, the link to which is aforementioned.
"""

import gzip
import ssl
from json import loads, dumps
from json.decoder import JSONDecodeError
from contextlib import suppress
from utils.Logger import log
from base64 import b64encode
from collections import namedtuple

from http.cookiejar import CookieJar
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import (
    Request,
    build_opener,
    HTTPRedirectHandler,
    HTTPSHandler,
    HTTPCookieProcessor,
)


Response = namedtuple("Response", "request content json status_code url headers cookiejar")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(
    url,
    params={},
    json=None,
    data=None,
    headers={},
    method="GET",
    verify=False,
    redirect=True,
    cookiejar=None,
    basic_auth=None,
    timeout=None,
):
    """
    Returns a (named) tuple with the following properties:
        - request
        - content
        - json (dict; or None)
        - headers (dict; all lowercase keys)
            - https://stackoverflow.com/questions/5258977/are-http-headers-case-sensitive
        - status
        - url (final url, after any redirects)
        - cookiejar
    """
    method = method.upper()
    headers["User-Agent"] = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
    headers = {k.lower(): v for k, v in headers.items()}  # lowercase headers

    if params:
        url += "?" + urlencode(params)  # build URL from params
    if json and data:
        raise Exception("Cannot provide both json and data parameters")
    if method not in ["POST", "PATCH", "PUT"] and (json or data):
        raise Exception(
            "Request method must POST, PATCH or PUT if json or data is provided"
        )
    if not timeout:
        timeout = 60

    if json:  # if we have json, stringify and put it in our data variable
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

    ctx = ssl.create_default_context()
    if not verify:  # ignore ssl errors
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    handlers = []
    handlers.append(HTTPSHandler(context=ctx))
    handlers.append(HTTPCookieProcessor(cookiejar=cookiejar))

    if not redirect:
        no_redirect = NoRedirect()
        handlers.append(no_redirect)

    opener = build_opener(*handlers)
    req = Request(url, data=data, headers=headers, method=method)
    
    try:
        with opener.open(req, timeout=timeout) as resp:
            status_code, content, resp_url = (resp.getcode(), resp.read().decode(), resp.geturl())
            headers = {k.lower(): v for k, v in list(resp.info().items())}

            if "gzip" in headers.get("content-encoding", ""):
                content = gzip.decompress(content).decode()

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
            content = gzip.decompress(content).decode()

        json = (
            loads(content)
            if "application/json" in headers.get("content-type", "").lower() and content
            else None
        )
    except URLError:
        log(
            None,
            "ERROR",
            "In case you didn't realise, Sherlock, you need an internet connection to run Grank ;-).",
        )
    
    with suppress(JSONDecodeError):
        content = loads(content)
    
    return Response(req, content, json, status_code, resp_url, headers, cookiejar)