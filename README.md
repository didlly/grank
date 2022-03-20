<div align="center">
    <h1>Grank</h1>
    <a href="https://github.com/didlly/grank/stargazers">
        <img src=https://img.shields.io/github/stars/didlly/grank?style=for-the-badge&logo=Python&color=blue/>
    </a>
    <a href="https://github.com/didlly/grank/network/members">
	<img src=https://img.shields.io/github/forks/didlly/grank?style=for-the-badge&logo=Python&color=blue/>
    </a>
    <a href="https://github.com/didlly/grank/issues">
	<img src=https://img.shields.io/github/issues/didlly/grank?style=for-the-badge&logo=Python&color=informational/>
    </a>
    <a href="https://github.com/didlly/grank/pulls">
	<img src=https://img.shields.io/github/issues-pr/didlly/grank?style=for-the-badge&logo=Python&color=informational/>
    </a>
</div>

<div align="center">
    <sub>Inspired by <a href="https://github.com/dankgrinder/dankgrinder">this</a> repository. This is a WIP and there will be more functions added in the future. Special thanks to <a href="https://github.com/V4NSH4J">V4NSH4J</a> for helping me solve lots of the problems I encountered.</sub>
    <br>
    <a href="https://discord.gg/h7jK9pBkAs">
        Discord
    </a>
</div>

<img src="https://raw.githubusercontent.com/didlly/grank/main/assets/cover.png">

