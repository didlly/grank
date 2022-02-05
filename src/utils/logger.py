from datetime import datetime
from os import makedirs
from utils.console import fore, style

def initialize_logger(cwd):
    try:
        # Make the directory `/logs/` if it doesn't exist.
        makedirs(f"{cwd}/logs/")
    except FileExistsError:
        # There is no `FolderExistsError`.
        pass
    
    # Return the file variable.
    return open(f"{cwd}/logs/{datetime.now().strftime('%d-%m-%Y~%H-%M')}.log", "w")

def register(log, username, level, text):
    # Log string to console.
    print(f"{datetime.now().strftime('[%x-%X]')}{f' - {fore.Bright_Magenta}{username}{style.RESET_ALL}' if username != None else ''} - {style.Italic}{fore.Bright_Red if level == 'ERROR' else fore.Bright_Blue if level == 'DEBUG' else fore.Bright_Yellow}[{level}]{style.RESET_ALL} | {text}")
    
    # Log string to logging file.
    log.write(f"{datetime.now().strftime('[%x-%X]')} - [{level}] | {text}\n")