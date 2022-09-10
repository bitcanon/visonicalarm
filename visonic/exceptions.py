# define Python user-defined exceptions
class Error(Exception):
    """ Base class for other exceptions """
    pass


class AuthenticationFailedError(Error):
    """ Raised when username or password are incorrect. """
    
    def __init__(self, message="Authentication failed. Please check the username and password."):
        self.message = message
        super().__init__(self.message)


class BadRequestError(Error):
    """ Raised when server returns a 400 Bad Request error. """
    
    def __init__(self, message="Bad Request. Check the connection details and try again."):
        self.message = message
        super().__init__(self.message)


class ConnectionTimeoutError(Error):
    """ Raised when connection to the REST API Server timed out. """
    
    def __init__(self, message="Connection to host timed out."):
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


class LoginFailedError(Error):
    """ Raised when the login attempt failed. """
    
    def __init__(self, message="Login attempts failed. Please check the settings and try again. Make sure to use the master code."):
        self.message = message
        super().__init__(self.message)


class NotFoundError(Error):
    """ Raised when an API endpoint is not found. """
    
    def __init__(self, message="The API endpoint was not found on the server."):
        self.message = message
        super().__init__(self.message)


class NotImplementedError(Error):
    """ Raised when a method is called that is not implemented yet. """

    def __init__(self, message="The method called has not yet been implemented."):
        self.message = message
        super().__init__(self.message)


class NotRestAPIError(Error):
    """ Raised when connection to server is not a Rest API. """
    
    def __init__(self, message="Connection to host timed out."):
        self.message = message
        super().__init__(self.message)


class NotSupportedError(Error):
    """ Raised when trying to call a method not supported in the current API version. """
    
    def __init__(self, message="Method is not supported in the selected version of the API."):
        self.message = message
        super().__init__(self.message)


class PermissionDeniedError(Error):
    """ Raised when not authenticated with master credentials. """
    
    def __init__(self, message="Insufficient credentials. Please connect with master user."):
        self.message = message
        super().__init__(self.message)


class SessionTokenError(Error):
    """ Raised when not authenticated with the REST API. """
    
    def __init__(self, message="Session token not found. Please log in prior to this call."):
        self.message = message
        super().__init__(self.message)


class UnsupportedRestAPIVersionError(Error):
    """ Raised when a version of the REST API is unsupported. """
    
    def __init__(self, message="Unsupported REST API version."):
        self.message = message
        super().__init__(self.message)
