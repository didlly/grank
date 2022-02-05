from json import load, loads
from utils.logger import register
from utils.console import style
from requests import get

def verify_credentials(log, cwd):
    try:
        credentials = load(open(f"{cwd}/credentials.json", "r"))
        register(log, None, "DEBUG", "Found `credentials.json` and parsed values from it.")
    except FileNotFoundError:
        register(log, None, "ERROR", "Unable to find `credentials.json`. Make sure the file is present.")
        _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
        exit(1)

    if "tokens" not in credentials.keys():
        register(log, None, "ERROR", "Unable to find `token` in `credentials.json`. Make sure it is present.")
        _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
        exit(1)
    else:
        register(log, None, "DEBUG", "Verified presence of value `token` in `credentials.json`.")
        
    if "channel_ids" not in credentials.keys():
        register(log, None, "ERROR", "Unable to find `channel_id` in `credentials.json`. Make sure it is present.")
        _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
        exit(1)
    else:
        register(log, None, "DEBUG", "Verified presence of value `channel_id` in `credentials.json`.")
    
    ID = []
    username = []

    for token in credentials["tokens"]:
        request = get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})  
        
        if request.status_code != 200:
            register(log, None, "ERROR", "Deemed one of the tokens as invalid. Please double-check you entered valid token(s) in `configuration.json`.")
            _ = input(f"\n{style.Italic and style.Faint}Press ENTER to exit the program...{style.RESET_ALL}")
            exit(1)
        
        data = loads(request.text)
        
        register(log, None, "DEBUG", f"Logged in as {data['username']}#{data['discriminator']}.")

        ID.append(data["id"])
        username.append(f"{data['username']}#{data['discriminator']}")
    
    print("")
    
    return credentials, ID, username