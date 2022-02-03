import sys
from os.path import dirname
from utils.logger import initialize_logger
from utils.configuration.verify_configuration import verify_configuration
from utils.configuration.verify_credentials import verify_credentials
from scripts.daily import daily
from scripts.beg import beg
from scripts.dig import dig
from scripts.fish import fish
from scripts.hunt import hunt
from scripts.search import search
from scripts.highlow import highlow
from scripts.postmeme import postmeme
from time import time, sleep
from utils.logger import register

try:
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
except Exception:
    pass

if getattr(sys, "frozen", False):
    cwd = dirname(sys.executable)
elif __file__:
    cwd = dirname(__file__)

log = initialize_logger(cwd)

config = verify_configuration(log, cwd)
temp = verify_credentials(log, cwd)

credentials = temp[0]
ID = temp[-1]

del temp

token = credentials["token"]
channel_id = credentials["channel_id"]

del credentials

while True:
    print("")
    
    if config["commands"]["daily"]:
        try:
            daily(channel_id, token, config, log, cwd)
        except Exception:
            register(log, "WARNING", f"An unexpected error occured during the running of the `pls daily` command: `{sys.exc_info()}`")
    
    sleep(config["cooldowns"]["commands"])
    
    
    if config["commands"]["beg"]:
        try:
            beg(channel_id, token, config, log)
        except Exception:
            register(log, "WARNING", f"An unexpected error occured during the running of the `pls beg` command: `{sys.exc_info()}`")
        
    start = time()
    sleep(config["cooldowns"]["commands"])
    
    
    if config["commands"]["dig"]:
        try:
            dig(channel_id, token, config, log, ID)
        except Exception:
            register(log, "WARNING", f"An unexpected error occured during the running of the `pls dig` command: `{sys.exc_info()}`")
    
    sleep(config["cooldowns"]["commands"])    


    if config["commands"]["fish"]:
        try:
            fish(channel_id, token, config, log, ID)
        except Exception:
            register(log, "WARNING", f"An unexpected error occured during the running of the `pls fish` command: `{sys.exc_info()}`")
    
    sleep(config["cooldowns"]["commands"]) 


    if config["commands"]["hunt"]:
        try:
            hunt(channel_id, token, config, log, ID)
        except Exception:
            register(log, "WARNING", f"An unexpected error occured during the running of the `pls hunt` command: `{sys.exc_info()}`")
    
    sleep(config["cooldowns"]["commands"]) 
    
    
    if config["commands"]["search"]:
        try:
            search(channel_id, token, config, log, ID)
        except Exception:
            register(log, "WARNING", f"An unexpected error occured during the running of the `pls search` command: `{sys.exc_info()}`")
    
    sleep(config["cooldowns"]["commands"])
    
    
    if config["commands"]["highlow"]:
        try:
            highlow(channel_id, token, config, log, ID)
        except Exception:
            register(log, "WARNING", f"An unexpected error occured during the running of the `pls highlow` command: `{sys.exc_info()}`")
    
    sleep(config["cooldowns"]["commands"])
    
    
    if config["commands"]["postmeme"]:
        try:
            postmeme(channel_id, token, config, log, ID)
        except Exception:
            register(log, "WARNING", f"An unexpected error occured during the running of the `pls postmeme` command: `{sys.exc_info()}`")
    
    
    end = time()
    
    cooldown = 45 - (end - start)
    
    if cooldown >= 0:
        if config["logging"]["debug"]:
            register(log, "DEBUG", f"Beginning {cooldown} second cooldown between command loop.")
        sleep(cooldown)
    elif config["logging"]["debug"]:
            register(log, "DEBUG", f"Skipping cooldown since it is not needed.") 