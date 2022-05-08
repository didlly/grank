import sys
from contextlib import suppress
from os import mkdir
from os.path import dirname
from platform import system
from database.Verifier import verify
from configuration.Credentials import verify_credentials
from database.Handler import Database
from instance.Client import Instance
from instance.Shifts import shifts
from utils.Shared import data
from discord.Gateway import gateway
from threading import Thread

if system().lower() == "windows":
    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

if getattr(sys, "frozen", False):
    cwd = dirname(sys.executable)
elif __file__:
    cwd = dirname(__file__)

cwd = f"{cwd}/" if cwd != "" else cwd

with suppress(FileExistsError):
    mkdir(f"{cwd}logs/")

accounts = verify_credentials(cwd)

for account in accounts:
    with suppress(FileExistsError):
        mkdir(f"{cwd}logs/{account.token}")

    Client = Instance(cwd, account)
    verify(cwd, account, Client)
    Repository = Database(cwd, account, Client)

    if Repository.config["shifts"]["enabled"]:
        data[Client.username] = False
        Thread(target=shifts, args=[Client, Repository]).start()
    else:
        data[Client.username] = True

    Client.Repository = Repository
    Thread(target=gateway, args=[Client]).start()
