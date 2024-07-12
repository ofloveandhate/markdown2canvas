class AlreadyExists(Exception):

    def __init__(self, message, errors=""):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        self.errors = errors

class SetupError(Exception):

    def __init__(self, message, errors=""):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        self.errors = errors




class DoesntExist(Exception):
    """
    Used when getting a thing, but it doesn't exist
    """

    def __init__(self, message, errors=""):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        self.errors = errors