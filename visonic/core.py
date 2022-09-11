import json
import requests

from datetime import datetime

from visonic.exceptions import *

class APIv9(object):
    """ Class used for communication with the Visonic API """

    # Client configuration
    __app_type = 'com.visonic.PowerMaxApp'
    __user_agent = 'Visonic%20GO/2.8.62.91 CFNetwork/901.1 Darwin/17.6.0'
    __rest_version = '9.0'
    __hostname = 'visonic.tycomonitor.com'
    __user_code = '1234'
    __app_id = '00000000-0000-0000-0000-000000000000'
    __user_email = 'your@email.com'
    __user_password = 'YourSecretPassword!'
    __user_token = None
    __panel_id = '123456'

    # API session token
    __session_token = None

    # Use a session to reuse one TCP connection instead of creating a new
    # connection for every call to the API
    __session = None
    __timeout = 4

    def __init__(self, hostname, user_code, user_id, panel_id, user_email, user_password):
        """ Class constructor initializes all URL variables. """

        # Set connection specific details
        self.__hostname = hostname
        self.__user_code = user_code
        self.__app_id = user_id
        self.__panel_id = panel_id
        self.__user_email = user_email
        self.__user_password = user_password

        # Visonic API URLs that should be used
        self.__url_base = 'https://' + self.__hostname + '/rest_api/' + \
                          self.__rest_version

        self.__url_version = 'https://' + self.__hostname + '/rest_api/version'
        self.__url_auth = self.__url_base + '/auth'
        self.__url_login = self.__url_base + '/panel/login'
        self.__url_status = self.__url_base + '/status'
        self.__url_alarms = self.__url_base + '/alarms'
        self.__url_alerts = self.__url_base + '/alerts'
        self.__url_troubles = self.__url_base + '/troubles'
        self.__url_panel_info = self.__url_base + '/panel_info'
        self.__url_events = self.__url_base + '/events'
        self.__url_devices = self.__url_base + '/devices'
        self.__url_set_state = self.__url_base + '/set_state'
        self.__url_locations = self.__url_base + '/locations'
        self.__url_active_users_info = self.__url_base + '/users'
        self.__url_process_status = self.__url_base + '/process_status?process_tokens='

        # Create a new session
        self.__session = requests.session()

    def __send_request(self, url, with_session_token=True, with_user_token=True, data_json=None, request_type='GET'):
        """ Send a GET or POST request to the server. Includes the Session-Token
        only if with_session_token is True. """

        # Prepare the headers to be sent
        headers = {
            'Host': self.__hostname,
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': self.__user_agent,
            'Accept-Language': 'en-us',
        }

        # Only needed for POST requests
        if request_type == 'POST':
            headers['Content-Type'] = 'application/json'
            headers['Content-Length'] = str(len(data_json))

        # Include the session token in the header
        if with_session_token:
            headers['Session-Token'] = self.__session_token

        # Include the user authentication token in the header
        if with_user_token:
            headers['User-Token'] = self.__user_token

        # Perform the request and raise an exception
        # if the response is not OK (HTML 200)
        try:
            if request_type == 'GET':
                response = self.__session.get(url, headers=headers, timeout=self.__timeout)
            elif request_type == 'POST':
                response = self.__session.post(url, headers=headers, data=data_json, timeout=self.__timeout)
            response.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            raise ConnectionTimeoutError(f"Connection to '{self.__hostname}' timed out after {str(self.__timeout)} seconds.")
            return None
        except requests.exceptions.HTTPError as e:
            if   '400 Client Error: Bad Request' in str(e):
                raise BadRequestError(response.content)
            elif '403 Client Error: Forbidden' in str(e):
                raise PermissionDeniedError()
            elif '404 Client Error: Not Found' in str(e):
                raise NotFoundError()
            elif '440 Client Error: Session token not found' in str(e):
                raise SessionTokenError()
            elif '442 Client Error: Login attempts limit reached' in str(e):
                raise LoginAttemptsLimitReachedError('Login attempts limit reached.')
            elif '444 Client Error: Wrong user code' in str(e):
                raise InvalidUserCodeError('Authentication failed due to wrong user code.')
            else:
                raise

        # Check HTTP response code
        if response.status_code == requests.codes.ok:
            return json.loads(response.content.decode('utf-8'))
        else:
            return None

    ######################
    # Public API methods #
    ######################

    @property
    def session_token(self):
        """ Property to keep track of the session token. """
        return self.__session_token

    @property
    def hostname(self):
        """ Property to keep track of the API servers hostname. """
        return self.__hostname

    @property
    def user_code(self):
        """ Property to keep track of the user code beeing used. """
        return self.__user_code

    @property
    def user_email(self):
        """ Property to keep track of the user email address beeing used. """
        return self.__user_email

    @property
    def user_password(self):
        """ Property to keep track of the user password beeing used. """
        return self.__user_password

    @property
    def user_token(self):
        """ Property to keep track of the user token beeing assigned during authentication. """
        return self.__user_token

    @property
    def app_id(self):
        """ Property to keep track of the user id (UUID) beeing used. """
        return self.__app_id

    @property
    def panel_id(self):
        """ Property to keep track of the panel id (panel web name). """
        return self.__panel_id

    def get_version_info(self):
        """ Find out which REST API versions are supported. """
        return self.__send_request(self.__url_version,
                                       with_session_token=False,
                                       with_user_token=False,
                                       request_type='GET')

    def authenticate(self):
        """ Try to authenticate and get a user auth token. """
        auth_info = {
            'email': self.__user_email,
            'password': self.__user_password,
            'app_id': self.__app_id,
        }

        auth_json = json.dumps(auth_info, separators=(',', ':'))
        res = self.__send_request(self.__url_auth,
                                       with_session_token=False,
                                       with_user_token=False,
                                       data_json=auth_json,
                                       request_type='POST')
        if res is not None:
            self.__user_token = res['user_token']
            return True
        else:
            return False

    def login(self):
        """ Try to login and get a session token. """
        login_info = {
            'user_code': self.__user_code,
            'app_type': self.__app_type,
            'app_id': self.__app_id,
            'panel_serial': self.__panel_id
        }

        login_json = json.dumps(login_info, separators=(',', ':'))
        res = self.__send_request(self.__url_login,
                                       with_session_token=False,
                                       data_json=login_json,
                                       request_type='POST')
        if res is not None:
            self.__session_token = res['session_token']
            return True
        else:
            return False

    def is_logged_in(self):
        """ Check if the session token is still valid. """
        try:
            self.get_status()
            return True
        except requests.HTTPError:
            return False

    def get_active_user_info(self):
        """ Get information about the active users.
        Note: Only master users can see the active_user_ids! """
        return self.__send_request(self.__url_active_users_info, request_type='GET')

    def get_alarms(self):
        """ Get the current alarms. """
        return self.__send_request(self.__url_alarms, request_type='GET')

    def get_alerts(self):
        """ Get the current alerts. """
        return self.__send_request(self.__url_alerts, request_type='GET')

    def get_devices(self):
        """ Get all device specific information. """
        return self.__send_request(self.__url_devices, request_type='GET')

    def get_events(self):
        """ Get the alarm panel events. """
        return self.__send_request(self.__url_events, request_type='GET')

    def get_locations(self):
        """ Get all locations in the alarm system. """
        return self.__send_request(self.__url_locations, request_type='GET')

    def get_panel_info(self):
        """ The general panel information is only supported in version 4.0. """
        return self.__send_request(self.__url_panel_info, request_type='GET')

    def get_panels(self):
        """ Get a list of panels. """
        # send_get('https://larm1.gardaalarm.se/rest_api/9.0/panels')
        raise NotImplementedError()

    def get_process_status(self, process_token):
        """ Get the current status of a process running on API server. """
        url = self.__url_process_status + process_token
        return self.__send_request(url, request_type='GET')

    def get_status(self):
        """ Get the current status of the alarm system. """
        return self.__send_request(self.__url_status, request_type='GET')

    def get_troubles(self):
        """ Get the current troubles. """
        return self.__send_request(self.__url_troubles, request_type='GET')

    def wakeup_sms(self):
        """ Send a wakeup SMS to the alarm panel. """
        # send_get('https://larm1.gardaalarm.se/rest_api/9.0/wakeup_sms')
        raise NotImplementedError()

    def arm_home(self, partition):
        """ Arm in Home mode. """
        arm_info = {'partition': partition, 'state': 'HOME'}
        arm_json = json.dumps(arm_info, separators=(',', ':'))
        return self.__send_request(self.__url_set_state, data_json=arm_json, request_type='POST')

    def arm_away(self, partition):
        """ Arm in Away mode. """
        arm_info = {'partition': partition, 'state': 'AWAY'}
        arm_json = json.dumps(arm_info, separators=(',', ':'))
        return self.__send_request(self.__url_set_state, data_json=arm_json, request_type='POST')

    def disarm(self, partition):
        """ Disarm the alarm system. """
        disarm_info = {'partition': partition, 'state': 'DISARM'}
        disarm_json = json.dumps(disarm_info, separators=(',', ':'))
        return self.__send_request(self.__url_set_state, data_json=disarm_json, request_type='POST')

    def send_get(self, url):
        """ Send a custom POST request. """
        return self.__send_request(url, request_type='GET')

    def send_post(self, url, data):
        """ Send a custom POST request. """
        data_json = json.dumps(data, separators=(',', ':'))
        return self.__send_request(url, data_json=data_json, request_type='POST')
