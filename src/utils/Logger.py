from datetime import datetime
from typing import Union

from utils.Console import fore, style


def log(username: Union[str, None], level: str, text: str) -> None:
    """
    The log function is used to log messages to the console.

    Args:
        username:Union[str, None]: Pass the username to the log function (or None if there is none)
        level (str): Specify the type of log message
        text (str): Pass in the text to be logged

    Returns:
        None
    """

    time = datetime.now().strftime("[%x-%X]")

    print(
        f"{time}{f' - {fore.Bright_Magenta}{username}{style.RESET_ALL}' if username is not None else ''} - {style.Italic}{fore.Bright_Red if level == 'ERROR' else fore.Bright_Blue if level == 'DEBUG' else fore.Bright_Yellow}[{level}]{style.RESET_ALL} | {text}"
    )

    if level == "ERROR":
        input(
            f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}\n"
        )
        exit(1)
