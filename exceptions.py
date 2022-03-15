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
        return "{} --> {}".format(self.message, self.val)


class DoxyException(BaseError):
    """
    exception thrown if the user uses a Doxyfile
    """

    def __init__(self,
                 val,
                 message="Format of Doxyfile contents incorrect. Expecting format: PROJECT_NUMBER= <major>.<minor>.<patch>"):
        super().__init__(val, message)


class PreProcessorException(BaseError):
    """
    exception thrown if the user uses a C header file
    """

    def __init__(self,
                 val,
                 message="Format of C contents incorrect. Expecting format (example): \n#define XXXXX_XXXXX_MAJOR (2U)\n#define XXXXX_XXXXX_MINOR (2U)\n#define XXXXX_XXXXX_PATCH (2U)\n"):
        super().__init__(val, message)


class VersionException(BaseError):
    """
    exception thrown if versions are different across multiple files
    """

    def __init__(self,
                 val,
                 message="Please ensure version numbers across all included files are equal and/or exist...\n"):
        super().__init__(val, message)

class FileNotSupportedException(BaseError):
    """
    exception thrown if file is not implemented in filetypes.py
    """

    def __init__(self,
                 val,
                 message="Filetype not supported. Please implement code for desired filetype."):
        super().__init__(val, message)

        
