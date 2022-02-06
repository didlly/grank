from requests import post, get
from utils.logger import register
from time import sleep, time
from json import loads, load
from sys import exc_info
from utils.console import style
import utils.run

def trivia(username, channel_id, token, config, log, ID, cwd):
    def trivia_run(username, channel_id, token, config, log, ID, cwd):
        request = post(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token}, data={"content": "pls trivia"})
        
        if request.status_code != 200:
            if config["logging"]["warning"]:
                register(log, username, "WARNING", f"Failed to send command `pls trivia`. Status code: {request.status_code} (expected 200). Aborting command.")
            return
        
        if config["logging"]["debug"]:
            register(log, username, "DEBUG", "Successfully sent command `pls trivia`.")
        
        latest_message = None
        
        for _ in range(0, config["cooldowns"]["timeout"] * 10):
            sleep(0.1)
            
            request = get(f"https://discord.com/api/v8/channels/{channel_id}/messages", headers={"authorization": token})
            
            if request.status_code != 200:
                continue

            latest_message = loads(request.text)[0]
            
            if latest_message["author"]["id"] == "270904126974590976" and latest_message["referenced_message"]["author"]["id"] == ID:
                if config["logging"]["debug"]:
                    register(log, username, "DEBUG", "Got Dank Memer's response to command `pls trivia`.")
                break
            else:
                continue 
        
        if latest_message is None or latest_message["author"]["id"] != "270904126974590976":
            if config["logging"]["warning"]:
                register(log, username, "WARNING", f"Timeout exceeded for response from Dank Memer ({config['cooldowns']['timeout']} {'second' if config['cooldowns']['timeout'] == 1 else 'seconds'}). Aborting command.")
            return

        try:
            answer = load(open(f"{cwd}/data.json", "r"))["trivia"][latest_message["embeds"][0]["description"].split("\n")[0].replace("*", "").replace('"', "&quot;")]
        except KeyError:
            register(log, None, "WARNING", f"Unknown trivia question `{latest_message['embeds'][0]['description'][0].replace('*', '')}`. Anwers: `{latest_message['components'][0]['components']}`. Please create an issue on Grank highlighting this.")
            _ = input(f"\n{style.Italic and style.Faint}Press ENTER to continue the running of the program...{style.RESET_ALL}")
            return
        
        custom_id = None

        for index, possible_answer in enumerate(latest_message["components"][0]["components"]):
            if possible_answer["label"] == answer:
                custom_id = latest_message["components"][0]["components"][index]["custom_id"]

        if custom_id is None:
            register(log, None, "WARNING", f"Unknown answer to trvia question `{latest_message['embeds'][0]['description'].replace('*', '')}`. Anwers: `{latest_message['components'][0]['components']}`. Please create an issue on Grank highlighting this.")
            _ = input(f"\n{style.Italic and style.Faint}Press ENTER to continue the running of the program...{style.RESET_ALL}")
            return

        data = {
            "application_id": 270904126974590976,
            "channel_id": channel_id,
            "type": 3,
            "data": {
                "component_type": 2,
                "custom_id": custom_id
            },
            "guild_id": latest_message["message_reference"]["guild_id"],
            "message_flags": 0,
            "message_id": latest_message["id"]
        }
        
        request = post(f"https://discord.com/api/v9/interactions", headers={"authorization": token}, json=data)
        
        if request.status_code == 200 or request.status_code == 204:
            if config["logging"]["debug"]:
                register(log, username, "DEBUG", "Successfully interacted with button on Dank Memer's response to command `pls trivia`.")
        elif config["logging"]["warning"]:
            register(log, username, "WARNING", f"Failed to interact with button on Dank Memer's response to command `pls trivia`. Status code: {request.status_code} (expected 200 or 204).")

    while True:
        while not utils.run.run[channel_id]:
            pass

        utils.run.run[channel_id] = False

        start = time()

        try:
            trivia_run(username, channel_id, token, config, log, ID, cwd)
        except Exception:
            register(log, username, "WARNING", f"An unexpected error occured during the running of the `pls trivia` command: `{exc_info()}`")
        
        end = time()

        utils.run.run[channel_id] = True

        if config["cooldowns"]["patron"]:
            cooldown = 3 - (end - start)
        else:
            cooldown = 5 - (end - start)

        if cooldown > 0:
            sleep(cooldown)