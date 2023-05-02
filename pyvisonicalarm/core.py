import json
import requests

from .const import (
    TEXT_STATUS_AWAY,
    TEXT_STATUS_DISARM,
    TEXT_STATUS_HOME,
    RequestType,
    VisonicURL,
)

from .exceptions import *


class API(object):
    """Class used for communication with the Visonic API"""

    # Client configuration
    __app_type = "com.visonic.powermaxapp"
    __user_agent = "Dart/2.10 (dart:io)"
    __rest_version = "9.0"

    # API tokens
    __user_token = None
    __session_token = None

    # Use a session to reuse one TCP connection instead of creating a new
    # connection for every call to the API
    __session = None
    __timeout = 4

    def __init__(self, hostname, app_id):
        """Class constructor initializes all URL variables."""

        # Set connection specific details
        self.__hostname = hostname
        self.__app_id = app_id

        # Create a new session
        self.__session = requests.session()

    def set_rest_version(self, version):
        """Set which version to use when connection to the API."""
        self.__rest_version = version

    def __raise_on_bad_request(self, error):
        """Raise an exception when the API returns a bad request."""
        api = json.loads(error.decode("utf-8"))
        # print(api)

        if api["error"] == 10001:  # BadRequestParams
            for pair in api["extras"]:
                if pair["value"] == "incorrect":
                    if pair["key"] == "panel_serial":
                        raise PanelSerialIncorrectError()
                    elif pair["key"] == "reset_password_code":
                        raise ResetPasswordCodeIncorrectError()
                if pair["value"] == "required":
                    if pair["key"] == "panel_serial":
                        raise PanelSerialRequiredError()
                    elif pair["key"] == "email":
                        raise EmailRequiredError()
                    elif pair["key"] == "password":
                        raise PasswordRequiredError()
                    elif pair["key"] == "app_id":
                        raise AppIDRequiredError()
                    elif pair["key"] == "user_code":
                        raise UserCodeRequiredError()
                    elif pair["key"] == "new_password":
                        raise PasswordRequiredError()
                if pair["value"] == "already_granted":
                    raise AlreadyGrantedError()
                if pair["value"] == "already_linked":
                    raise AlreadyLinkedError()
                if pair["key"] == "new_password":
                    raise NewPasswordStrengthError()
        elif api["error"] == 10004:  # WrongCombination
            for pair in api["extras"]:
                if pair["value"] == "wrong_combination":
                    if pair["key"] == "email" or pair["key"] == "password":
                        raise WrongUsernameOrPasswordError()
                    if (
                        pair["key"] == "panel_serial"
                        or pair["key"] == "master_user_code"
                    ):
                        raise WrongPanelSerialOrMasterUserCodeError()
        elif api["error"] == 10021:  # WrongUserCode
            raise UserCodeIncorrectError()
        elif api["error"] == 400 and api["error_reason_code"] == "PanelNotConnected":
            raise PanelNotConnectedError()

        # Raise a generic error when the library has no
        # specific exception implemented yet.
        raise UndefinedBadRequestError(str(api))

    def __raise_on_forbidden(self, error):
        """Raise an exception when the API returns a forbidden error."""
        api = json.loads(error.decode("utf-8"))
        # print(api)

        if api["error"] == 10010:  # NotAllowed
            raise NotAllowedError()
        elif api["error"] == 10002:  # UserAuthRequired
            raise UserAuthRequiredError()

        # Raise a generic error when the library has no
        # specific exception implemented yet.
        raise UndefinedForbiddenError(str(api))

    def __raise_on_unauthorized(self, error):
        """Raise an exception when the API returns a unauthorized error."""
        api = json.loads(error.decode("utf-8"))
        # print(api)

        # Raise an exception when we are not authorized to access the endpoint
        raise UnauthorizedError(str(api))

    def __send_request(
        self,
        endpoint,
        with_session_token=True,
        with_user_token=True,
        data_json=None,
        request_type=RequestType.GET,
    ):
        """Send a GET or POST request to the server. Includes the Session-Token
        only if with_session_token is True."""

        # Add host and api version to url
        if endpoint == VisonicURL.VERSION:
            url = f"{VisonicURL.BASE.format(self.__hostname)}/{endpoint}"
        else:
            url = f"{VisonicURL.BASE.format(self.__hostname)}/{self.__rest_version}/{endpoint}"

        # Prepare the headers to be sent
        headers = {
            "Host": self.__hostname,
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": self.__user_agent,
            "Accept-Language": "en-us",
            "Accept-Encoding": "gzip",
        }

        # Only needed for POST requests
        if request_type == "POST":
            headers["Content-Type"] = "application/json"
            headers["Content-Length"] = str(len(data_json))

        # Include the session token in the header
        if with_session_token:
            headers["Session-Token"] = self.__session_token

        # Include the user authentication token in the header
        if with_user_token:
            headers["User-Token"] = self.__user_token

        # Perform the request and raise an exception
        # if the response is not OK (HTML 200)
        try:
            if request_type == "GET":
                response = self.__session.get(
                    url, headers=headers, timeout=self.__timeout
                )
            elif request_type == "POST":
                response = self.__session.post(
                    url, headers=headers, data=data_json, timeout=self.__timeout
                )
            response.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            raise ConnectionTimeoutError(
                f"Connection to '{self.__hostname}' timed out after {str(self.__timeout)} seconds."
            )
            return None
        except requests.exceptions.HTTPError as e:
            api = json.loads(response.content.decode("utf-8"))
            if "400 Client Error: Bad Request" in str(e):
                self.__raise_on_bad_request(response.content)
            elif "401 Client Error: Unauthorized" in str(e):
                self.__raise_on_unauthorized(response.content)
            elif "403 Client Error: Forbidden" in str(e):
                self.__raise_on_forbidden(response.content)
            elif "404 Client Error: Not Found" in str(e):
                raise NotFoundError()
            elif "420 Client Error:" in str(e):
                # TODO: {'error': 10020, 'error_message': 'Login temporary blocked', 'error_reason_code': 'LoginTemporaryBlocked', 'extras': [{'key': 'timeout', 'value': 44}]} // 44 = seconds to unblocked
                # print(api)
                raise LoginTemporaryBlockedError(
                    f"Login is temporary blocked due to too many failed login attempts ({api['extras'][0]['count']} seconds remaining)."
                )
            elif "440 Client Error: Session token not found" in str(e):
                raise SessionTokenError()
            elif "442 Client Error: Login attempts limit reached" in str(e):
                raise LoginAttemptsLimitReachedError("Login attempts limit reached.")
            elif "444 Client Error: Wrong user code" in str(e):
                raise InvalidUserCodeError(
                    "Authentication failed due to wrong user code."
                )
            else:
                print(api)
                raise

        # Check HTTP response code
        if response.status_code == requests.codes.ok:
            return json.loads(response.content.decode("utf-8"))
        else:
            return None

    ######################
    # Public API methods #
    ######################

    @property
    def session_token(self):
        """Property to keep track of the session token."""
        return self.__session_token

    @property
    def hostname(self):
        """Property to keep track of the API servers hostname."""
        return self.__hostname

    @property
    def user_token(self):
        """Property to keep track of the user token beeing assigned during authentication."""
        return self.__user_token

    @property
    def app_id(self):
        """Property to keep track of the user id (UUID) beeing used."""
        return self.__app_id

    def get_version_info(self):
        """Find out which REST API versions are supported."""
        return self.__send_request(
            VisonicURL.VERSION,
            with_session_token=False,
            with_user_token=False,
            request_type=RequestType.GET,
        )

    def authenticate(self, email, password):
        """Try to authenticate and get a user auth token."""
        auth_info = {
            "email": email,
            "password": password,
            "app_id": self.__app_id,
        }

        auth_json = json.dumps(auth_info, separators=(",", ":"))
        res = self.__send_request(
            VisonicURL.AUTH,
            with_session_token=False,
            with_user_token=False,
            data_json=auth_json,
            request_type=RequestType.POST,
        )
        if res is not None:
            self.__user_token = res["user_token"]
            return True
        else:
            return False

    def is_logged_in(self):
        """Check if the session token is still valid."""
        try:
            self.get_status()
            return True
        except requests.HTTPError:
            return False

    def access_grant(self, user_id, email):
        """Grant a user access to the alarm panel via the API."""
        user_data = {"user": user_id, "email": email}
        user_json = json.dumps(user_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.ACCESS_GRANT, data_json=user_json, request_type=RequestType.POST
        )

    def access_revoke(self, user_id):
        """Revoke access to the alarm panel via the API for a user."""
        user_data = {"user": user_id}
        user_json = json.dumps(user_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.ACCESS_REVOKE, data_json=user_json, request_type=RequestType.POST
        )

    def activate_siren(self):
        """Activate the siren (sound the alarm)."""
        siren_data = {}
        siren_json = json.dumps(siren_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.ACTIVATE_SIREN,
            data_json=siren_json,
            request_type=RequestType.POST,
        )

    def disable_siren(self, mode):
        """Disable the siren (mute the alarm)."""
        siren_data = {"mode": mode}
        siren_json = json.dumps(siren_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.DISABLE_SIREN,
            data_json=siren_json,
            request_type=RequestType.POST,
        )

    def get_alarms(self):
        """Get the current alarms."""
        return self.__send_request(VisonicURL.ALARMS)

    def get_alerts(self):
        """Get the current alerts."""
        return self.__send_request(VisonicURL.ALERTS)

    def get_cameras(self):
        """Get the cameras in the system."""
        return self.__send_request(VisonicURL.CAMERAS)

    def get_devices(self):
        """Get all device specific information."""
        return self.__send_request(VisonicURL.DEVICES)

    def get_email_notifications(self):
        """Get settings for the email notifications."""
        return self.__send_request(VisonicURL.NOTIFICATIONS_EMAIL)

    def get_events(self):
        """Get the alarm panel events."""
        return self.__send_request(VisonicURL.EVENTS)

    def get_feature_set(self):
        """Get the alarm panel feature set."""
        return self.__send_request(VisonicURL.FEATURE_SET)

    def get_locations(self):
        """Get all locations in the alarm system."""
        return self.__send_request(VisonicURL.LOCATIONS)

    def get_panel_info(self):
        """The general panel information is only supported in version 4.0."""
        return self.__send_request(VisonicURL.PANEL_INFO)

    def get_panels(self):
        """Get a list of panels."""
        return self.__send_request(VisonicURL.PANELS)

    def get_process_status(self, process_token):
        """Get the current status of a process running on API server."""
        return self.__send_request(VisonicURL.PROCESS_STATUS.format(process_token))

    def get_smart_devices(self):
        """Get a list of smart devices."""
        return self.__send_request(VisonicURL.SMART_DEVICES)

    def get_smart_devices_settings(self):
        """Get a list of smart devices settings."""
        return self.__send_request(VisonicURL.SMART_DEVICES_SETTINGS)

    def get_status(self):
        """Get the current status of the alarm system."""
        return self.__send_request(VisonicURL.STATUS)

    def get_troubles(self):
        """Get the current troubles."""
        return self.__send_request(VisonicURL.TROUBLES)

    def get_users(self):
        """Get information about the active users.
        Note: Only master users can see the active_user_ids!"""
        return self.__send_request(VisonicURL.USERS)

    def get_wakeup_sms(self):
        """Get the settings needed to wake up the alarm panel via SMS."""
        return self.__send_request(VisonicURL.WAKEUP_SMS)

    def panel_add(
        self, alias: str, panel_serial: str, access_proof: str, master_user_code: str
    ):
        """Add a new alarm panel to the user account. A master user code is required."""
        panel_data = {
            "alias": alias,
            "panel_serial": panel_serial,
            "access_proof": access_proof,
            "master_user_code": master_user_code,
        }
        panel_json = json.dumps(panel_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.PANEL_ADD, data_json=panel_json, request_type=RequestType.POST
        )

    def panel_login(self, panel_serial: str, user_code: str):
        """Try to login to the alarm panel and get a session token."""
        login_info = {
            "user_code": user_code,
            "app_type": self.__app_type,
            "app_id": self.__app_id,
            "panel_serial": panel_serial,
        }

        login_json = json.dumps(login_info, separators=(",", ":"))
        res = self.__send_request(
            VisonicURL.PANEL_LOGIN,
            with_session_token=False,
            data_json=login_json,
            request_type=RequestType.POST,
        )
        if res:
            self.__session_token = res["session_token"]
            return True
        else:
            return False

    def panel_rename(self, alias: str, panel_serial: str):
        """Rename an alarm panel."""
        panel_data = {
            "panel_serial": panel_serial,
            "alias": alias,
        }
        panel_json = json.dumps(panel_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.PANEL_RENAME, data_json=panel_json, request_type=RequestType.POST
        )

    def panel_unlink(self, panel_serial: str, password: str, app_id: str):
        """Unlink an alarm panel from the user account."""
        panel_data = {
            "panel_serial": panel_serial,
            "password": password,
            "app_id": app_id,
        }
        panel_json = json.dumps(panel_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.PANEL_UNLINK, data_json=panel_json, request_type=RequestType.POST
        )

    def password_reset(self, email: str):
        """Request a password reset email. An email will be sent to the email address provided."""
        reset_data = {"email": email}
        reset_json = json.dumps(reset_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.PASSWORD_RESET,
            data_json=reset_json,
            request_type=RequestType.POST,
        )

    def password_reset_complete(self, reset_password_code: str, new_password: str):
        """Complete the password reset request."""
        reset_data = {
            "reset_password_code": reset_password_code,
            "new_password": new_password,
            "app_id": self.__app_id,
        }
        reset_json = json.dumps(reset_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.PASSWORD_RESET_COMPLETE,
            data_json=reset_json,
            request_type=RequestType.POST,
        )

    def set_email_notifications(self, mode: str):
        """Set settings for the email notifications."""
        notification_data = {"mode": mode}
        notification_json = json.dumps(notification_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.NOTIFICATIONS_EMAIL,
            data_json=notification_json,
            request_type=RequestType.POST,
        )

    def set_bypass_zone(self, zone: int, set_enabled: bool):
        """Enable or disable bypass mode for a zone."""
        bypass_data = {"zone": zone, "set": set_enabled}
        bypass_json = json.dumps(bypass_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.SET_BYPASS_ZONE,
            data_json=bypass_json,
            request_type=RequestType.POST,
        )

    def set_name(self, object_class: str, id: int, name: str):
        """Set the name of any type of object in the alarm system."""
        name_data = {"class": object_class, "id": id, "name": name}
        name_json = json.dumps(name_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.SET_NAME, data_json=name_json, request_type=RequestType.POST
        )

    def set_user_code(self, user_code: str, user_id: str):
        """Set the code of a user in the alarm system."""
        code_data = {"user_code": user_code, "user_id": user_id}
        code_json = json.dumps(code_data, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.SET_USER_CODE, data_json=code_json, request_type=RequestType.POST
        )

    def arm_home(self, partition: int):
        """Arm in Home mode."""
        arm_info = {"partition": partition, "state": TEXT_STATUS_HOME}
        arm_json = json.dumps(arm_info, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.SET_STATE, data_json=arm_json, request_type=RequestType.POST
        )

    def arm_away(self, partition: id):
        """Arm in Away mode."""
        arm_info = {"partition": partition, "state": TEXT_STATUS_AWAY}
        arm_json = json.dumps(arm_info, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.SET_STATE, data_json=arm_json, request_type=RequestType.POST
        )

    def disarm(self, partition: id):
        """Disarm the alarm system."""
        disarm_info = {"partition": partition, "state": TEXT_STATUS_DISARM}
        disarm_json = json.dumps(disarm_info, separators=(",", ":"))
        return self.__send_request(
            VisonicURL.SET_STATE, data_json=disarm_json, request_type=RequestType.POST
        )

    def send_get(self, url):
        """Send a custom POST request."""
        return self.__send_request(url)

    def send_post(self, url, data):
        """Send a custom POST request."""
        data_json = json.dumps(data, separators=(",", ":"))
        return self.__send_request(
            url, data_json=data_json, request_type=RequestType.POST
        )
