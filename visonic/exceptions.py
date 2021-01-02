# define Python user-defined exceptions
class Error(Exception):
    """ Base class for other exceptions """
    pass


class SessionTokenError(Error):
    """ Raised when not authenticated with the REST API. """
    
    def __init__(self, message="Session token not found. Please log in prior to this call."):
        self.message = message
        super().__init__(self.message)


class NotAdminError(Error):
    """ Raised when not authenticated with admin credentials. """
    
    def __init__(self, message="Insufficient credentials. Please log in with admin user."):
        self.message = message
        super().__init__(self.message)

