from json import load, loads
from utils.logger import register
from utils.console import style
from requests import get

def verify_credentials(log, cwd):
    try:
        credentials = load(open(f"{cwd}/credentials.json", "r"))
        register(log, "DEBUG", "Found `credentials.json` and parsed values from it.")
    except FileNotFoundError:
        register(log, "ERROR", "Unable to find `credentials.json`. Make sure the file is present.")
        _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
        exit(1)

    if "token" not in credentials.keys():
        register(log, "ERROR", "Unable to find value `token` in `credentials.json`. Make sure the value is present.")
        _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
        exit(1)
    else:
        register(log, "DEBUG", "Verified presence of value `token` in `credentials.json`.")
        
    if "channel_id" not in credentials.keys():
        register(log, "ERROR", "Unable to find value `channel_id` in `credentials.json`. Make sure the value is present.")
        _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
        exit(1)
    else:
        register(log, "DEBUG", "Verified presence of value `channel_id` in `credentials.json`.")
    
    request = get("https://discord.com/api/v9/users/@me", headers={"Authorization": credentials["token"]})  
    
    if request.status_code != 200:
        register(log, "ERROR", "Deemed `token` as invalid. Please double-check you entered the right token in `configuration.json`.")
        _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
        exit(1)
    
    data = loads(request.text)
    
    register(log, "DEBUG", f"Logged in as {data['username']}#{data['discriminator']}.")
    
    return credentials, data["id"]