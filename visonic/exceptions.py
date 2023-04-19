# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""

    pass


class AlreadyGrantedError(Error):
    """Raised when trying to grant access to a user that has already been granted access."""

    def __init__(self, message="The user has already been granted access."):
        self.message = message
        super().__init__(self.message)


class AlreadyLinkedError(Error):
    """Raised when trying grant an already linked email address."""

    def __init__(self, message="The email address has already been linked to a user."):
        self.message = message
        super().__init__(self.message)


class AppIDRequiredError(Error):
    """Raised when an AppID is not provided in the API calls."""

    def __init__(
        self,
        message="Connection to the alarm panel failed because the app ID is missing.",
    ):
        self.message = message
        super().__init__(self.message)


class EmailRequiredError(Error):
    """Raised when the email address is missing in the authentication request."""

    def __init__(
        self, message="Authentication failed because the email address is missing."
    ):
        self.message = message
        super().__init__(self.message)


class LoginTemporaryBlockedError(Error):
    """Raised when the password is missing in the authentication request."""

    def __init__(
        self,
        message="Login is temporary blocked due to too many failed login attempts.",
    ):
        self.message = message
        super().__init__(self.message)


class NewPasswordStrengthError(Error):
    """Raised when the password is missing in the authentication request."""

    def __init__(
        self,
        message="New password is not strong enough. Please enter a complex password containing letters, digits and special characters.",
    ):
        self.message = message
        super().__init__(self.message)


class NotAllowedError(Error):
    """Raised when the request is not allowed."""

    def __init__(self, message="The request is not allowed."):
        self.message = message
        super().__init__(self.message)


class PanelNotConnectedError(Error):
    """Raised when the API server is not connected to the alarm panel."""

    def __init__(self, message="Alarm panel is not connected to the API server."):
        self.message = message
        super().__init__(self.message)


class PanelSerialIncorrectError(Error):
    """Raised when an incorrect panel serial/ID number was provided in the request."""

    def __init__(
        self,
        message="Connection to the alarm panel failed because the panel ID is incorrect.",
    ):
        self.message = message
        super().__init__(self.message)


class PanelSerialRequiredError(Error):
    """Raised when a panel serial/ID number was not provided in the request."""

    def __init__(
        self,
        message="Connection to the alarm panel failed because the panel ID is missing.",
    ):
        self.message = message
        super().__init__(self.message)


class PasswordRequiredError(Error):
    """Raised when the password is missing in the authentication request."""

    def __init__(self, message="Request failed because the password is missing."):
        self.message = message
        super().__init__(self.message)


class ResetPasswordCodeIncorrectError(Error):
    """Raised when the password reset code obtained via email is incorrect."""

    def __init__(
        self,
        message="Reset password code is incorrect. Check you email or try to resend the password reset request.",
    ):
        self.message = message
        super().__init__(self.message)


class UndefinedBadRequestError(Error):
    """Raised when an undefined 400 Bad Request error occurs."""

    def __init__(
        self, message="Bad Request. Check the connection details and try again."
    ):
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(Error):
    """Raised when a 401 Client Error occurs."""

    def __init__(self, message="Unauthorized to access API endpoint."):
        self.message = message
        super().__init__(self.message)


class UndefinedForbiddenError(Error):
    """Raised when an undefined 403 Client Error occurs."""

    def __init__(self, message="The request is forbidden."):
        self.message = message
        super().__init__(self.message)


class UserAuthRequiredError(Error):
    """Raised when a forbidden error occurs due to not being authenticated."""

    def __init__(self, message="User authentication required."):
        self.message = message
        super().__init__(self.message)


class UserCodeIncorrectError(Error):
    """Raised when the user code provided in the request is incorrect."""

    def __init__(
        self,
        message="Connection to the alarm panel failed because the user code is incorrect.",
    ):
        self.message = message
        super().__init__(self.message)


class UserCodeRequiredError(Error):
    """Raised when the user code provided in the request was missing."""

    def __init__(
        self,
        message="Connection to the alarm panel failed because the user code is missing.",
    ):
        self.message = message
        super().__init__(self.message)


class WrongUsernameOrPasswordError(Error):
    """Raised when the username or password is incorrect."""

    def __init__(
        self,
        message="Authentication failed because the wrong username or password was provided.",
    ):
        self.message = message
        super().__init__(self.message)


class WrongPanelSerialOrMasterUserCodeError(Error):
    """Raised when the panel serial or master user code is incorrect."""

    def __init__(
        self,
        message="The wrong combination of panel serial and/or master user code was provided.",
    ):
        self.message = message
        super().__init__(self.message)


class ConnectionTimeoutError(Error):
    """Raised when connection to the REST API Server timed out."""

    def __init__(self, message="Connection to host timed out."):
        self.message = message
        super().__init__(self.message)


class InvalidPanelIDError(Error):
    """Raised when the Panel ID is not found in the server."""

    def __init__(self, message="Invalid Panel ID."):
        self.message = message
        super().__init__(self.message)


class InvalidUserCodeError(Error):
    """Raised when the user code is not associated with the alarm system."""

    def __init__(self, message="Invalid User Code."):
        self.message = message
        super().__init__(self.message)


class LoginAttemptsLimitReachedError(Error):
    """Raised when the number of failed login attempts are too many."""

    def __init__(
        self,
        message="Login attempts limit reached. Please wait a few minutes and then try again.",
    ):
        self.message = message
        super().__init__(self.message)


class LoginFailedError(Error):
    """Raised when the login attempt failed."""

    def __init__(
        self,
        message="Login attempts failed. Please check the settings and try again. Make sure to use the master code.",
    ):
        self.message = message
        super().__init__(self.message)


class NotFoundError(Error):
    """Raised when an API endpoint is not found."""

    def __init__(self, message="The API endpoint was not found on the server."):
        self.message = message
        super().__init__(self.message)


class NotImplementedError(Error):
    """Raised when a method is called that is not implemented yet."""

    def __init__(self, message="The method called has not yet been implemented."):
        self.message = message
        super().__init__(self.message)


class NotRestAPIError(Error):
    """Raised when connection to server is not a Rest API."""

    def __init__(self, message="Connection to host timed out."):
        self.message = message
        super().__init__(self.message)


class NotSupportedError(Error):
    """Raised when trying to call a method not supported in the current API version."""

    def __init__(
        self, message="Method is not supported in the selected version of the API."
    ):
        self.message = message
        super().__init__(self.message)


class SessionTokenError(Error):
    """Raised when not authenticated with the REST API."""

    def __init__(
        self, message="Session token not found. Please log in prior to this call."
    ):
        self.message = message
        super().__init__(self.message)


class UnsupportedRestAPIVersionError(Error):
    """Raised when a version of the REST API is unsupported."""

    def __init__(self, message="Unsupported REST API version."):
        self.message = message
        super().__init__(self.message)
