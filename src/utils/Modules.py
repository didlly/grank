from os import name, system
from subprocess import check_call
from sys import executable

from utils.Logger import log


def verify_modules() -> None:
    """
    The verify_modules function checks to make sure that the `websocket-client` module is installed. If it is not,
    it will install it for you. This function should be called before any other functions in this library.

    Args:

    Returns:
        None
    """

    try:
        # Try and import the WebSocket class from the `websocket-client` module
        from websocket import WebSocket
    except ImportError:
        # If the `websocket-client` module is not installed, an ImportError would be raised, which is caught here, and the program will install the `websocket-client` module
        log(
            None,
            "WARNING",
            "Module `websocket-client` is not installed. Installing now.",
        )

        log(None, "DEBUG", "Verifying that pip is installed. This may take a while.")
        # Make sure pip is isntalled
        check_call([executable, "-m", "ensurepip"])

        log(None, "DEBUG", "Checking for an update for pip. This may take a while.")
        # Make sure pip is updated to the latest available version
        check_call([executable, "-m", "pip", "install", "-U", "pip", "wheel"])

        # ...install it
        check_call([executable, "-m", "pip", "install", "websocket-client"])
        log(None, "DEBUG", "Successfully installed the module `websocket-client`.")

        # Clear the terminal of any previous text (i.e, text from the installation process)
        system("cls" if name == "nt" else "clear")
