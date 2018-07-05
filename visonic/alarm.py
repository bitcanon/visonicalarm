import json
import requests

from time import sleep


class API(object):
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

    def __init__(self, hostname, user_code, user_id, panel_id, partition):
        """ Class constructor initializes all URL variables. """

        # Set connection specific details
        self.__hostname = hostname
        self.__user_code = user_code
        self.__user_id = user_id
        self.__panel_id = panel_id
        self.__partition = partition

        # Visonic API URLs that should be used
        self.__url_base = 'https://' + self.__hostname + '/rest_api/' + self.__rest_version

        self.__url_version = 'https://' + self.__hostname + '/rest_api/version'
        self.__url_is_panel_exists = self.__url_base + '/is_panel_exists?panel_web_name=' + self.__panel_id
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
        self.__url_allow_switch_to_programming_mode = self.__url_base + '/allow_switch_to_programming_mode'

    def __send_get_request(self, url, with_session_token):
        """ Send a GET request to the server. Includes the Session-Token only if with_session_token is True. """

        # Prepare the headers to be sent
        headers = {
            'Host': self.__hostname,
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': self.__user_agent,
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'br, gzip, deflate'
        }

        # Include the session token in the header
        if with_session_token:
            headers['Session-Token'] = self.__session_token

        # Perform the request and raise an exception if the response is not OK (HTML 200)
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        if response.status_code == requests.codes.ok:
            value = json.loads(response.content.decode('utf-8'))
            return value

    def __send_post_request(self, url, data_json, with_session_token):
        """ Send a POST request to the server. Includes the Session-Token only if with_session_token is True. """

        # Prepare the headers to be sent
        headers = {
            'Host': self.__hostname,
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': self.__user_agent,
            'Content-Length': str(len(data_json)),
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'br, gzip, deflate'
        }

        # Include the session token in the header
        if with_session_token:
            headers['Session-Token'] = self.__session_token

        # Perform the request and raise an exception if the response is not OK (HTML 200)
        response = requests.post(url, headers=headers, data=data_json)
        response.raise_for_status()

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
        """ Property to keep track of the session token """
        return self.__session_token

    def get_version_info(self):
        """ Find out which REST API versions are supported """
        return self.__send_get_request(self.__url_version, with_session_token=False)

    def get_panel_exists(self):
        """ Check if our panel exists on the server """
        return self.__send_get_request(self.__url_is_panel_exists, with_session_token=False)

    def login(self):
        """ Try to login and get a session token """
        # Setup authentication information
        login_info = {
            'user_code': self.__user_code,
            'app_type': self.__app_type,
            'user_id': self.__user_id,
            'panel_web_name': self.__panel_id
        }

        login_json = json.dumps(login_info, separators=(',', ':'))
        res = self.__send_post_request(self.__url_login, login_json, with_session_token=False)
        self.__session_token = res['session_token']

    def is_logged_in(self):
        """ Check if the session token is still valid """
        try:
            self.get_status()
            return True
        except requests.HTTPError:
            return False

    def get_status(self):
        """ Get the current status of the alarm system """
        return self.__send_get_request(self.__url_status, with_session_token=True)

    def get_alarms(self):
        """ Get the current alarms """
        return self.__send_get_request(self.__url_alarms, with_session_token=True)

    def get_alerts(self):
        """ Get the current alerts """
        return self.__send_get_request(self.__url_alerts, with_session_token=True)

    def get_troubles(self):
        """ Get the current troubles """
        return self.__send_get_request(self.__url_troubles, with_session_token=True)

    def is_master_user(self):
        """ Check if the current user is a master user """
        ret = self.__send_get_request(self.__url_is_master_user, with_session_token=True)
        return ret['is_master_user']

    def get_general_panel_info(self):
        """ Get the general panel information """
        return self.__send_get_request(self.__url_general_panel_info, with_session_token=True)

    def get_events(self):
        """ Get the alarm panel events """
        return self.__send_get_request(self.__url_events, with_session_token=True)

    def get_wakeup_sms(self):
        """ Get the information needed to send a wakeup SMS to the alarm system """
        return self.__send_get_request(self.__url_wakeup_sms, with_session_token=True)

    def get_all_devices(self):
        """ Get the device specific information """
        return self.__send_get_request(self.__url_all_devices, with_session_token=True)

    def arm_home(self, partition):
        """ Arm in Home mode and with Exit Delay """
        arm_info = {'partition': partition}
        arm_json = json.dumps(arm_info, separators=(',', ':'))
        return self.__send_post_request(self.__url_arm_home, arm_json, with_session_token=True)

    def arm_home_instant(self, partition):
        """ Arm in Home mode and instantly (without Exit Delay) """
        arm_info = {'partition': partition}
        arm_json = json.dumps(arm_info, separators=(',', ':'))
        return self.__send_post_request(self.__url_arm_home_instant, arm_json, with_session_token=True)

    def disarm(self, partition):
        """ Disarm the alarm system """
        disarm_info = {'partition': partition}
        disarm_json = json.dumps(disarm_info, separators=(',', ':'))
        return self.__send_post_request(self.__url_disarm, disarm_json, with_session_token=True)


