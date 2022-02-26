from utils.yaml import load
from utils.logger import log

def load_config(cwd):
    config = load(f"{cwd}/config.yml")

    options = ["['commands']", "['commands']['daily']", "['commands']['beg']", "['commands']['fish']", "['commands']['hunt']", "['commands']['dig']", "['commands']['search']", "['commands']['highlow']", "['commands']['postmeme']", "['commands']['trivia']", "['auto_buy']", "['auto_buy']['enabled']", "['auto_buy']['laptop']", "['auto_buy']['shovel']", "['auto_buy']['fishing pole']", "['auto_buy']['hunting rifle']", "['auto_trade']", "['auto_trade']['enabled']", "['auto_trade']['trader']", "['cooldowns']", "['cooldowns']['patron']", "['cooldowns']['timeout']", "['logging']['debug']", "['logging']['warning']"]

    for option in options:
        try:
            exec(f"_ = config{option}")
        except KeyError:
            log(None, "ERROR", f"Unable to find configuration option for `{option}`. Make sure it is present.")

    return config