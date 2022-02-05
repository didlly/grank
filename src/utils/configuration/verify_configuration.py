from yaml import safe_load
from utils.logger import register
from utils.console import style

def verify_configuration(log, cwd):
    try:
        config = safe_load(open(f"{cwd}/config.yml", "r"))
        register(log, None, "DEBUG", "Found `config.yml` and parsed values from it.")
    except FileNotFoundError:
        register(log, None, "ERROR", "Unable to find `config.yml`. Make sure the file is present.")
        _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
        exit(1)
     
    return config