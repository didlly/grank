class MessageSendError(Exception):
    # Failed to send a message
    pass


class WebhookSendError(Exception):
    # Failed to send a webhook
    pass


class ResponseTimeout(Exception):
    # Failed to get Dank Memer's response in the given timeout
    pass


class ButtonInteractError(Exception):
    # Failed to interact with a button on Dank Memer's message
    pass


class DropdownInteractError(Exception):
    # Failed to interact with a dropdown on Dank Memer's message
    pass


class InvalidUserID(Exception):
    # The User ID provided does not follow the correct format
    pass


class IDNotFound(Exception):
    # The User ID provided was not found
    pass


class ExistingUserID(Exception):
    # The User ID provided already exists in the database
    pass
