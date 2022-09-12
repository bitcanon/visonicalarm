# define Python user-defined exceptions
class Error(Exception):
    """ Base class for other exceptions """
    pass


class AppIDRequiredError(Error):
    """ Raised when an AppID is not provided in the API calls. """
    def __init__(self, message="Connection to the alarm panel failed because the app ID is missing."):
        self.message = message
        super().__init__(self.message)


class EmailRequiredError(Error):
    """ Raised when the email address is missing in the authentication request. """
    def __init__(self, message="Authentication failed because the email address is missing."):
        self.message = message
        super().__init__(self.message)


class PanelSerialIncorrectError(Error):
    """ Raised when an incorrect panel serial/ID number was provided in the request. """
    def __init__(self, message="Connection to the alarm panel failed because the panel ID is incorrect."):
        self.message = message
        super().__init__(self.message)


class PanelSerialRequiredError(Error):
    """ Raised when a panel serial/ID number was not provided in the request. """
    def __init__(self, message="Connection to the alarm panel failed because the panel ID is missing."):
        self.message = message
        super().__init__(self.message)


class PasswordRequiredError(Error):
    """ Raised when the password is missing in the authentication request. """
    def __init__(self, message="Authentication failed because the password is missing."):
        self.message = message
        super().__init__(self.message)


class UserCodeIncorrectError(Error):
    """ Raised when the user code provided in the request is incorrect. """
    def __init__(self, message="Connection to the alarm panel failed because the user code is incorrect."):
        self.message = message
        super().__init__(self.message)


class UserCodeRequiredError(Error):
    """ Raised when the user code provided in the request was missing. """
    def __init__(self, message="Connection to the alarm panel failed because the user code is missing."):
        self.message = message
        super().__init__(self.message)


class WrongUsernameOrPasswordError(Error):
    """ Raised when the username or password is incorrect. """
    def __init__(self, message="Authentication failed because the wrong username or password was provided."):
        self.message = message
        super().__init__(self.message)


class BadRequestError(Error):
    """ Raised when server returns a 400 Bad Request error. """
    
    def __init__(self, message="Bad Request. Check the connection details and try again.", api_error=None):
        self.message = message
        self.api_error = api_error
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
