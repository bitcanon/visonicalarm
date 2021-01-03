# define Python user-defined exceptions
class Error(Exception):
    """ Base class for other exceptions """
    pass


class SessionTokenError(Error):
    """ Raised when not authenticated with the REST API. """
    
    def __init__(self, message="Session token not found. Please log in prior to this call."):
        self.message = message
        super().__init__(self.message)


class NotMasterError(Error):
    """ Raised when not authenticated with master credentials. """
    
    def __init__(self, message="Insufficient credentials. Please connect with master user."):
        self.message = message
        super().__init__(self.message)


class ConnectionTimeoutError(Error):
    """ Raised when connection to the REST API Server timed out. """
    
    def __init__(self, message="Connection to host timed out."):
        self.message = message
        super().__init__(self.message)


class NotRestAPIError(Error):
    """ Raised when connection to server is not a Rest API. """
    
    def __init__(self, message="Connection to host timed out."):
        self.message = message
        super().__init__(self.message)


class UnsupportedRestAPIVersionError(Error):
    """ Raised when a version of the REST API is unsupported. """
    
    def __init__(self, message="Unsupported REST API version."):
        self.message = message
        super().__init__(self.message)
