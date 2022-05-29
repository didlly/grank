from os import name, system
from subprocess import check_call
from sys import executable

from utils.Logger import log

def verify_modules() -> None:
    log(None, "DEBUG", "Verifying that pip is installed. This may take a while.")
    check_call([executable, "-m", "ensurepip"])

    log(None, "DEBUG", "Checking for an update for pip. This may take a while.")
    check_call([executable, "-m", "pip", "install", "-U", "pip", "wheel"])
   
    if "websocket-client" not in {pkg.key for pkg in __import__("pkg_resources").working_set}:
        log(
            None,
            "WARNING",
            "Module `websocket-client` is not installed. Installing now.",
        )

        check_call([executable, "-m", "pip", "install", "websocket-client"])

        log(None, "DEBUG", "Installed the module `websocket-client`.")
    else:
        log(None, "DEBUG", "Verified that the module `websocket-client` is installed.")

    system("cls" if name == "nt" else "clear")
