from os import name, system
from subprocess import check_call
from sys import exc_info, executable

from utils.Logger import log


def install(module: str) -> None:
    """
    The install function installs the specified module.

    Args:
        module (str): The module to install

    Returns:
        None
    """

    check_call([executable, "-m", "pip", "install", module])
    log(None, "DEBUG", f"Successfully installed the module `{module}`.")


def uninstall(module: str) -> None:
    """
    The uninstall function uninstalls the specified module.

    Args:
        module (str): The module to uninstall

    Returns:
        None
    """

    check_call([executable, "-m", "pip", "uninstall", module])
    log(None, "DEBUG", f"Successfully uninstalled the module `{module}`.")


def verify_modules() -> None:
    """
    The verify_modules function checks to make sure that the `websocket-client` module is installed. If it is not,
    it will install it for you. This function should be called before any other functions in this library.

    Args:
        None

    Returns:
        None
    """

    try:
        from websocket import WebSocketConnectionClosedException
    except ImportError:
        log(None, "DEBUG", "Verifying that pip is installed. This may take a while.")
        check_call([executable, "-m", "ensurepip"])

        log(None, "DEBUG", "Checking for an update for pip. This may take a while.")
        check_call([executable, "-m", "pip", "install", "-U", "pip", "wheel"])

        if "cannot import" in exc_info():
            uninstall("websocket")
            uninstall("websockets")

        log(
            None,
            "WARNING",
            "Module `websocket-client` is not installed. Installing now.",
        )

        check_call([executable, "-m", "pip", "install", "websocket-client"])
        log(None, "DEBUG", "Successfully installed the module `websocket-client`.")

        system("cls" if name == "nt" else "clear")
