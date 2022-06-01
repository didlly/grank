"""
The `main.py` file controls everything that Grank does. It spawns the threads for actions like connecting to the Discord websocket, monitoring shifts etc.
"""

from contextlib import suppress
from os import mkdir
from os.path import dirname
from platform import python_implementation, python_version, system
from sys import argv
from threading import Thread

from configuration.Credentials import verify_credentials
from database.Handler import Database
from database.Verifier import verify
from instance.Client import Instance
from utils.Console import style
from utils.Logger import log
from utils.Modules import verify_modules
from utils.Requests import request
from utils.Shared import data

# Check that all the required modules are installed
verify_modules()

# If the OS is Windows...
if system().lower() == "windows":
    from ctypes import windll

    # ...make sure the terminal supports ANSI (coloured) output
    kernel32 = windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Get the cwd (current working directory)
cwd = dirname(argv[0])

# If Python could not determine the cwd, set it to an empty string, else concaternate a `/` to it
cwd = cwd if cwd == "" else f"{cwd}/"

# Get the latest trivia database
data["trivia"] = request(
    "https://raw.githubusercontent.com/didlly/grank/main/src/trivia.json",
).content

# Open the `current_verion` file and...
with open(f"{cwd}current_version", "r") as f:
    # ...read the current verison from it
    data["version"] = f.read()

latest_version = request(
    "https://raw.githubusercontent.com/didlly/grank/main/src/current_version"
).content

# Output: 1. Current Grank version, 2. Current Python version, 3. Python implementation (CPython, PyPy etc), 4. Operating System
print(
    f"Grank {style.Bold}{data['version']}{style.RESET_ALL} running on Python {style.Bold}v{python_version()}{style.RESET_ALL} ({style.Bold}{python_implementation()}{style.RESET_ALL}) using {style.Bold}{system()}{style.RESET_ALL}.\n"
)

# If the installed version isn't the same as the latest version...
if data["version"] != latest_version:
    # ...tell the user to update if possible
    log(None, "WARNING", f"New version available. Update if possible.")

# ...suppres a FileExistsError...
with suppress(FileExistsError):
    # ...make the logs directory
    mkdir(f"{cwd}logs/")

# ...suppres a FileExistsError...
with suppress(FileExistsError):
    # ...make this version's logs directory
    mkdir(f"{cwd}logs/{data['version']}")

# Get details about all the accounts entered in `credentials.json`
accounts = verify_credentials(cwd)

# Import the `gateway` module (wasn't imported before since the modules required might not have been installed then)
gateway = __import__("discord.Gateway").Gateway.gateway

for account in accounts:
    # ...suppres a FileExistsError...
    with suppress(FileExistsError):
        # ...make this account's logs directory
        mkdir(f"{cwd}logs/{data['version']}/{account.token}")

    # Initialize the class for this account for interacting with Discord
    Client = Instance(cwd, account)

    # Make sure this account's database is not corrupted
    verify(cwd, Client, account)

    # Initialize the class for this account for interacting with it's database
    Repository = Database(cwd, account, Client)

    # Merge the account's database class with it's client class.
    Client.Repository = Repository

    # Start the websocket session for this account
    Thread(target=gateway, args=[Client]).start()
