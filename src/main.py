import sys
import utils.run
from os.path import dirname
from utils.logger import initialize_logger
from utils.configuration.verify_configuration import verify_configuration
from utils.configuration.verify_credentials import verify_credentials
from threading import Thread

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
credentials = verify_credentials(log, cwd)

for index, token in enumerate(credentials[0]["tokens"]):
    channel_id = credentials[0]["channel_ids"][index]
    ID = credentials[1][index]
    username = credentials[-1][index]
    utils.run.run[channel_id] = True

    if config["commands"]["daily"]:
        from scripts.daily import daily
        daily_thread = Thread(target=daily, args=(username, channel_id, token, config, log, cwd))
        daily_thread.start()

    if config["commands"]["beg"]:
        from scripts.beg import beg
        beg_thread = Thread(target=beg, args=(username, channel_id, token, config, log))
        beg_thread.start()

    if config["commands"]["dig"]:
        from scripts.dig import dig
        dig_thread = Thread(target=dig, args=(username, channel_id, token, config, log, ID, cwd))
        dig_thread.start()

    if config["commands"]["fish"]:
        from scripts.fish import fish
        fish_thread = Thread(target=fish, args=(username, channel_id, token, config, log, ID, cwd))
        fish_thread.start()

    if config["commands"]["hunt"]:
        from scripts.hunt import hunt
        hunt_thread = Thread(target=hunt, args=(username, channel_id, token, config, log, ID, cwd))
        hunt_thread.start()

    if config["commands"]["search"]:
        from scripts.search import search
        search_thread = Thread(target=search, args=(username, channel_id, token, config, log, ID))
        search_thread.start()

    if config["commands"]["highlow"]:
        from scripts.highlow import highlow
        highlow_thread = Thread(target=highlow, args=(username, channel_id, token, config, log, ID))
        highlow_thread.start()

    if config["commands"]["postmeme"]:
        from scripts.postmeme import postmeme
        postmeme_thread = Thread(target=postmeme, args=(username, channel_id, token, config, log, ID, cwd))
        postmeme_thread.start()

    if config["commands"]["trivia"]:
        from scripts.trivia import trivia
        trivia_thread = Thread(target=trivia, args=(username, channel_id, token, config, log, ID, cwd))
        trivia_thread.start()