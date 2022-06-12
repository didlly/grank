# Welcome to Grank

[![Stargazers](https://img.shields.io/github/stars/didlly/grank?style=for-the-badge&logo=Python&color=blue)](https://github.com/didlly/grank/stargazers)
[![Forks](https://img.shields.io/github/forks/didlly/grank?style=for-the-badge&logo=Python&color=blue)](https://github.com/didlly/grank/network/members)
[![Issues](https://img.shields.io/github/issues/didlly/grank?style=for-the-badge&logo=Python&color=informational)](https://github.com/didlly/grank/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/didlly/grank?style=for-the-badge&logo=Python&color=informational)](https://github.com/didlly/grank/pulls)

Grank is a feature rich Dank Memer automation program that is open-source and free to use, as well as having many self-bot commands to make using Grank easier. Grank is inspired by [dankgrinder](https://github.com/dankgrinder/dankgrinder). Since dankgrinder has been discontinued and the [recommended fork](https://github.com/V4NSH4J/dankgrinder) has also been discontinued, I decided to make my own version from scratch in Python. Grank is as good as, if not better, than dankgrinder.

## Choose your docs:
Choose the docs you would like to view, or stay on this page for more information on why & how Grank was created.

### User
Click [here](/grank/users) to proceed to the user documentation. This includes details on how to set-up Grank.

## Why was Grank created
Back in early January of 2022, me and my friends started grinding out Dank Memer as a fun past-time to see who could make the most money / networth. For the first half of January, I grinded Dank Memer legitimately, but then realised how easy it would be to automate it.

My first attempt at a grinder for Dank Memer was really bad - it was a simple hotkey script created using AHK and, understandably, could only run when Discord was the open window. This made it extremely inefficient. After searching around on the internet for a better way to automate Dank Memer, I came across [dankgrinder](https://github.com/dankgrinder/dankgrinder). It seems I came a bit late to the party, since both it and the [recommended fork](https://github.com/V4NSH4J/dankgrinder) were discontinued by the time I found them. Nevertheless, the recommended fork still functioned as it was meant to.

I quickly realised thought, that while there was still a chance of the fork getting developed on once more, the chances were slim since V4NSH4J was moving towards other projects, at that time namely [DMDGO](https://github.com/V4NSH4J/discord-mass-DM-GO). I decided to put my skills to the test by trying to make my own version in Python which, needless to say, has been gaining traction increasingly in the past few months.

And now, I can flex to my friends about having 100x the money they have while they fail to work out how to setup the script ;-) (it's really easy idk why they can't lol).

## How does Grank work
Before I get into exactly how Grank works, I would like to give a huge thanks to [V4NSH4J](https://github.com/V4NSH4J/). They're the creator of the now unsupported dankgrinder fork, and without them Grank may never have been completed.

Everything on the internet is request based. You search for something on Google - you send request(s) to Google. You watch your [favourite YouTube video](https://www.youtube.com/watch?v=dQw4w9WgXcQ) - you send request(s) to YouTube. And specifically for us, you send a message on Discord - you send request(s) to Discord.

What I'm trying to say is that everything you do is based on requests, so if you mimic those requests yourself, you can easily automate the action. If you send a message on Discord, and use the `Network` tab in the `Inspect` screen, you can see a `POST` request to `https://discord.com/api/v10/channels/{channel-id}.` Grank mimics those requests, as can be seen in the various subprograms of the class `Instance` in `/src/instance/Client.py`. After that, it's just a game of learning your opponent (in our case Dank Memer), and working out the most optimal ways to respond to them.

Grank does not use any Discord self-bot library, since I wanted to code my own for maximum flexibility (as can be seen in `/src/discord/Gateway.py` & `/src/instance/Client.py`), and so the [Discord Developer Docs](https://discord.com/developers/docs) (intended for bot creators, not self-bot creators) were (ironically) a great help in working out how to automate the commands.

## Developers
### Sole Developer
[ME] - [didlly](https://github.com/didlly)

### Contributors
[SXVXGE](https://github.com/SXVXGEE) - Contributing code to the trivia scraper & contributing to the database.

### Helpers
[V4NSH4J](https://github.com/V4NSH4J/) - Helping me with undestanding Discord's docs & answering all my questions without getting tired of the continual stream of questions ;-).

<hr>

[![Stargazers repo roster for @didlly/grank](https://reporoster.com/stars/dark/didlly/grank)](https://github.com/didlly/grank/stargazers)

[![Forkers repo roster for @didlly/grank](https://reporoster.com/forks/dark/didlly/grank)](https://github.com/didlly/grank/network/members)