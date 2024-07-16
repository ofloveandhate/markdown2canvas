'''
Exception types emitted by markdown2canvas
'''

__all__ = [
    'AlreadyExists',
    'SetupError',
    'DoesntExist'
]

class AlreadyExists(Exception):
    """
    Used to indicate that you're trying to do a thing cautiously, and the thing already existed on Canvas.
    """

    def __init__(self, message, errors=""):
        super().__init__(message)

        self.errors = errors

class SetupError(Exception):
    """
    Used to indicate that markdown2canvas couldn't get off the ground, or there's something else wrong that's not content-related but meta or config.
    """ 

    def __init__(self, message, errors=""):            
        super().__init__(message)
            
        self.errors = errors




class DoesntExist(Exception):
    """
    Used when getting a thing, but it doesn't exist.
    """

    def __init__(self, message, errors=""):            
        super().__init__(message)
            
        self.errors = errors



