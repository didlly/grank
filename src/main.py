import contextlib
import sys
from os.path import dirname
from platform import system

from requests import get
from utils.console import fore, style

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
from datetime import datetime
from json import dumps
from os import mkdir
from sys import exc_info
from threading import Thread

from configuration.config import load_config
from configuration.credentials import load_credentials
from discord.guild_id import guild_id
from discord.instance import Client as client
from scripts.beg import beg
from scripts.blackjack import blackjack
from scripts.crime import crime
from scripts.custom import custom
from scripts.daily import daily
from scripts.dig import dig
from scripts.fish import fish
from scripts.guess import guess
from scripts.highlow import highlow
from scripts.hunt import hunt
from scripts.lottery import lottery
from scripts.postmeme import postmeme
from scripts.search import search
from scripts.snakeeyes import snakeeyes
from scripts.stream import stream
from scripts.trivia import trivia
from scripts.vote import vote
from utils.logger import log
from utils.shared import data
from utils.shifts import shifts

with contextlib.suppress(FileExistsError):
	mkdir(f"{cwd}logs/")

logging.basicConfig(filename=f"{cwd}logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log", filemode="a", format="%(levelname)s %(asctime)s - %(message)s")

data["logger"] = logging.getLogger()

config = load_config(cwd)
credentials = load_credentials(cwd)

