import json
import requests

from datetime import datetime

from visonic.exceptions import *

class API(object):
    """ Class used for communication with the Visonic API """

    # Client configuration
    __app_type = 'com.visonic.powermaxapp'
    __user_agent = 'Dart/2.10 (dart:io)'
    __rest_version = '9.0'

    # API tokens
    __user_token = None
    __session_token = None

    # Use a session to reuse one TCP connection instead of creating a new
    # connection for every call to the API
    __session = None
    __timeout = 4

    def __init__(self, hostname, app_id):
        """ Class constructor initializes all URL variables. """

        # Set connection specific details
        self.__hostname = hostname
        self.__app_id = app_id

        self.render_urls()

        # Create a new session
        self.__session = requests.session()

    def render_urls(self):
        """ Configure the API endpoints. """
        self.__url_base = 'https://' + self.__hostname + '/rest_api/' + self.__rest_version
        self.__url_version = 'https://' + self.__hostname + '/rest_api/version'

        # API endpoints
        self.__url_access_grant             = self.__url_base + '/access/grant'
        self.__url_access_revoke            = self.__url_base + '/access/revoke'
        self.__url_activate_siren           = self.__url_base + '/activate_siren'
        self.__url_alarms                   = self.__url_base + '/alarms'
        self.__url_alerts                   = self.__url_base + '/alerts'
        self.__url_auth                     = self.__url_base + '/auth'
        self.__url_cameras                  = self.__url_base + '/cameras'
        self.__url_devices                  = self.__url_base + '/devices'
        self.__url_disable_siren            = self.__url_base + '/disable_siren'
        self.__url_events                   = self.__url_base + '/events'
        self.__url_feature_set              = self.__url_base + '/feature_set'
        self.__url_locations                = self.__url_base + '/locations'
        self.__url_notifications_email      = self.__url_base + '/notifications/email'
        self.__url_panel_login              = self.__url_base + '/panel/login'
        self.__url_panel_info               = self.__url_base + '/panel_info'
        self.__url_panel_add                = self.__url_base + '/panel/add'
        self.__url_panel_rename             = self.__url_base + '/panel/rename'
        self.__url_panel_unlink             = self.__url_base + '/panel/unlink'
        self.__url_panels                   = self.__url_base + '/panels'
        self.__url_password_reset           = self.__url_base + '/password/reset'
        self.__url_password_reset_complete  = self.__url_base + '/password/reset/complete'
        self.__url_process_status           = self.__url_base + '/process_status?process_tokens='
        self.__url_set_bypass_zone          = self.__url_base + '/set_bypass_zone'
        self.__url_set_name                 = self.__url_base + '/set_name'
        self.__url_set_state                = self.__url_base + '/set_state'
        self.__url_set_user_code            = self.__url_base + '/set_user_code'
        self.__url_smart_devices            = self.__url_base + '/smart_devices'
        self.__url_smart_devices_settings   = self.__url_base + '/smart_devices/settings'
        self.__url_status                   = self.__url_base + '/status'
        self.__url_troubles                 = self.__url_base + '/troubles'
        self.__url_users                    = self.__url_base + '/users'
        self.__url_wakeup_sms               = self.__url_base + '/wakeup_sms'

        # To be implemented

        # Will not be implemented
        self.__url_apptype                  = self.__url_base + '/apptype'
        self.__url_home_automation_devices  = self.__url_base + '/home_automation_devices'
        self.__url_make_video               = self.__url_base + '/make_video'

    def set_rest_version(self, version):
        """ Set which version to use when connection to the API. """
        self.__rest_version = version
        self.render_urls()

    def __raise_on_bad_request(self, error):
        """ Raise an exception when the API returns a bad request. """
        api = json.loads(error.decode('utf-8'))
        print(api)

        if api['error'] == 10001: # BadRequestParams
            for pair in api['extras']:
                if pair['value'] == 'incorrect':
                    if pair['key'] == 'panel_serial':
                        raise PanelSerialIncorrectError()
                    elif pair['key'] == 'reset_password_code':
                        raise ResetPasswordCodeIncorrectError()
                if pair['value'] == 'required':
                    if pair['key'] == 'panel_serial':
                        raise PanelSerialRequiredError()
                    elif pair['key'] == 'email':
                        raise EmailRequiredError()
                    elif pair['key'] == 'password':
                        raise PasswordRequiredError()
                    elif pair['key'] == 'app_id':
                        raise AppIDRequiredError()
                    elif pair['key'] == 'user_code':
                        raise UserCodeRequiredError()
                    elif pair['key'] == 'new_password':
                        raise PasswordRequiredError()
                if pair['value'] == 'already_granted':
                    raise AlreadyGrantedError()
                if pair['value'] == 'already_linked':
                    raise AlreadyLinkedError()
                if pair['key'] == 'new_password':
                    raise NewPasswordStrengthError()
        elif api['error'] == 10004: # WrongCombination
            for pair in api['extras']:
                if pair['value'] == 'wrong_combination':
                    if pair['key'] == 'email' or pair['key'] == 'password':
                        raise WrongUsernameOrPasswordError()
                    if pair['key'] == 'panel_serial' or pair['key'] == 'master_user_code':
                        raise WrongPanelSerialOrMasterUserCodeError()
        elif api['error'] == 10021: # WrongUserCode
            raise UserCodeIncorrectError()
        elif api['error'] == 400 and api['error_reason_code'] == 'PanelNotConnected':
            raise PanelNotConnectedError()

        # Raise a generic error when the library has no
        # specific exception implemented yet.
        raise UndefinedBadRequestError(str(api))

    def __raise_on_forbidden(self, error):
        """ Raise an exception when the API returns a forbidden error. """
        api = json.loads(error.decode('utf-8'))
        print(api)

        if api['error'] == 10010: # NotAllowed
            raise NotAllowedError()

        # Raise a generic error when the library has no
        # specific exception implemented yet.
        raise UndefinedForbiddenError(str(api))

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
            'Accept-Encoding': 'gzip',
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
            api = json.loads(response.content.decode('utf-8'))
            print(api)
            if   '400 Client Error: Bad Request' in str(e):
                self.__raise_on_bad_request(response.content)
            elif '403 Client Error: Forbidden' in str(e):
                self.__raise_on_forbidden(response.content)
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
    def user_token(self):
        """ Property to keep track of the user token beeing assigned during authentication. """
        return self.__user_token

    @property
    def app_id(self):
        """ Property to keep track of the user id (UUID) beeing used. """
        return self.__app_id

    def get_version_info(self):
        """ Find out which REST API versions are supported. """
        return self.__send_request(self.__url_version,
                                       with_session_token=False,
                                       with_user_token=False,
                                       request_type='GET')

    def authenticate(self, email, password):
        """ Try to authenticate and get a user auth token. """
        auth_info = {
            'email': email,
            'password': password,
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

    def is_logged_in(self):
        """ Check if the session token is still valid. """
        try:
            self.get_status()
            return True
        except requests.HTTPError:
            return False

    def access_grant(self, user_id, email):
        """ Grant a user access to the alarm panel via the API. """
        user_data = {'user': user_id, 'email': email}
        user_json = json.dumps(user_data, separators=(',', ':'))
        return self.__send_request(self.__url_access_grant, data_json=user_json, request_type='POST')

    def access_revoke(self, user_id):
        """ Revoke access to the alarm panel via the API for a user. """
        user_data = {'user': user_id}
        user_json = json.dumps(user_data, separators=(',', ':'))
        return self.__send_request(self.__url_access_revoke, data_json=user_json, request_type='POST')

    def activate_siren(self):
        """ Activate the siren (sound the alarm). """
        siren_data = {}
        siren_json = json.dumps(siren_data, separators=(',', ':'))
        return self.__send_request(self.__url_activate_siren, data_json=siren_json, request_type='POST')

    def disable_siren(self, mode):
        """ Disable the siren (mute the alarm). """
        siren_data = {'mode': mode}
        siren_json = json.dumps(siren_data, separators=(',', ':'))
        return self.__send_request(self.__url_disable_siren, data_json=siren_json, request_type='POST')

    def get_alarms(self):
        """ Get the current alarms. """
        return self.__send_request(self.__url_alarms, request_type='GET')

    def get_alerts(self):
        """ Get the current alerts. """
        return self.__send_request(self.__url_alerts, request_type='GET')

    def get_cameras(self):
        """ Get the cameras in the system. """
        return self.__send_request(self.__url_cameras, request_type='GET')

    def get_devices(self):
        """ Get all device specific information. """
        return self.__send_request(self.__url_devices, request_type='GET')

    def get_email_notifications(self):
        """ Get settings for the email notifications. """
        return self.__send_request(self.__url_notifications_email, request_type='GET')

    def get_events(self):
        """ Get the alarm panel events. """
        return self.__send_request(self.__url_events, request_type='GET')

    def get_feature_set(self):
        """ Get the alarm panel feature set. """
        return self.__send_request(self.__url_feature_set, request_type='GET')

    def get_locations(self):
        """ Get all locations in the alarm system. """
        return self.__send_request(self.__url_locations, request_type='GET')

    def get_panel_info(self):
        """ The general panel information is only supported in version 4.0. """
        return self.__send_request(self.__url_panel_info, request_type='GET')

    def get_panels(self):
        """ Get a list of panels. """
        return self.__send_request(self.__url_panels, request_type='GET')

    def get_process_status(self, process_token):
        """ Get the current status of a process running on API server. """
        url = self.__url_process_status + process_token
        return self.__send_request(url, request_type='GET')

    def get_smart_devices(self):
        """ Get a list of smart devices. """
        return self.__send_request(self.__url_smart_devices, request_type='GET')

    def get_smart_devices_settings(self):
        """ Get a list of smart devices settings. """
        return self.__send_request(self.__url_smart_devices_settings, request_type='GET')

    def get_status(self):
        """ Get the current status of the alarm system. """
        return self.__send_request(self.__url_status, request_type='GET')

    def get_troubles(self):
        """ Get the current troubles. """
        return self.__send_request(self.__url_troubles, request_type='GET')

    def get_users(self):
        """ Get information about the active users.
        Note: Only master users can see the active_user_ids! """
        return self.__send_request(self.__url_users, request_type='GET')

    def get_wakeup_sms(self):
        """ Get the settings needed to wake up the alarm panel via SMS. """
        return self.__send_request(self.__url_wakeup_sms, request_type='GET')

    def panel_add(self, alias, panel_serial, access_proof, master_user_code):
        """ Add a new alarm panel to the user account. A master user code is required. """
        panel_data = {
            'alias': alias, 
            'panel_serial': panel_serial, 
            'access_proof': access_proof, 
            'master_user_code': master_user_code
        }
        panel_json = json.dumps(panel_data, separators=(',', ':'))
        return self.__send_request(self.__url_panel_add, data_json=panel_json, request_type='POST')

    def panel_login(self, panel_serial, user_code):
        """ Try to login to the alarm panel and get a session token. """
        login_info = {
            'user_code': user_code,
            'app_type': self.__app_type,
            'app_id': self.__app_id,
            'panel_serial': panel_serial
        }

        login_json = json.dumps(login_info, separators=(',', ':'))
        res = self.__send_request(self.__url_panel_login,
                                       with_session_token=False,
                                       data_json=login_json,
                                       request_type='POST')
        if res is not None:
            self.__session_token = res['session_token']
            return True
        else:
            return False

    def panel_rename(self, alias, panel_serial):
        """ Rename an alarm panel. """
        panel_data = {
            'panel_serial': panel_serial, 
            'alias': alias, 
        }
        panel_json = json.dumps(panel_data, separators=(',', ':'))
        return self.__send_request(self.__url_panel_rename, data_json=panel_json, request_type='POST')

    def panel_unlink(self, panel_serial, password, app_id):
        """ Unlink an alarm panel from the user account. """
        panel_data = {
            'panel_serial': panel_serial, 
            'password': password, 
            'app_id': app_id, 
        }
        panel_json = json.dumps(panel_data, separators=(',', ':'))
        return self.__send_request(self.__url_panel_unlink, data_json=panel_json, request_type='POST')

    def password_reset(self, email):
        """ Request a password reset email. An email will be sent to the email address provided. """
        reset_data = {'email': email}
        reset_json = json.dumps(reset_data, separators=(',', ':'))
        return self.__send_request(self.__url_password_reset, data_json=reset_json, request_type='POST')

    def password_reset_complete(self, reset_password_code, new_password):
        """ Complete the password reset request. """
        reset_data = {'reset_password_code': reset_password_code, 'new_password': new_password, 'app_id': self.__app_id}
        reset_json = json.dumps(reset_data, separators=(',', ':'))
        return self.__send_request(self.__url_password_reset_complete, data_json=reset_json, request_type='POST')

    def set_email_notifications(self, mode):
        """ Set settings for the email notifications. """
        notification_data = {'mode': mode}
        notification_json = json.dumps(notification_data, separators=(',', ':'))
        return self.__send_request(self.__url_notifications_email, data_json=notification_json, request_type='POST')

    def set_bypass_zone(self, zone, set_enabled):
        """ Enable or disable bypass mode for a zone. """
        bypass_data = {'zone': zone, 'set': set_enabled}
        bypass_json = json.dumps(bypass_data, separators=(',', ':'))
        return self.__send_request(self.__url_set_bypass_zone, data_json=bypass_json, request_type='POST')

    def set_name(self, object_class, id, name):
        """ Set the name of any type of object in the alarm system. """
        name_data = {'class': object_class, 'id': id, 'name': name}
        name_json = json.dumps(name_data, separators=(',', ':'))
        return self.__send_request(self.__url_set_name, data_json=name_json, request_type='POST')

    def set_user_code(self, user_code, user_id):
        """ Set the code of a user in the alarm system. """
        code_data = {'user_code': user_code, 'user_id': user_id}
        code_json = json.dumps(code_data, separators=(',', ':'))
        return self.__send_request(self.__url_set_user_code, data_json=code_json, request_type='POST')

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
