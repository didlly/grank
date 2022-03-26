def balance(Client) -> dict:
	"""Gets the balance of the user.

	Args:
		Client (class): The Client for the user.

	Returns:
		latest_message (dict): The dictionary version of Dank Memer's message containing the user's balance.
	"""
 
	Client.send_message("pls bal")
  
	return Client.retreive_message("pls bal")