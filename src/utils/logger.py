from datetime import datetime
from utils.shared import data
from utils.console import fore, style

def log(username, level, text):
    print(f"{datetime.now().strftime('[%x-%X]')}{f' - {fore.Bright_Magenta}{username}{style.RESET_ALL}' if username is not None else ''} - {style.Italic}{fore.Bright_Red if level == 'ERROR' else fore.Bright_Blue if level == 'DEBUG' else fore.Bright_Yellow}[{level}]{style.RESET_ALL} | {text}")

    if level == "ERROR":
        data["logger"].error(text) 
    elif level == "debug":
        data["logger"].debug(text)
    else:
        data["logger"].warning(text)
    
    if level == "ERROR":
        _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
        exit(1)