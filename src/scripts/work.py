def work(Client) -> None:
    Client.send_message("pls work")
    
    latest_message = Client.retreive_message("pls work")
    
    if "You don't currently have a job to work at." in latest_message["content"]:
        Client.send_message("pls work list")
        
        latest_message = Client.retreive_message("pls work list")
        
        for job in latest_message["embeds"][0]["fields"]:
            pass
        
            # Will finish later today (hopefully).