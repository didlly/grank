from datetime import datetime
from typing import Union

from utils.console import fore, style
from utils.shared import data


def log(username: Union[str, None], level: str, text: str) -> None:
    """A function which logs messages to the console and to the log file.

    Args:
        username (str / None): The username of the account.
        level (str): The type of message to be logged.
        text (str): The message to be logged.
    
    Returns:
        None
    """
    
    print(f"{datetime.now().strftime('[%x-%X]')}{f' - {fore.Bright_Magenta}{username}{style.RESET_ALL}' if username is not None else ''} - {style.Italic}{fore.Bright_Red if level == 'ERROR' else fore.Bright_Blue if level == 'DEBUG' else fore.Bright_Yellow}[{level}]{style.RESET_ALL} | {text}")

    if level == "ERROR":
        data["logger"].error(text) 
    elif level == "DEBUG":
        data["logger"].debug(text)
    else:
        data["logger"].warning(text)
    
    if level == "ERROR":
        _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
        exit(1)