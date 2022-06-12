class MessageSendError(Exception):
    pass


class WebhookSendError(Exception):
    pass


class ResponseTimeout(Exception):
    pass


class ButtonInteractError(Exception):
    pass


class DropdownInteractError(Exception):
    pass


class InvalidUserID(Exception):
    pass


class IDNotFound(Exception):
    pass


class ExistingUserID(Exception):
    pass
