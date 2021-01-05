import json
import requests

from datetime import datetime

from visonic.exceptions import *


class APIv4(object):
    """ Class used for communication with the Visonic API """

    # Client configuration
    __app_type = 'com.visonic.PowerMaxApp'
    __user_agent = 'Visonic%20GO/2.8.62.91 CFNetwork/901.1 Darwin/17.6.0'
    __rest_version = '4.0'
    __hostname = 'visonic.tycomonitor.com'
    __user_code = '1234'
    __user_id = '00000000-0000-0000-0000-000000000000'
    __panel_id = '123456'
    __partition = 'ALL'

    # The Visonic API URLs used
    __url_base = None
    __url_version = None
    __url_is_panel_exists = None
    __url_login = None
    __url_status = None
    __url_alarms = None
    __url_alerts = None
    __url_troubles = None
    __url_is_master_user = None
    __url_general_panel_info = None
    __url_events = None
    __url_wakeup_sms = None
    __url_all_devices = None
    __url_arm_home = None
    __url_arm_home_instant = None
    __url_arm_away = None
    __url_arm_away_instant = None
    __url_disarm = None
    __url_locations = None
    __url_active_users_info = None
    __url_set_date_time = None
    __url_allow_switch_to_programming_mode = None

    # API session token
    __session_token = None

    # Use a session to reuse one TCP connection instead of creating a new
    # connection for every call to the API
    __session = None
    __timeout = 4

    def __init__(self, hostname, user_code, user_id, panel_id, partition):
        """ Class constructor initializes all URL variables. """

        # Set connection specific details
        self.__hostname = hostname
        self.__user_code = user_code
        self.__user_id = user_id
        self.__panel_id = panel_id
        self.__partition = partition

        # Visonic API URLs that should be used
        self.__url_base = 'https://' + self.__hostname + '/rest_api/' + \
                          self.__rest_version

        self.__url_version = 'https://' + self.__hostname + '/rest_api/version'
        self.__url_is_panel_exists = self.__url_base + \
            '/is_panel_exists?panel_web_name='
        self.__url_login = self.__url_base + '/login'
        self.__url_status = self.__url_base + '/status'
        self.__url_alarms = self.__url_base + '/alarms'
        self.__url_alerts = self.__url_base + '/alerts'
        self.__url_troubles = self.__url_base + '/troubles'
        self.__url_is_master_user = self.__url_base + '/is_master_user'
        self.__url_general_panel_info = self.__url_base + '/general_panel_info'
        self.__url_events = self.__url_base + '/events'
        self.__url_wakeup_sms = self.__url_base + '/wakeup_sms'
        self.__url_all_devices = self.__url_base + '/all_devices'
        self.__url_arm_home = self.__url_base + '/arm_home'
        self.__url_arm_home_instant = self.__url_base + '/arm_home_instant'
        self.__url_arm_away = self.__url_base + '/arm_away'
        self.__url_arm_away_instant = self.__url_base + '/arm_away_instant'
        self.__url_disarm = self.__url_base + '/disarm'
        self.__url_locations = self.__url_base + '/locations'
        self.__url_active_users_info = self.__url_base + '/active_users_info'
        self.__url_set_date_time = self.__url_base + '/set_date_time'
        self.__url_allow_switch_to_programming_mode = self.__url_base + \
            '/allow_switch_to_programming_mode'

        # Create a new session
        self.__session = requests.session()

    def __send_request(self, url, with_session_token, data_json=None, request_type='GET'):
        """ Send a GET or POST request to the server. Includes the Session-Token
        only if with_session_token is True. """

        # Prepare the headers to be sent
        headers = {
            'Host': self.__hostname,
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': self.__user_agent,
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'br, gzip, deflate',
        }

        # Only needed for POST requests
        if request_type == 'POST':
            headers['Content-Type'] = 'application/json'
            headers['Content-Length'] = str(len(data_json))

        # Include the session token in the header
        if with_session_token:
            headers['Session-Token'] = self.__session_token

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
            if   '403 Client Error: Forbidden' in str(e):
                raise PermissionDeniedError()
            elif '404 Client Error: Not Found' in str(e):
                raise NotRestAPIError('Unable to retrieve supported Rest API versions from server.')
            elif '440 Client Error: Session token not found' in str(e):
                raise SessionTokenError()
            elif '442 Client Error: Login attempts limit reached' in str(e):
                raise LoginAttemptsLimitReachedError('Login attempts limit reached.')
            elif '444 Client Error: Wrong user code' in str(e):
                raise InvalidUserCodeError('Authentication failed due to wrong user code.')

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
    def user_id(self):
        """ Property to keep track of the user id (UUID) beeing used. """
        return self.__user_id

    @property
    def panel_id(self):
        """ Property to keep track of the panel id (panel web name). """
        return self.__panel_id

    @property
    def partition(self):
        """ Property to keep track of the partition. """
        return self.__partition

    def get_version_info(self):
        """ Find out which REST API versions are supported. """
        return self.__send_request(self.__url_version,
                                       with_session_token=False,
                                       request_type='GET')

    def get_panel_exists(self, panel_id):
        """ Check if our panel exists on the server. """
        return self.__send_request(self.__url_is_panel_exists + panel_id,
                                       with_session_token=False,
                                       request_type='GET')

    def login(self):
        """ Try to login and get a session token. """
        # Setup authentication information
        login_info = {
            'user_code': self.__user_code,
            'app_type': self.__app_type,
            'user_id': self.__user_id,
            'panel_web_name': self.__panel_id
        }

        login_json = json.dumps(login_info, separators=(',', ':'))
        res = self.__send_request(self.__url_login,
                                       with_session_token=False,
                                       data_json=login_json,
                                       request_type='POST')
        self.__session_token = res['session_token']

    def is_logged_in(self):
        """ Check if the session token is still valid. """
        try:
            self.get_status()
            return True
        except requests.HTTPError:
            return False

    def get_status(self):
        """ Get the current status of the alarm system. """
        return self.__send_request(self.__url_status,
                                       with_session_token=True,
                                       request_type='GET')

    def get_alarms(self):
        """ Get the current alarms. """
        return self.__send_request(self.__url_alarms,
                                       with_session_token=True,
                                       request_type='GET')

    def get_alerts(self):
        """ Get the current alerts. """
        return self.__send_request(self.__url_alerts,
                                       with_session_token=True,
                                       request_type='GET')

    def get_troubles(self):
        """ Get the current troubles. """
        return self.__send_request(self.__url_troubles,
                                       with_session_token=True,
                                       request_type='GET')

    def is_master_user(self):
        """ Check if the current user is a master user. """
        ret = self.__send_request(self.__url_is_master_user,
                                      with_session_token=True,
                                      request_type='GET')
        return ret['is_master_user']

    def get_general_panel_info(self):
        """ Get the general panel information. """
        return self.__send_request(self.__url_general_panel_info,
                                       with_session_token=True,
                                       request_type='GET')

    def get_events(self):
        """ Get the alarm panel events. """
        return self.__send_request(self.__url_events,
                                       with_session_token=True,
                                       request_type='GET')

    def get_wakeup_sms(self):
        """ Get the information needed to send a
        wakeup SMS to the alarm system. """
        return self.__send_request(self.__url_wakeup_sms,
                                       with_session_token=True,
                                       request_type='GET')

    def get_all_devices(self):
        """ Get the device specific information. """
        return self.__send_request(self.__url_all_devices,
                                       with_session_token=True,
                                       request_type='GET')

    def get_locations(self):
        """ Get all locations in the alarm system. """
        return self.__send_request(self.__url_locations,
                                       with_session_token=True,
                                       request_type='GET')

    def get_active_user_info(self):
        """ Get information about the active users.
        Note: Only master users can see the active_user_ids! """
        return self.__send_request(self.__url_active_users_info,
                                       with_session_token=True,
                                       request_type='GET')

    def set_date_time(self, current_time):
        """ Set the time on the alarm panel.
        Note: Only master users can set the time! """

        # Make sure the time has the correct format: 20180704T185700
        set_time = current_time.isoformat().replace(':', '').replace('.',
                                                    '').replace('-', '')[:15]

        time_info = {'time': set_time}
        time_json = json.dumps(time_info, separators=(',', ':'))
        return self.__send_request(self.__url_set_date_time,
                                        with_session_token=True,
                                        data_json=time_json,
                                        request_type='POST')

    def arm_home(self, partition):
        """ Arm in Home mode and with Exit Delay. """
        arm_info = {'partition': partition}
        arm_json = json.dumps(arm_info, separators=(',', ':'))
        return self.__send_request(self.__url_arm_home,
                                        with_session_token=True,
                                        data_json=arm_json,
                                        request_type='POST')

    def arm_home_instant(self, partition):
        """ Arm in Home mode instantly (without Exit Delay). """
        arm_info = {'partition': partition}
        arm_json = json.dumps(arm_info, separators=(',', ':'))
        return self.__send_request(self.__url_arm_home_instant,
                                        with_session_token=True,
                                        data_json=arm_json,
                                        request_type='POST')

    def arm_away(self, partition):
        """ Arm in Away mode and with Exit Delay. """
        arm_info = {'partition': partition}
        arm_json = json.dumps(arm_info, separators=(',', ':'))
        return self.__send_request(self.__url_arm_away,
                                        with_session_token=True,
                                        data_json=arm_json,
                                        request_type='POST')

    def arm_away_instant(self, partition):
        """ Arm in Away mode instantly (without Exit Delay). """
        arm_info = {'partition': partition}
        arm_json = json.dumps(arm_info, separators=(',', ':'))
        return self.__send_request(self.__url_arm_away_instant,
                                        with_session_token=True,
                                        data_json=arm_json,
                                        request_type='POST')

    def disarm(self, partition):
        """ Disarm the alarm system. """
        disarm_info = {'partition': partition}
        disarm_json = json.dumps(disarm_info, separators=(',', ':'))
        return self.__send_request(self.__url_disarm,
                                        with_session_token=True,
                                        data_json=disarm_json,
                                        request_type='POST')
