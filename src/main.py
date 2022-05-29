from contextlib import suppress
from os import mkdir
from os.path import dirname
from platform import system, python_version, python_implementation
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

verify_modules()

if system().lower() == "windows":
    from ctypes import windll

    kernel32 = windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

cwd = dirname(argv[0])

cwd = cwd if cwd == "" else f"{cwd}/"

data["trivia"] = request(
    "https://raw.githubusercontent.com/didlly/grank/main/src/trivia.json",
).content

with open(f"{cwd}current_version", "r") as f:
    data["version"] = f.read()

latest_version = request(
    "https://raw.githubusercontent.com/didlly/grank/main/src/current_version"
).content

print(f"Grank {style.Bold}{data['version']}{style.RESET_ALL} running on Python {style.Bold}v{python_version()}{style.RESET_ALL} ({style.Bold}{python_implementation()}{style.RESET_ALL}) using {style.Bold}{system()}{style.RESET_ALL}.\n")

if data["version"] != latest_version:
    log(None, "WARNING", f"New version available. Update if possible.")

with suppress(FileExistsError):
    mkdir(f"{cwd}logs/")

with suppress(FileExistsError):
    mkdir(f"{cwd}logs/{data['version']}")

accounts = verify_credentials(cwd)

for account in accounts:
    with suppress(FileExistsError):
        mkdir(f"{cwd}logs/{data['version']}/{account.token}")

    Client = Instance(cwd, account)
    verify(cwd, Client)
    Repository = Database(cwd, account, Client)

    Client.Repository = Repository
    Thread(target=__import__("discord.Gateway").Gateway.gateway, args=[Client]).start()
