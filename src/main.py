from sys import argv
from contextlib import suppress
from os import mkdir
from os.path import dirname
from platform import system
from database.Verifier import verify
from configuration.Credentials import verify_credentials
from database.Handler import Database
from instance.Client import Instance
from utils.Console import fore, style
from utils.Logger import log
from discord.Gateway import gateway
from threading import Thread
from requests import get
from requests.exceptions import ConnectionError
from utils.Shared import data
from json import loads
from utils.Logger import log

if system().lower() == "windows":
    from ctypes import windll

    kernel32 = windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

cwd = dirname(argv[0])

cwd = cwd if cwd == "" else f"{cwd}/"

try:
    data["trivia"] = loads(
        get(
            "https://raw.githubusercontent.com/didlly/grank/main/src/trivia.json",
            allow_redirects=True,
        ).content
    )
except ConnectionError:
    log(
        "ERROR",
        "In case you didn't realise, Sherlock, you need an internet connection to run Grank ;-).",
    )

with open(f"{cwd}current_version", "r") as f:
    data["version"] = f.read()

latest_version = get(
    "https://raw.githubusercontent.com/didlly/grank/main/src/current_version"
).content.decode()

print(
    f"""{fore.Magenta}
░██████╗░██████╗░░█████╗░███╗░░██╗██╗░░██╗
██╔════╝░██╔══██╗██╔══██╗████╗░██║██║░██╔╝
██║░░██╗░██████╔╝███████║██╔██╗██║█████═╝░
{fore.Bright_Magenta}██║░░╚██╗██╔══██╗██╔══██║██║╚████║██╔═██╗░
╚██████╔╝██║░░██║██║░░██║██║░╚███║██║░╚██╗
░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝
{style.RESET_ALL}
{style.Italic + style.Bold}GITHUB: {style.RESET_ALL}https://github.com/didlly/grank
{style.Italic + style.Bold}INSTALLED VERSION: {style.RESET_ALL}{data['version']}
{style.Italic + style.Bold}LATEST VERSION: {style.RESET_ALL}{latest_version}
{style.Italic + style.Bold}DISCORD SERVER: {style.RESET_ALL}https://discord.com/invite/X3JMC9FAgy
"""
)

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
    verify(cwd, account, Client)
    Repository = Database(cwd, account, Client)

    Client.Repository = Repository
    Thread(target=gateway, args=[Client]).start()
