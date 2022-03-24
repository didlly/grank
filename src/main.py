import sys
from platform import system
from os.path import dirname
from scripts.snakeeyes import snakeeyes_parent
from utils.console import fore, style
from requests import get

if system().lower() == "windows":
	import ctypes
	kernel32 = ctypes.windll.kernel32
	kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
 
if getattr(sys, "frozen", False):
	cwd = dirname(sys.executable)
elif __file__:
	cwd = dirname(__file__)
	
cwd = f"{cwd}/" if cwd != "" else cwd

with open(f"{cwd}current_version", "r") as f:
	version = f.read()

print(f"""{fore.Magenta}
░██████╗░██████╗░░█████╗░███╗░░██╗██╗░░██╗
██╔════╝░██╔══██╗██╔══██╗████╗░██║██║░██╔╝
██║░░██╗░██████╔╝███████║██╔██╗██║█████═╝░
{fore.Bright_Magenta}██║░░╚██╗██╔══██╗██╔══██║██║╚████║██╔═██╗░
╚██████╔╝██║░░██║██║░░██║██║░╚███║██║░╚██╗
░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝
{style.RESET_ALL}
{style.Italic + style.Bold}GITHUB: {style.RESET_ALL}https://github.com/didlly/grank
{style.Italic + style.Bold}INSTALLED VERSION: {style.RESET_ALL}{version}
{style.Italic + style.Bold}LATEST VERSION: {style.RESET_ALL}{get("https://raw.githubusercontent.com/didlly/grank/main/src/current_version").content.decode()}
{style.Italic + style.Bold}DISCORD SERVER: {style.RESET_ALL}https://discord.com/invite/h7jK9pBkAs
""")

import logging
from os import mkdir
from datetime import datetime
from configuration.config import load_config
from configuration.credentials import load_credentials
from threading import Thread
from utils.shared import data
from utils.shifts import shifts
from utils.logger import log
from discord.instance import Client as client
from json import load, dumps
from json.decoder import JSONDecodeError
from discord.guild_id import guild_id
from scripts.blackjack import blackjack_parent
from scripts.crime import crime_parent
from scripts.daily import daily_parent
from scripts.beg import beg_parent
from scripts.dig import dig_parent
from scripts.fish import fish_parent
from scripts.guess import guess_parent
from scripts.hunt import hunt_parent
from scripts.lottery import lottery_parent
from scripts.search import search_parent
from scripts.stream import stream_parent
from scripts.highlow import highlow_parent
from scripts.postmeme import postmeme_parent
from scripts.trivia import trivia_parent
from scripts.snakeeyes import snakeeyes_parent
from scripts.custom import custom_parent

try:
	mkdir(f"{cwd}logs/")
except FileExistsError:
	pass

logging.basicConfig(filename=f"{cwd}logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log", filemode="a", format="%(levelname)s %(asctime)s - %(message)s")

data["logger"] = logging.getLogger()

config = load_config(cwd)
credentials = load_credentials(cwd)

for index in range(len(credentials)):
	user_id = credentials[index][0]
	username = credentials[index][1]
	session_id = credentials[index][2]
	channel_id = credentials[index][3]
	token = credentials[index][4]
	data[channel_id] = True
 
	Client = client(config, user_id, username, session_id, channel_id, token)

	try:
		database = load(open(f"{cwd}database.json", "r"))
	except JSONDecodeError:
		log(None, "WARNING", "Database file is corrupted. Re-downloading now.")
		req = get("https://raw.githubusercontent.com/didlly/grank/main/src/database.json", allow_redirects=True).content
		log(None, "DEBUG", "Retreived new database file.")
		with open(f"{cwd}database.json", "wb") as db:
			log(None, "DEBUG", f"Opened `{cwd}database.json`.")
			db.write(req)
			log(None, "DEBUG", f"Wrote new database to `{cwd}database.json`.")
		log(None, "DEBUG", f"Closed `{cwd}database.json`.")
		database = load(open(f"{cwd}database.json", "r"))
		
	if f"{user_id}_confirmation" not in database.keys():
		Client.send_message("pls settings confirmations nah")
		database[f"{user_id}_confirmation"] = True
		with open(f"{cwd}database.json", "w") as database_file:
			database_file.write(dumps(database))

	guild_id(Client)
	
	if config["shifts"]["enabled"]:
		data[username] = False
		Thread(target=shifts, args=(username, config, cwd)).start()
	else:
		data[username] = True
	
	if config["custom commands"]["enabled"]:
		for key in config["custom commands"]:
			if key == "enabled":
				continue
			if config["custom commands"][key]["enabled"]:
				Thread(target=custom_parent, args=(Client, key, config["custom commands"][key]["cooldown"], config["custom commands"][key]["patron cooldown"])).start()
   
	if config["commands"]["daily"]:
		Thread(target=daily_parent, args=[Client, cwd]).start()

	if config["commands"]["beg"]:
		Thread(target=beg_parent, args=[Client]).start()

	if config["blackjack"]["enabled"]:
		Thread(target=blackjack_parent, args=[Client]).start()
  
	if config["commands"]["crime"]:
		Thread(target=crime_parent, args=[Client]).start()

	if config["commands"]["dig"]:
		Thread(target=dig_parent, args=[Client, cwd]).start()

	if config["commands"]["fish"]:
		Thread(target=fish_parent, args=[Client, cwd]).start()
  
	if config["commands"]["guess"]:
		Thread(target=guess_parent, args=[Client]).start()

	if config["commands"]["hunt"]:
		Thread(target=hunt_parent, args=[Client, cwd]).start()
  
	if config["lottery"]["enabled"]:
		Thread(target=lottery_parent, args=[Client, cwd]).start()

	if config["commands"]["search"]:
		Thread(target=search_parent, args=[Client]).start()
  
	if config["stream"]["enabled"]:
		Thread(target=stream_parent, args=[Client, cwd]).start()

	if config["commands"]["highlow"]:
		Thread(target=highlow_parent, args=[Client]).start()

	if config["commands"]["postmeme"]:
		Thread(target=postmeme_parent, args=[Client]).start()

	if config["snakeeyes"]["enabled"]:
		Thread(target=snakeeyes_parent, args=[Client]).start()

	if config["commands"]["trivia"]:
		Thread(target=trivia_parent, args=[Client, cwd]).start()