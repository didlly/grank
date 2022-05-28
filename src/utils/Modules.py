from os import name, system
from subprocess import check_call
from sys import executable

from pkg_resources import working_set


def verify_modules() -> None:
    if "websocket-client" not in {pkg.key for pkg in working_set}:
        check_call([executable, "-m", "pip", "install", "websocket-client"])
        system("cls" if name == "nt" else "clear")
