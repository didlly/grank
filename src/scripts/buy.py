from discord.message import send_message, retreive_message
from utils.logger import log
from json import load

def buy(username, channel_id, token, config, user_id, cwd, item):
    send_message(channel_id, token, config, username, f"pls buy {item}")
    
    latest_message = retreive_message(channel_id, token, config, username, f"pls buy {item}", user_id)

    if latest_message is None:
        return
        
    if latest_message["content"] == "Far out, you don't have enough money in your wallet or your bank to buy that much!!":
        from scripts.balance import balance
        bal = balance(username, channel_id, token, config, log, user_id)
        
        if bal != None:  
            data = load(f"{cwd}/database.json")
            
            bank = int(latest_message["embeds"][0]["description"].split(":")[-1].split(" / ")[0].repalce("⏣", ""))
            wallet = int(latest_message["embeds"][0]["description"].split("\n")[0].split("⏣")[-1])
            
            if (wallet + bank) - data["item"] > 0:
                amount = (wallet + bank) - data["item"]
                
                send_message(channel_id, token, config, username, f"pls with {amount}")                                
                send_message(channel_id, token, config, username, f"pls buy {item}")
            elif config["logging"]["warning"]:
                log(username, "WARNING", f"Insufficient funds to buy a {item}.")  
    elif latest_message[-1]["embeds"][0]["author"]["name"].lower() == f"successful {item} purchase":
        if config["logging"]["debug"]:
            log(username, "DEBUG", f"Successfully bought {item}.")