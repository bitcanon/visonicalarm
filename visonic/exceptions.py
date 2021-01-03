# define Python user-defined exceptions
class Error(Exception):
    """ Base class for other exceptions """
    pass


class SessionTokenError(Error):
    """ Raised when not authenticated with the REST API. """
    
    def __init__(self, message="Session token not found. Please log in prior to this call."):
        self.message = message
        super().__init__(self.message)


class PermissionDeniedError(Error):
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


class InvalidPanelIDError(Error):
    """ Raised when the Panel ID is not found in the server. """
    
    def __init__(self, message="Invalid Panel ID."):
        self.message = message
        super().__init__(self.message)


class InvalidUserCodeError(Error):
    """ Raised when the user code is not associated with the alarm system. """
    
    def __init__(self, message="Invalid User Code."):
        self.message = message
        super().__init__(self.message)


class LoginAttemptsLimitReachedError(Error):
    """ Raised when the number of failed login attempts are too many. """
    
    def __init__(self, message="Login attempts limit reached. Please wait a few minutes and then try again."):
        self.message = message
        super().__init__(self.message)

