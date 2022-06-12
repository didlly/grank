class DictToClass(object):
    def __init__(self, data: dict) -> None:
        """This __init__ function copies the keys and values in the specified dictionary into the class

        Args:
            data (dict): The dictionary to be converted into a class

        Returns:
            None
        """

        for name, value in data.items():
            setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return DictToClass(value) if isinstance(value, dict) else value