def run(credentials: dict, index: int):
	user_id = credentials[index][0]
	username = credentials[index][1]
	session_id = credentials[index][2]
	channel_id = credentials[index][3]
	token = credentials[index][4]
 
	Client = client(config, user_id, username, session_id, channel_id, token, cwd)
	
	if f"{user_id}_confirmation" not in Client.database.keys():
		Client.send_message("pls settings confirmations nah")
		Client.database[f"{user_id}_confirmation"] = True
		Client.database_file.write(dumps(Client.database))

	guild_id(Client)
	
	if Client.config["shifts"]["enabled"]:
		data[username] = False
		Thread(target=shifts, args=(Client)).start()
	else:
		data[username] = True
	   
	last_beg, last_blackjack, last_crime, last_dig, last_fish, last_guess, last_highlow, last_hunt, last_postmeme, last_search, last_snakeeyes, last_trivia = ["01/01/22-00:00:00"] * 12
	
	while True:
		if Client.config["commands"]["beg"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_beg, "%x-%X")).total_seconds() > 25) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_beg, "%x-%X")).total_seconds() > 45:
				try:
					beg(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls beg` command: `{exc_info()}`.")
				last_beg = datetime.now().strftime("%x-%X")
	
		if Client.config["blackjack"]["enabled"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_blackjack, "%x-%X")).total_seconds() > 5) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_blackjack, "%x-%X")).total_seconds() > 10:
				try:
					blackjack(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls blackjack` command: `{exc_info()}`.")
				last_blackjack = datetime.now().strftime("%x-%X")
	
		if Client.config["commands"]["crime"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_crime, "%x-%X")).total_seconds() > 15) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_crime, "%x-%X")).total_seconds() > 45:
				try:
					crime(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls crime` command: `{exc_info()}`.")
				last_crime = datetime.now().strftime("%x-%X")
	
		if Client.config["commands"]["daily"] and data[username]:
			if (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(Client.database["daily"], "%x-%X")).total_seconds() > 23400:
				try:
					daily(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls daily` command: `{exc_info()}`.")

				Client.database["daily"] = datetime.now().strftime("%x-%X")
				Client.database_file.write(dumps(Client.database))
	
				if Client.config["logging"]["debug"]:
					log(Client.username, "DEBUG", "Successfully updated latest command run of `pls daily`.")

		if Client.config["commands"]["dig"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_dig, "%x-%X")).total_seconds() > 25) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_dig, "%x-%X")).total_seconds() > 45:
				try:
					dig(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls dig` command: `{exc_info()}`.")
				last_dig = datetime.now().strftime("%x-%X")
	
		if Client.config["commands"]["fish"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_fish, "%x-%X")).total_seconds() > 25) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_fish, "%x-%X")).total_seconds() > 45:
				try:
					fish(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls fish` command: `{exc_info()}`.")
				last_fish = datetime.now().strftime("%x-%X")
	
		if Client.config["commands"]["guess"] and data[username]:
			if (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_guess, "%x-%X")).total_seconds() > 60:
				try:
					guess(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls guess` command: `{exc_info()}`.")
				last_guess = datetime.now().strftime("%x-%X")

		if Client.config["commands"]["highlow"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_highlow, "%x-%X")).total_seconds() > 15) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_highlow, "%x-%X")).total_seconds() > 30:
				try:
					highlow(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls highlow` command: `{exc_info()}`.")
				last_highlow = datetime.now().strftime("%x-%X")
	
		if Client.config["commands"]["hunt"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_hunt, "%x-%X")).total_seconds() > 25) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_hunt, "%x-%X")).total_seconds() > 40:
				try:
					hunt(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls hunt` command: `{exc_info()}`.")
				last_hunt = datetime.now().strftime("%x-%X")
	
		if Client.config["lottery"]["enabled"] and data[username]:
			if (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(Client.database["lottery"], "%x-%X")).total_seconds() > Client.config["lottery"]["cooldown"]:
				try:
					lottery(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls lottery` command: `{exc_info()}`.")
				
				Client.database["lottery"] = datetime.now().strftime("%x-%X")
				Client.database_file.write(dumps(Client.database))
	
				if Client.config["logging"]["debug"]:
					log(Client.username, "DEBUG", "Successfully updated latest command run of `pls lottery`.")

		if Client.config["commands"]["postmeme"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_postmeme, "%x-%X")).total_seconds() > 45) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_postmeme, "%x-%X")).total_seconds() > 50:
				try:
					postmeme(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls postmeme` command: `{exc_info()}`.")
				last_postmeme = datetime.now().strftime("%x-%X")
	
		if Client.config["commands"]["search"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_search, "%x-%X")).total_seconds() > 15) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_search, "%x-%X")).total_seconds() > 30:
				try:
					search(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls search` command: `{exc_info()}`.")
				last_search = datetime.now().strftime("%x-%X")

		if Client.config["snakeeyes"]["enabled"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_snakeeyes, "%x-%X")).total_seconds() > 5) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_snakeeyes, "%x-%X")).total_seconds() > 10:
				try:
					snakeeyes(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls snakeeyes` command: `{exc_info()}`.")
				last_snakeeyes = datetime.now().strftime("%x-%X")
	
		if Client.config["stream"]["enabled"] and data[username]:
			if (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(Client.database["stream"], "%x-%X")).total_seconds() > 600:
				try:
					stream(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls stream` command: `{exc_info()}`.")
				
				Client.database["stream"] = datetime.now().strftime("%x-%X")
				Client.database_file.write(dumps(Client.database))
	
				if Client.config["logging"]["debug"]:
					log(Client.username, "DEBUG", "Successfully updated latest command run of `pls stream`.")
	
		if Client.config["commands"]["trivia"] and data[username]:
			if (Client.config["cooldowns"]["patron"] and (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_trivia, "%x-%X")).total_seconds() > 3) or (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(last_trivia, "%x-%X")).total_seconds() > 5:
				try:
					trivia(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls trivia` command: `{exc_info()}`.")
				last_trivia = datetime.now().strftime("%x-%X")
	
		if Client.config["commands"]["vote"] and data[username]:
			if (datetime.strptime(datetime.now().strftime("%x-%X"), "%x-%X") - datetime.strptime(Client.database["vote"], "%x-%X")).total_seconds() > 43200:
				try:
					vote(Client)
				except Exception:
					if Client.config["logging"]["warning"]:
						log(Client.username, "WARNING", f"An unexpected error occured during the running of the `pls vote` command: `{exc_info()}`.")
      
				Client.database["vote"] = datetime.now().strftime("%x-%X")
				Client.database_file.write(dumps(Client.database))
	
				if Client.config["logging"]["debug"]:
					log(Client.username, "DEBUG", "Successfully updated latest command run of `pls vote`.")

		if Client.config["custom commands"]["enabled"]:
			for key in Client.config["custom commands"]:
				if key == "enabled":
					continue
				if Client.config["custom commands"][key]["enabled"]:
					try:
						exec(f"if (datetime.strptime(datetime.now().strftime('%x-%X'), '%x-%X') - datetime.strptime(custom_{key.replace(' ', '_')}, '%x-%X')).total_seconds() > Client.config['custom commands'][key]['cooldown']: custom(Client, key)")
					except NameError:
						exec(f"custom_{key.replace(' ', '_')} = '01/01/22-00:00:00'")
						custom(Client, key)
      
		while not data[username]:
			pass
		
		if Client.config["auto update"]:
			if Client.config["auto update"]["config"]:
				Client = client(config, user_id, username, session_id, channel_id, token, cwd)

for index in range(len(credentials)):
	Thread(target=run, args=[credentials, index]).start()