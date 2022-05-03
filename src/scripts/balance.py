def balance(Client) -> dict:
    Client.send_message("pls bal")

    return Client.retreive_message("pls bal")
