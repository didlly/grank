from utils.logger import log
from os import system

try:
    from requests import get
    log(None, "DEBUG", "Verified that the `requests` module is installed.")
except ModuleNotFoundError:
    log(None, "WARNING", "The `requests` module is not installed. Installing now.")
    system("pypy -m pip install 'requests'")
    log(None, "DEBUG", "Installed the `requests` module.")
    
try:
    from yaml import safe_load
    log(None, "DEBUG", "Verified that the `yaml` module is installed.")
except ModuleNotFoundError:
    log(None, "WARNING", "The `yaml` module is not installed. Installing now.")
    system("pypy -m pip install 'yaml'")
    log(None, "DEBUG", "Installed the `yaml` module.")
    
try:
    from websocket import WebSocket
    log(None, "DEBUG", "Verified that the `websocket-client` module is installed.")
except ModuleNotFoundError:
    log(None, "WARNING", "The `websocket-client` module is not installed. Installing now.")
    system("pypy -m pip install 'websocket-client'")
    log(None, "DEBUG", "Installed the `websocket-client` module.")