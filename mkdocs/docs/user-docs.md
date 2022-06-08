# User Documentation

[![Join our Discord](https://www.oathro.com/themes/oathro/img/discord-button.png)](https://discord.gg/X3JMC9FAgy)

## Features
* Ease of use - Once Grank has been setup, you can control it through Discord using many different and useful commands.
* Smart - If Grank detects that the account does not have an item required for a command (e.g. not having a `hunting rifle` for the `pls hunt` command), Grank will automatically buy the item. What if the account doesn't have enough money in it's wallet? Then Grank checks the amount of money in the account's bank. If the two combined provide sufficient funds to buy the item, Grank will withdraw the required amount (and no more), and will buy the item. If the account doesn't have enough money in it's wallet and bank combined, Grank logs a warning stating this.
* Anti detection features - Grank has many features to prevent detection by Dank Memer, Discord or other users. One of these such features is a Typing Indicator. When you start typing a message on Discord, a typing indicator appears, which lets everyone else in the channel know you are typing a message. If enabled, Grank will trigger the Typing Indicator, wait a random amount (which can be controlled in the config), and send the command. This also adds a random gap between commands that makes the self-bot more human.
* Custom commamds - Want to periodically run a command like `pls bet 1000`? Well you can with Grank. Either add the command to the config file, or take advantage of Grank's self-bot commands feature and run the command `grank command add {command} {interval}` (where `command` is the command to be run and `interval` is how often it should be run).
* Anti heist - If someone is heisting you, Grank will stop it.
* Auto join heist - If someone else is being heisted, Grank will join the heist.
* Auto trade - Automatically trades specified items to an alt account upon receiving the item.
* Auto accept trade - If someone sends a trade request to Grank, Grank will automatically accept it (provided they are in the allowed user list to do so).

***NOTE:*** All these options can be toggled and customised in the config.

## Supported commands

* `pls adv`
* `pls beg`
* `pls blackjack`
* `pls crime`
* `pls daily`
* `pls dig`
* `pls fish`
* `pls guess`
* `pls highlow`
* `pls hunt`
* `pls lottery`
* `pls postmeme`
* `pls search`
* `pls snakeeyes`
* `pls stream`
* `pls trivia`
* `pls work`

## Installing for the first time
* Download and extract the latest version of Grank from [here](https://github.com/didlly/grank/archive/refs/heads/main.zip).

### Windows
* Download PyPy from [here](https://downloads.python.org/pypy/pypy3.9-v7.3.9-win64.zip).
* Extract the contents into the `/src` directory.

### Linux
* Download PyPy from [here](https://downloads.python.org/pypy/pypy3.9-v7.3.9-linux64.tar.bz2) (or if that doesn't work from [here](https://downloads.python.org/pypy/pypy3.9-v7.3.9-aarch64-portable.tar.bz2)).
* Extract the contents into the `/src` directory.

### macOS
* Download PyPy from [here](https://downloads.python.org/pypy/pypy3.9-v7.3.9-osx64.tar.bz2).
* Extract the contents into the `/src` directory.

***NOTE:*** Everytime you update Grank's source code, you do **NOT HAVE** to re-download PyPy.

## Updating
* Download and extract the latest version of Grank from [here](https://github.com/didlly/grank/archive/refs/heads/main.zip) into the directory you extracted the previous version of Grank into. Let it overwrite any existing files.

## Setting up Grank
To use Grank, you will have to provide your Discord token. Don't worry, your token is never shared with anyone else.

[Useful Youtube video on how to get your Discord Token](https://www.youtube.com/watch?v=WWHZoa0SxCc)

### How to enter these details.

Open `src/credentials.json`. You should see a dictionary with a key called `TOKEN`. Add your token into the list after this key. You can add as many entries as you want. The file has been filled in with a dummy layout so you know how to input your data.

You are now ready to use the program. Run `pypy main.py` (or `pypy3 main.py`) in a command prompt in the `/src` directory to start the program. You do not have to have Discord open to run the program, so you can have the program running in the background while you do other things!

## How to use Grank
Now you have Grank set-up, you are probably wondering how to use Grank. Grank is controlled through Discord. You can view all the commands below, or run `grank help` to get started on your journey using Grank. You will find more information by running the specific `-help` command for each command category.

### Supported commands
`grank help` - Displays the help command.

### `autostart` category

| Name | Description |
| ------------- | ------------- |
| `autostart`  | Shows a list of all the auto-start channels for this account. |
| `autostart -help`  | Shows help about the `autostart` command. |
| `autostart enable` | Enables the auto-start channels function. |
| `autostart disable` | Disables the auto-start channels function. |
| `autostart add 0` | Adds the channel with the ID of `0` to the list of auto-start channels. |
| `autostart remove` | Removes the autostart channel. |

### `commands / cmds` category

| Name | Description |
| ------------- | ------------- |
| `commands`  | Shows a list of all the custom commands for this account. |
| `commands -help`  | Shows help about the `commands` command. |
| `commands add pls_help 69` | Adds the custom command 'pls help' to the list of custom commands and tells Grank it needs to be run every 69 seconds. |
| `commands remove pls_help 69` | Removes the custom commands called 'pls help' from the list of custom commands. |

### `config / conf` category

| Name | Description |
| ------------- | ------------- |
| `config`  | Shows a list of all the config options and their values for this account. |
| `config -help`  | Shows help about the `config` command. |
| `config reset` | Resets the config to the default settings. |
| `config.cooldowns.patron`  | Displays the value of the patron key in the subconfig cooldowns. |
| `config.cooldowns.patron = True`  | Sets the patron key in the subconfig cooldowns to True. |

***NOTE***: To access keys containing a space character, replace the space with an underscore (_).

### `controllers / cont` category

| Name | Description |
| ------------- | ------------- |
| `controllers`  | Shows a list of all the controllers for this account. |
| `controllers -help`  | Shows help about the `controllers` command. |
| `controllers purge 0`  | Removes all the logged messages from the controller with the ID of `0`. |
| `controllers info 0`  | Provides information about the controller. This includes information such as when the controller was added, which account added the controller, and what commands the controller has run. |
| `controllers add 0:`  | Adds the account with the ID of `0` to the list of controllers. |
| `controllers remove 0`  | Removes the account with the ID of `0` from the list of controllers. |

***NOTE:*** You can also @mention the user you want to interact with.

### `database / db` category

| Name | Description |
| ------------- | ------------- |
| `database`  | Shows a list of all the database options and their values for this account. |
| `database -help`  | Shows help about the `database` command. |
| `database reset`  | Resets the database to the default settings. |

### `info / inf` category

| Name | Description |
| ------------- | ------------- |
| `info`  | Shows info about the grinder (like session stats, commands ran stats, etc). |

### `servers` category

| Name | Description |
| ------------- | ------------- |
| `servers`  | Shows a list of all the blacklisted servers for this account. |
| `servers -help`  | Shows help about the `servers` command. |
| `servers enable` | Enables the blacklisted servers function. |
| `servers disable` | Disables the blacklisted servers function. |
| `servers add 0` | Adds the server with the ID of `0` to the list of blacklisted servers. |
| `servers remove 0` | Removes the server with the ID of `0` from the list of blacklisted servers. |

### `shifts` category

| Name | Description |
| ------------- | ------------- |
| `shifts`  | Shows a list of all the shifts for this account. |
| `shifts -help`  | Shows help about the `shifts` command. |
| `shifts enable` | Enables the shifts function. |
| `shifts disable` | Disables the shifts function. |
| `shifts add 7200 3600 60` | Adds a shift with an active length of `7200`, a passive length of `3600`, and a variation of `60`. |
| `shifts remove 1` | Removes the 1st shift profile. |

### `start` category

| Name | Description |
| ------------- | ------------- |
| `start`  | Starts the grinder. |
| `start -help`  | Shows help about the `start` command. |

### `stop` category

| Name | Description |
| ------------- | ------------- |
| `stop`  | Stops the grinder. |
| `stop -help`  | Shows help about the `stop` command. |

## Config file

The `config.yml` file is used to change the way the program runs.

### `commands` category

Values in the `commands` category tell the program whether or not to *run certain commands*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `adventure`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls adventure`. |
| `beg`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls beg`. |
| `daily`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls daily`. |
| `dig`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls dig`. |
| `fish`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls fish`. |
| `guess`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls guess`. |
| `highlow`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls highlow`. |
| `hunt`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls hunt`. |
| `postmeme`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls postmeme`. |
| `trivia`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls trivia`. |
| `vote`  | `Boolean` | `True`  | Tells the program whether or not to vote for Dank Memer on Discord Bot List. |
| `work`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls work`. |

### `crime` category
Values in the `crime` category tell the program *whether or not to run the command `pls crime`*, and *what places to choose* (or random).

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls crime`. |
| `random`  | `Boolean` | `True`  | Tells the program whether or not to choose a random place. |

#### __`preferences` subcategory__
This subcategory tells the program what places to choose, if they are available, and if `random` is set to `False`. You can make the program skip an option by setting it to `False`. The first option takes priority over the second option, etc. They do not have to be the same case as Dank Memer's options, and you can use shorten the name since Grank compares them using the `in` operator. Please do not add `'`s into the names of places to be searched, since it will cause a parsing error. The program will handle `'`s itself until the bug is fixed.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `tax evasion`  | `Boolean` | `True`  | Tells the program to choose `tax evasion` if it is present. |
| `vandalism`  | `Boolean` | `True`  | Tells the program to choose `vandalism` if it is present. |

### `search` category
Values in the `search` category tell the program *whether or not to run the command `pls search`*, and *what places to choose* (or random).

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls search`. |
| `random`  | `Boolean` | `True`  | Tells the program whether or not to choose a random place. |

#### __`preferences` subcategory__
This subcategory tells the program what places to choose, if they are available, and if `random` is set to `False`. You can make the program skip an option by setting it to `False`. The first option takes priority over the second option, etc. They do not have to be the same case as Dank Memer's options, and you can use shorten the name since Grank compares them using the `in` operator. Please do not add `'`s into the names of places to be searched, since it will cause a parsing error. The program will handle `'`s itself until the bug is fixed.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `Gods own place`  | `Boolean` | `True`  | Tells the program to choose `Gods own place` if it is present. |
| `bank`  | `Boolean` | `True`  | Tells the program to choose `bank` if it is present. |

### `lottery` category

Values in the `lottery` category tell the program *whether lottery tickets should be bought*, and *how often they should be bought*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | Tells the program whether or not to buy lottery tickets. |
| `cooldown`  | `Integer` | `3600`  | Tells the program the interval between buying lottery tickets. |

### `stream` category

Values in the `stream` category tell the program *whether or not to run the command `pls stream`*, and *what buttons should it interact with*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `True`  | Tells the program whether or not to run the command `pls stream`. |
| `ads`  | `Boolean` | `True`  | Tells the program whether or not to collect run ads during the stream. |
| `chat`  | `Boolean` | `True`  | Tells the program whether or not to read the chat during the stream. |
| `donations`  | `Boolean` | `True`  | Tells the program whether or not to collect donations during the stream. |

### `blackjack` category

Values in the `blackjack` category tell the program *whether or not to run the command `pls blackjack`*, and *how much it should bet each time*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | Tells the program whether or not to run the command `pls blackjack`. |
| `random`  | `Boolean` | `False`  | Tells the program whether or not to choose a random amount each time the command `pls blackjack` is run, or to choose a pre-set amount. |
| `amount`  | `Integer` | `1500`  | The pre-set amount to be bet if `random` is set to `False`. |
| `minimum`  | `Integer` | `1500`  | The minimum amount to be bet if `random` is set to `True`. |
| `maximum`  | `Integer` | `3000`  | The maximum amount to be bet if `random` is set to `True`. |

### `snakeeyes` category

Values in the `snakeeyes` category tell the program *whether or not to run the command `pls snakeeyes`*, and *how much it should bet each time*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | Tells the program whether or not to run the command `pls snakeeyes`. |
| `random`  | `Boolean` | `False`  | Tells the program whether or not to choose a random amount each time the command `pls snakeeyes` is run, or to choose a pre-set amount. |
| `amount`  | `Integer` | `1500`  | The pre-set amount to be bet if `random` is set to `False`. |
| `minimum`  | `Integer` | `1500`  | The minimum amount to be bet if `random` is set to `True`. |
| `maximum`  | `Integer` | `3000`  | The maximum amount to be bet if `random` is set to `True`. |

### `cooldowns` category

Values in the `cooldowns` category tell the program *the cooldowns for each command* & *cooldowns between commands*. Edit them only if you know what you are doing. You have the most optimal settings by default.

### `custom commands` category

Values in the `custom commands` category tell the program *what custom commands should be run* and *their cooldowns*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | Tells the program whether or not to run any of the custom commands. |

***NOTE:*** You can add your own custom commands by following the layout for the default options.

### `shifts` category

Values in the `shifts` category tell the program *whether or not to run Grank in shifts*, and *the length of active and passive phases*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | Tells the program whether or not to run in shifts. |

#### __Example shifts config__

You can add as many shift configs as you want, so long as you number them in order starting from `1`. The program will infinitely cycle through all the shift configurations.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `active`  | `Integer` | `7200`  | Tells the program how long the program should run before sleeping (in seconds). |
| `passive`  | `Integer` | `3600`  | Tells the program how long the program should sleep before running again (in seconds). |
| `variation`  | `Integer` | `3600`  | Tells the program how much to vary the shifts by. |

### `auto buy` category

Values in the `auto buy` category tell the program whether or not to *buy certain items* if needed.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `True`  | If this is set to `False` no items will be bought. If it is set to `True` the program will try and buy the item if their respective config value is `True`. |
| `shovel`  | `Boolean` | `True`  | Tells the program whether or not to try and buy the item `shovel` if needed and the user doesn't have it. |
| `fishing pole`  | `Boolean` | `True`  | Tells the program whether or not to try and buy the item `fishing pole` if needed and the user doesn't have it. |
| `hunting rifle`  | `Boolean` | `True`  | Tells the program whether or not to try and buy the `hunting rifle` if needed and the user doesn't have it. |
| `keyboard`  | `Boolean` | `True`  | Tells the program whether or not to try and buy the item `keyboard` if needed and the user doesn't have it. |
| `mouse`  | `Boolean` | `True`  | Tells the program whether or not to try and buy the item `mouse` if 
needed and the user doesn't have it. |
| `adventure ticket`  | `Boolean` | `True`  | Tells the program whether or not to try and buy the item `adventure ticket` if needed and the user doesn't have it. |

### `auto trade` category

Values in the `auto trade` category tell the program *who items should be traded to*, and *what items should be traded.*

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | If this is set to `False` no items will be traded. If it is set to `True` the program will try and trade the item if their respective config value is `True`. |
| `trader token`  | `String` | `None`  | The token of the user the items should be traded to. |
| `bank note`  | `Boolean` | `True`  | Tells the program whether or not to try and trade the item `bank note` to the user specified in the `trader` option. |
| `tidepod`  | `Boolean` | `True`  | Tells the program whether or not to try and trade the item `tidepod` to the user specified in the `trader` option. |

***NOTE:*** You can add your own items to be traded by following the layout for the default options.

### `auto accept trade` category

Values in the `anti heist` category tell the program whether or not to *automatically accept trades* and *who to accept them from*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `True`  | Tells the program whether or not to automatically accept trades from other users. |
| `traders`  | `List` | `[0, 0]`  | Tells the program which accounts to automatically accept trades from. |

### `auto sell` category

Values in the `auto sell` category tell the program *what items should be sold (upon receiving them).*

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | If this is set to `False` no items will be sold. If it is set to `False` the program will try and sell the item if their respective config value is `True`. |
| `apple`  | `Boolean` | `True`  | Tells the program whether or not to try and sell the item `apple` (upon receiving it). |
| `common fish`  | `Boolean` | `True`  | Tells the program whether or not to try and sell the item `common fish` (upon receiving it). |

***NOTE:*** You can add your own items to be traded by following the layout for the default options.

### `typing indicator` category

Values in the `typing indicator` category tell the program whether to make Discord think the self-bot is typing, and for how long it should. This is just for aesthetics and I would recommend it to be *off in private servers* to increase command speed, and *on in public servers* to make the self-bot look more legitimate.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | If this is set to `True`, the program will make Discord think the self-bot is typing. If it is set to `False` the program will not make Discord think the self-bot is typing, thus increasing command speed. |
| `minimum`  | `Float` | `0`  | The minimum time for the program to sleep after Discord is told that the user is typing. |
| `maximum`  | `Float` | `0.5`  | The maximum time for the program to sleep after Discord is told that the user is typing. |

### `message delay` category

Values in the `messge delay` category tell the program whether to *add random pauses before sending messages* and *how long the pauses should be for*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | If this is set to `True`, the program will add random pauses before sending messages. |
| `minimum`  | `Float` | `0`  | The minimum time for the program to pause. |
| `maximum`  | `Float` | `0.5`  | The maximum time for the program to pause. |

### `button delay` category

Values in the `button delay` category tell the program whether to *add random pauses before interacting with buttons* and *how long the pauses should be for*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | If this is set to `True`, the program will add random pauses before interacting with buttons. |
| `minimum`  | `Float` | `0`  | The minimum time for the program to pause. |
| `maximum`  | `Float` | `0.5`  | The maximum time for the program to pause. |

### `dropdown delay` category

Values in the `dropdown delay` category tell the program whether to *add random pauses before selecting dropdowns* and *how long the pauses should be for*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | If this is set to `True`, the program will add random pauses before selecting dropdowns. |
| `minimum`  | `Float` | `0`  | The minimum time for the program to pause. |
| `maximum`  | `Float` | `0.5`  | The maximum time for the program to pause. |

### `anti heist` category

Values in the `anti heist` category tell the program whether or not to *automatically avert heists* by *calling the police*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `True`  | Tells the program whether or not to automatically avert heists. |

### `auto join heist` category

Values in the `auto join heist` category tell the program whether or not to *automatically join heists* directed to *other users*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `True`  | Tells the program whether or not to automatically join heists directed to other users. |

### `auto start` category

Values in the `auto start` category tell the program whether or not to *automatically start the grinder* and *which channels to automatically start the grinder in*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | Tells the program whether or not to automatically start the grinder. |
| `channel`  | `Integer` | `0`  | Tells the program which channels to automatically start the grinder in. |

### `blacklisted servers` category

Values in the `blacklisted servers` category tell the program whether or not to *ignore messages from certain servers* and *which servers to ignore the messages from*. The program *ignores commands and events* from blacklisted servers.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `False`  | Tells the program whether or not to ignore messages in the specified channel. |
| `servers`  | `List` | `[0, 0]`  | Tells the program which servers to ingore messages from. |

### `settings` category

Values in the `settings` category *change how the program functions*.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `prefix`  | `List` | `["grank"]`  | A list of prefixes the program should respond to. |
| `patron`  | `Boolean` | `False`  | Changes cooldowns to reflect the cooldowns of `patrons`. |
| `timeout`  | `Integer` | `5`  | Timeout for waiting for responses from Dank Memer to commands that require user interaction (like `pls search`). |

### `events` category
Values in the `events` category the program whether or not to *join events* and *what events* to join.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `Boolean` | `True`  | Tells the program whether or not to respond to events. |
| `attack the boss by clicking disenfect`  | `Boolean` | `True`  | Tells the program whether or not to respond to the `attack the boss by clicking disenfect` event. |
| `windows sucks lol`  | `Boolean` | `True`  | Tells the program whether or not to respond to the `windows sucks lol` event. |
| `why my pls rich no work`  | `Boolean` | `True`  | Tells the program whether or not to respond to the `why my pls rich no work` event. |
| `f`  | `Boolean` | `True`  | Tells the program whether or not to respond to the `f` event. |
| `frick off karen`  | `Boolean` | `True`  | Tells the program whether or not to respond to the `frick off karen` event. |
| `attack the boss by clicking jerk`  | `Boolean` | `True`  | Tells the program whether or not to respond to the `attack the boss by clicking jerk` event. |

### `logging` category

Values in the `logging` category tell the program whether or not to log *`debug`* and *`warning`* messages. We would recommend having *at least* `warning` set to `True`. Fatal errors will be logged regardless of the configuration.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `debug`  | `Boolean` | `True`  | Tells the program whether or not to log `debug` messages. |
| `warning`  | `Boolean` | `True`  | Tells the program whether or not to log `warning` messages. |

***NOTE***: Values in the `logging` category do not affect logging messages sent when the configuration file is being loaded and the token is being verified.

#### __`webhook logging` subcategory__

Values in the `webhook logging` subcategory tell the program whether or not to log events through a webhook and the webhook URL to log through.

| Name  | Type | Default Value | Description |
| ------------- | ------------- | ------------- | ------------- |
| `enabled`  | `True` | `False`  | Tells the program whether or not to log events through a webhook. |
| `url`  | `String` | `discord.com/api/webhooks/`  | The webhook URL to log events through. |

## Disclaimer

This is a self-bot. Self-bots are against Discord's TOS. Automation of Dank Memer commands also breaks Dank Memer's rules. By using this program you acknowledge that I can take no responsibility for actions taken against you if you are caught.

This being said, I believe the chance of being caught running this script is low, provided you take the appropriate measures. The only probable way you will be caught is if someone tries to send you a message and you don't respond.