## Contents
* [What is Grank?](https://github.com/didlly/grank#what-is-grank)
* [Features](https://github.com/didlly/grank#features)
* [Supported commands](https://github.com/didlly/grank#supported-commands)
* [Todo](https://github.com/didlly/grank#todo)
* [Getting started](https://github.com/didlly/grank#getting-started)
	* [Setting up the environment.](https://github.com/didlly/grank#setting-up-the-environment)
        * [Windows](https://github.com/didlly/grank#Windows)
        * [macOS and Linux](https://github.com/didlly/grank#macOS-and-Linux)
	* [Getting your Discord token and channel ID.](https://github.com/didlly/grank#getting-your-discord-token-and-channel-id)
        * [How do you get this information](https://github.com/didlly/grank#how-do-you-get-this-information)
        * [How to enter them](https://github.com/didlly/grank#how-to-enter-them)
* [Config file](https://github.com/didlly/grank#config-file)
	* [```commands``` category](https://github.com/didlly/grank#commands-category)
    * [```auto_buy``` category](https://github.com/didlly/grank#auto_buy-category)
    * [```auto_trade``` category](https://github.com/didlly/grank#auto_trade-category)
    * [```typing_indicator``` category](https://github.com/didlly/grank#typing_indicator-category)
	* [```cooldowns``` category](https://github.com/didlly/grank#cooldowns-category)
	* [```logging``` category](https://github.com/didlly/grank#logging-category)
* [Disclaimer](https://github.com/didlly/grank#disclaimer)

## What is Grank?
Grank is a feature-rich script that automatically grinds Dank Memer for you. It is inspired by [dankgrinder](https://github.com/dankgrinder/dankgrinder). Since dankgrinder has been discontinued and the [recommended fork](https://github.com/V4NSH4J/dankgrinder) has also been discontinued, I decided to make my own version from scratch in Python.

## Features
- Supports multi-instancing.
- Efficiently coded.
- Smart - if the user doesn't have a required item to run a command like ```pls pm```, it will buy the required item so long as there are sufficient funds in the user's wallet & bank.
- Autotrade - the self-bot automates the acception of the trade on both the side of the trader and the trade receiver.
- Typing indicator.
- Detects special events like `Dodge the fireball`.
- Custom commands.

## Supported commands
- ```pls daily```
- ```pls beg```
- ```pls blackjack```
- ```pls crime```
- ```pls dig```
- ```pls fish```
- ```pls guess```
- ```pls highlow```
- ```pls hunt```
- ```pls lottery```
- ```pls postmeme```
- ```pls stream```
- ```pls search```
- ```pls snakeeyes```
- ```pls trivia```

## Todo
Visit [this](https://github.com/didlly/grank/projects/1) link for project updates.

## Getting Started

### Setting up the environment

#### Windows
Skip this and download the latest version of Grank from [here](https://github.com/didlly/grank/releases)

#### macOS and Linux
Unfortunately, I do not have access to a Mac or Linux device, so you will have to run the program from the source code.

- Download and extract the latest version of Grank from [here](https://github.com/didlly/grank/archive/refs/heads/main.zip).
- Navigate into the `/src/` folder of Grank.
- Download and extract the files of the latest version of [`pypy`](https://www.pypy.org/download.html) for your platform into the folder. Make sure the files are in the `/src/` folder and not in a sub-folder, otherwise this will not work.
- Download and save [this](https://bootstrap.pypa.io/get-pip.py) file in that directory.
- Open a command prompt in that directory.
- Run the command `pypy get-pip.py`. If you changed the name of the file when you downloaded it, please replace `get-pip.py` with the new name.
- Run the command `pypy installer.py`.

### Getting your Discord token and channel ID
To use Grank, you will have to provide your Discord token and a channel ID. Don't worry - these details are never shared with anyone. It is best if only you and Dank Memer can send messages in the channel you get the ID of. This is to avoid confusion with other people's interactions.

#### How do you get this information
- [Useful article on how to get your Discord token.](https://discordhelp.net/discord-token)

- [Useful article on how to get a channel ID.](https://docs.statbot.net/docs/faq/general/how-find-id/)

#### How to enter them
Since Grank supports multi-instancing, for every `token` you put in you will have to specify a `channel_id`. Open `src/credentials.json`. You should see a dictionary with two keys - `tokens` and `channel_ids`. As mentioned earlier, for every `token` you put in the list of `tokens`, you need to put a `channel id` in the list of `channel ids`. You can add as many entries as you want. The file has been filled in with a dummy layout so you know how to input your data.

You are now ready to use the program. Run ```pypy main.py``` in a command prompt in the `/src/` directory to start the program (or if you are on Windows run `main.exe`). You do not have to have Discord open to run the program, so you can have the program running in the background while you do other things! Grank also supports multi-instancing, so you can run the program on different accounts at once!

## Config file
The ```config.yml``` file is used to change the way the program runs.

### ```commands``` category
Values in the ```commands``` category tell the program whether or not to *run certain commands*.

| Name  | Type | Default Value | Description | 
| ------------- | ------------- | ------------- | ------------- |
| ```daily```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls daily```. |
| ```beg```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls beg```. |
| ```crime```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls crime```. |
| ```dig```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls dig```. |
| ```fish```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls fish```. |
| ```guess```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls guess```. |
| ```hunt```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls hunt```. |
| ```search```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls search```. |
| ```highlow```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls highlow```. |
| ```postmeme```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls postmeme```. |
| ```trivia```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls trivia```. |

### ```lottery``` category
Values in the ```lottery``` category tell the program *whether lottery tickets should be bought*, and *how often they should be bought*.

| Name  | Type | Default Value | Description | 
| ------------- | ------------- | ------------- | ------------- |
| ```enabled```  | ```Boolean``` | ```False```  | Tells the program whether or not to buy lottery tickets. |
| ```cooldown```  | ```Integer``` | ```3600```  | Tells the program the interval between buying lottery tickets. |

### ```stream``` category
Values in the ```stream``` category tell the program *whether or not to run the command ```pls stream```*, and *what buttons should it interact with*.

| Name  | Type | Default Value | Description | 
| ------------- | ------------- | ------------- | ------------- |
| ```enabled```  | ```Boolean``` | ```True```  | Tells the program whether or not to run the command ```pls stream`. |
| ```ads```  | ```Boolean``` | ```True```  | Tells the program whether or not to collect run ads during the stream. |
| ```chat```  | ```Boolean``` | ```True```  | Tells the program whether or not to read the chat during the stream. |
| ```donations```  | ```Boolean``` | ```True```  | Tells the program whether or not to collect donations during the stream. |

### ```blackjack``` category
Values in the ```blackjack``` category tell the program *whether or not to run the command ```pls blackjack```*, and *how much it should bet each time*.

| Name  | Type | Default Value | Description | 
| ------------- | ------------- | ------------- | ------------- |
| ```enabled```  | ```Boolean``` | ```False```  | Tells the program whether or not to run the command ```pls blackjack```. |
| ```random```  | ```Boolean``` | ```False```  | Tells the program whether or not to choose a random amount each time the command `pls blackjack` is run, or to choose a pre-set amount. |
| ```amount```  | ```Integer``` | ```1500```  | The pre-set amount to be bet if `random` is set to `False`. |
| ```minimum```  | ```Integer``` | ```1500```  | The minimum amount to be bet if `random` is set to `True`. |
| ```maximum```  | ```Integer``` | ```3000```  | The maximum amount to be bet if `random` is set to `True`. |

### ```snakeeyes``` category
Values in the ```snakeeyes``` category tell the program *whether or not to run the command ```pls snakeeyes```*, and *how much it should bet each time*.

| Name  | Type | Default Value | Description | 
| ------------- | ------------- | ------------- | ------------- |
| ```enabled```  | ```Boolean``` | ```False```  | Tells the program whether or not to run the command ```pls snakeeyes```. |
| ```random```  | ```Boolean``` | ```False```  | Tells the program whether or not to choose a random amount each time the command `pls snakeeyes` is run, or to choose a pre-set amount. |
| ```amount```  | ```Integer``` | ```1500```  | The pre-set amount to be bet if `random` is set to `False`. |
| ```minimum```  | ```Integer``` | ```1500```  | The minimum amount to be bet if `random` is set to `True`. |
| ```maximum```  | ```Integer``` | ```3000```  | The maximum amount to be bet if `random` is set to `True`. |

### ```custom commands``` category
Values in the ```custom commands``` category tell the program *what custom commands should be run* and *their cooldowns*.

| Name  | Type | Default Value | Description | 
| ------------- | ------------- | ------------- | ------------- |
| ```enabled```  | ```Boolean``` | ```False```  | Tells the program whether or not to run any of the custom commands. |

***NOTE:*** You can add your own custom commands by following the layout for the default options.

### ```shifts``` category
Values in the ```shifts``` category tell the program *whether or not to run Grank in shifts*, and *the length of active and passive phases*.

| Name  | Type | Default Value | Description | 
| ------------- | ------------- | ------------- | ------------- |
| ```enabled```  | ```Boolean``` | ```False```  | Tells the program whether or not to run in shifts. |
| ```active```  | ```Integer``` | ```7200```  | Tells the program how long the program should run before sleeping (in seconds). |
| ```passive```  | ```Integer``` | ```3600```  | Tells the program how long the program should sleep before running again (in seconds). |

### ```auto buy``` category
Values in the ```auto buy``` category tell the program whether or not to *buy certain items* if needed.

| Name  | Type | Default Value | Description | 
| ------------- | ------------- | ------------- | ------------- |
| ```enabled```  | ```Boolean``` | ```True```  | If this is set to ```True``` no items will be bought. If it is set to ```False``` the program will try and buy the item if their respective config value is ```True```. |
| ```laptop```  | ```Boolean``` | ```True```  | Tells the program whether or not to try and buy the item ```laptop``` if needed and the user doesn't have it. |
| ```shovel```  | ```Boolean``` | ```True```  | Tells the program whether or not to try and buy the item ```shovel``` if needed and the user doesn't have it. |
| ```fishing pole```  | ```Boolean``` | ```True```  | Tells the program whether or not to try and buy the item ```fishing pole``` if needed and the user doesn't have it. |
| ```hunting rifle```  | ```Boolean``` | ```True```  | Tells the program whether or not to try and buy the ```hunting rifle``` if needed and the user doesn't have it. |
| ```keyboard```  | ```Boolean``` | ```True```  | Tells the program whether or not to try and buy the item ```keyboard``` if needed and the user doesn't have it. |
| ```mouse```  | ```Boolean``` | ```True```  | Tells the program whether or not to try and buy the item ```mouse``` if needed and the user doesn't have it. |

### ```auto trade``` category
Values in the ```auto trade``` category tell the program *who items should be traded to*, and *what items should be traded.*

| Name  | Type | Default Value | Description | 
| ------------- | ------------- | ------------- | ------------- |
| ```enabled```  | ```Boolean``` | ```False```  | If this is set to ```True``` no items will be traded. If it is set to ```False``` the program will try and trade the item if their respective config value is ```True```. |
| ```trader_token```  | ```String``` | ```None```  | The token of the user the items should be traded to. |
| ```bank note```  | ```Boolean``` | ```True```  | Tells the program whether or not to try and trade the item ```bank note``` to the user specified in the ```trader```option. |
| ```tidepod```  | ```Boolean``` | ```True```  | Tells the program whether or not to try and trade the item ```tidepod``` to the user specified in the ```trader```option. |

***NOTE:*** You can add your own items to be traded by following the layout for the default options.

### ```typing indicator``` category
Values in the ```typing indicator``` category tell the program whether to make Discord think the self-bot is typing, and for how long it should. This is just for aesthetics and I would recommend it to be *off in private servers* to increase command speed, and *on in public servers* to make the self-bot look more legitimate.

| Name  | Type | Default Value | Description | 
| ------------- | ------------- | ------------- | ------------- |
| ```enabled```  | ```Boolean``` | ```False```  | If this is set to ```True```, the program will make Discord think the self-bot is typing. If it is set to ```False``` the program will not make Discord think the self-bot is typing, thus increasing command speed. |
| ```minimum```  | ```Float``` | ```0```  | The minimum time for the program to sleep after Discord is told that the user is typing. |
| ```maximum```  | ```Float``` | ```1```  | The maximum time for the program to sleep after Discord is told that the user is typing. |

### ```cooldowns``` category
Values in the ```cooldowns``` category tell the program whether to use cooldowns for *`patrons`* and what the *timeout is for getting responses from Dank Memer*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| ```patron```  | ```Boolean``` | ```False```  | Changes cooldowns to reflect the cooldowns of ```patrons```. |
| ```timeout```  | ```Integer``` | ```5```  | Timeout for waiting for responses from Dank Memer to commands that require user interaction (like ```pls search```). |

### ```logging``` category
Values in the ```logging``` category tell the program whether or not to log *```debug```* and *```warning```* messages. We would recommend having *at least* ```warning``` set to ```True```. Fatal errors will be logged regardless of the configuration.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| ```debug```  | ```Boolean``` | ```True```  | Tells the program whether or not to log ```debug``` messages. |
| ```warning```  | ```Boolean``` | ```True```  | Tells the program whether or not to log ```warning``` messages. |

***NOTE***: Values in the ```logging``` category do not affect logging messages sent when the configuration file is being loaded and the token is being verified.

## Disclaimer
This is a self-bot. Self-bots are against Discord's TOS. Automation of Dank Memer commands also breaks Dank Memer's rules. By using this program you acknowledge that I can take no responsibility for actions taken against you if you are caught.

This being said, I believe the chance of being caught running this script is low, provided you take the appropriate measures. The only probable way you will be caught is if someone tries to send you a message and you don't respond.

[![Stargazers repo roster for @didlly/grank](https://reporoster.com/stars/dark/didlly/grank)](https://github.com/didlly/grank/stargazers)

[![Forkers repo roster for @didlly/grank](https://reporoster.com/forks/dark/didlly/grank)](https://github.com/didlly/grank/network/members)
