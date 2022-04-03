import contextlib
import sys
from os.path import dirname
from utils.logger import log
from os import system, mkdir, name
from datetime import datetime
from utils.shared import data
import logging

if name.lower() == "nt":
	import ctypes
	kernel32 = ctypes.windll.kernel32
	kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

if getattr(sys, "frozen", False):
	cwd = dirname(sys.executable)
elif __file__:
	cwd = dirname(__file__)

cwd = f"{cwd}/" if cwd != "" else cwd

with contextlib.suppress(FileExistsError):
	mkdir(f"{cwd}logs/")
logging.basicConfig(filename=f"{cwd}logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log", filemode="a", format="%(levelname)s %(asctime)s - %(message)s")

data["logger"] = logging.getLogger()

try:
    from requests import get
    log(None, "DEBUG", "Verified that the `requests` module is installed.")
except ModuleNotFoundError:
    log(None, "WARNING", "The `requests` module is not installed. Installing now.")
    system("pypy -m pip install 'requests'")
    log(None, "DEBUG", "Installed the `requests` module.")

try:
    from websocket import WebSocket
    log(None, "DEBUG", "Verified that the `websocket-client` module is installed.")
except ModuleNotFoundError:
    log(None, "WARNING", "The `websocket-client` module is not installed. Installing now.")
    system("pypy -m pip install 'websocket-client'")
    log(None, "DEBUG", "Installed the `websocket-client` module.")
