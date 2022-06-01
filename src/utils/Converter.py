class DictToClass(object):
    def __init__(self, data: dict) -> None:
        """This __init__ function copies the keys and values in the specified dictionary into the class

        Args:
            data (dict): The dictionary to be converted into a class

        Returns:
            None
        """

        # For each item in data...
        for name, value in data.items():
            # Set its value in this class to what is returned by _wrap(value)
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        # If the value is a tuple, list, set or frozenset...
        if isinstance(value, (tuple, list, set, frozenset)):
            # ...return a recursive call of the function _wrap for every item in value
            return type(value)([self._wrap(v) for v in value])
        # Else...
        else:
            # ...return a recursive call of the class DictToClass if the value is a dictionary, else value
            return DictToClass(value) if isinstance(value, dict) else value
