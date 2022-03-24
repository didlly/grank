def balance(Client):
	request = Client.send_message("pls bal")

	if request is False:
		return None
	  
	return Client.retreive_message("pls bal")