class Connect(object):
    """ The class that is operating against the Visonic API """

    # Web Client configuration
    __app_type = 'com.visonic.PowerMaxApp'
    __user_agent = 'Visonic-GO/2.6.8 CFNetwork/808.1.4 Darwin/16.1.0'
    __hostname = 'visonic.tycomonitor.com'
    __user_code = '1234'
    __user_id = '00000000-0000-0000-0000-000000000000'
    __panel_id = '123456'
    __partition = 'ALL'

    # Connection settings
    __max_connection_attempts = 20

    # The Visonic API URLs used
    __login_url = None
    __status_url = None
    __arm_away_url = None
    __arm_home_url = None
    __disarm_url = None

    # API session token
    __session_token = None

    def __init__(self, hostname, user_code, user_id, panel_id, partition):
        """ Class constructor """

        # Set connection specific details
        self.__hostname = hostname
        self.__user_code = user_code
        self.__user_id = user_id
        self.__panel_id = panel_id
        self.__partition = partition

        # Visonic API URLs that should be used
        self.__login_url = 'https://' + self.__hostname + '/rest_api/3.0/login'
        self.__status_url = 'https://' + self.__hostname + '/rest_api/3.0/status'
        self.__arm_away_url = 'https://' + self.__hostname + '/rest_api/3.0/arm_away'
        self.__arm_home_url = 'https://' + self.__hostname + '/rest_api/3.0/arm_home'
        self.__disarm_url = 'https://' + self.__hostname + '/rest_api/3.0/disarm'

    def set_faulty_session_token(self):
        self.__session_token = '9559d855-d57d-4650-8ffc-15a6e3721b81'

    def __get_session_token(self):
        """ Retrieve a session token to be used by the other API requests """

        # Setup authentication information
        login_info = {
            'user_code': self.__user_code,
            'app_type': self.__app_type,
            'user_id': self.__user_id,
            'panel_web_name': self.__panel_id
        }

        login_json = json.dumps(login_info, separators=(',', ':'))

        # print(login_json)

        # Header information used by the Visonic App
        api_headers = {
            'Host': self.__hostname,
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'User-Agent': self.__user_agent,
            'Accept-Language': 'en-gb',
            'Content-Length': str(len(login_json))
        }

        # Connect to the API and try to get a session token
        response = requests.post(self.__login_url, headers=api_headers, data=login_json)
        response.raise_for_status()

        # Check HTTP response code
        if response.status_code == requests.codes.ok:
            data = json.loads(response.content.decode('utf-8'))
            session_token = data['session_token']
            return session_token
        else:
            return None

    def __get_status(self):
        """
        Get the current alarm status. This will get the information via the Visonic API and
        simultaneously connect to the Visonic Alarm System in order to get the fresh status.

        The object returned from the server looks something like this:
        {
            'is_connected': True,
            'exit_delay': 30,
            'partitions': [{
               'partition': 'ALL',
               'active': True,
               'state': 'Disarm',
               'ready_status': True
            }]
        }
        """

        # Prepare the header to be send
        status_headers = {
            'Host': self.__hostname,
            'Accept': '*/*',
            'User-Agent': self.__user_agent,
            'Accept-Language': 'en-gb',
            'Session-Token': self.__session_token
        }

        # Alarm status variables we want to populate
        is_connected = False
        is_active = False
        armed_state = 'unknown'
        partition = 'unknown'
        ready_status = False
        exit_delay = 0
        conn_retries = 0

        # Poll the API and wait for the is_connected variable to be True so the
        # Visonic Alarm System is connected to the central servers.
        while conn_retries < self.__max_connection_attempts and is_connected is False:
            conn_retries += 1

            response = requests.get(self.__status_url, headers=status_headers)
            response.raise_for_status()

            if response.status_code == requests.codes.ok:
                data = json.loads(response.content.decode('utf-8'))
                is_connected = data['is_connected']
                exit_delay = data['exit_delay']
                partitions = data['partitions']

                if is_connected:
                    #print('Connected to your Visonic Alarm system! :)')

                    # Current state of the alarm
                    state = partitions[0]['state']
                    if state == 'Disarm':
                        armed_state = 'disarmed'
                    elif state == 'Home':
                        armed_state = 'armed_home'
                    elif state == 'Away':
                        armed_state = 'armed_away'
                    elif state == 'ExitDelayHome':
                        armed_state = 'arming_exit_delay_home'
                    elif state == 'ExitDelayAway':
                        armed_state = 'arming_exit_delay_away'
                    else:
                        armed_state = state

                    # Is the alarm ready to be armed? If False there is probably door
                    # or window sensors that are open
                    ready_status = partitions[0]['ready_status']

                    # The partition reported by the alarm system
                    partition = partitions[0]['partition']

                    # Is the alarm system active
                    is_active = partitions[0]['active']

                    # Dictionary with the alarm state
                    alarm_status = {
                        'state': armed_state,
                        'ready_status': ready_status,
                        'partition': partition,
                        'is_connected': is_connected,
                        'is_active': is_active,
                        'exit_delay': exit_delay,
                        'session_token': self.__session_token
                    }

                    return alarm_status
                else:
                    print('Not yet connected, retrying [{0}]...'.format(conn_retries))
                    sleep(1)
            else:
                # Connection failed and we return an unknown state
                alarm_status = {
                    'state': armed_state,
                    'ready_status': ready_status,
                    'partition': partition,
                    'is_connected': is_connected,
                    'is_active': is_active,
                    'exit_delay': exit_delay,
                    'session_token': self.__session_token
                }

                return alarm_status

    def login(self):
        """ Try to login and get a session token """

        self.__session_token = self.__get_session_token()
        if self.__session_token is None:
            return False
        else:
            return True

    def status(self):
        """ Get the status of the alarm """

        return self.__get_status()
