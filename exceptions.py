class BaseError(Exception):
    """
    base error structure class
    """
    def __init__(self, val, message):
        """
        @param val: actual value
        @param message: message shown to the user
        """
        self.val = val
        self.message = message
        super().__init__()

    def __str__(self):
        return "{} --> {}".format(self.val, self.message)


class DoxyException(BaseError):
    """
    exception thrown if the user uses a Doxyfile
    """
    def __init__(self, val, message="Not a C-language file, defaulting to Doxyfile..."):
        super().__init__(val, message)
