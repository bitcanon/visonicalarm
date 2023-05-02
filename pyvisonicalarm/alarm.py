from .classes import (
    Camera,
    Event,
    FeatureSet,
    Location,
    PanelInfo,
    Panel,
    Process,
    Status,
    Trouble,
    User,
    WakeupSMS,
)
from .core import API
from .device_definitions import DEVICE_SUBTYPES, DEVICE_TYPES
from .devices import GenericDevice
from .exceptions import UnsupportedRestAPIVersionError


class Setup(object):
    """Class definition of the main alarm system."""

    def __init__(self, hostname, app_id, api_version="latest"):
        """Initiate the connection to the REST API."""
        self.__api = API(hostname, app_id)
        # self.set_rest_version(api_version)

    # System properties
    @property
    def api(self):
        """Return the API for direct access."""
        return self.__api

    def access_grant(self, user_id, email):
        """Grant a user access to the alarm panel via the API."""
        return self.__api.access_grant(user_id, email)

    def access_revoke(self, user_id):
        """Revoke access to the alarm panel via the API for a user."""
        return self.__api.access_revoke(user_id)

    def activate_siren(self):
        """Activate the siren (sound the alarm)."""
        return self.__api.activate_siren()["process_token"]

    def arm_home(self, partition=-1):
        """Send Arm Home command to the alarm system."""
        return self.__api.arm_home(partition)["process_token"]

    def arm_away(self, partition=-1):
        """Send Arm Away command to the alarm system."""
        return self.__api.arm_away(partition)["process_token"]

    def authenticate(self, email, password):
        """Try to authenticate against the API with an email address and password."""
        self.set_rest_version("latest")
        return self.__api.authenticate(email, password)

    def connected(self):
        """Check if the API server is connected to the alarm panel"""
        return self.get_status().connected

    def disable_siren(self, mode="all"):
        """Disable the siren (mute the alarm)."""
        return self.__api.disable_siren(mode=mode)["process_token"]

    def disarm(self, partition=-1):
        """Send Disarm command to the alarm system."""
        return self.__api.disarm(partition)["process_token"]

    def get_cameras(self):
        """Fetch all the devices that are available."""
        cameras = self.__api.get_cameras()
        return [Camera(camera) for camera in cameras]

    def get_devices(self):
        """Fetch all the devices that are available."""
        device_list = []
        devices = self.__api.get_devices()

        for device in devices:
            if DeviceClass := DEVICE_SUBTYPES.get(device["subtype"]):
                device_list.append(DeviceClass(device))
            elif DeviceClass := DEVICE_TYPES.get(device["device_type"]):
                device_list.append(DeviceClass(device))
            else:
                device_list.append(GenericDevice(device))

        return device_list

    def get_events(self, timestamp_hour_offset=2):
        """Get the last couple of events (60 events on my system)."""
        events = self.__api.get_events()
        return [Event(event) for event in events]

    def get_feature_set(self):
        """Fetch the locations associated with the alarm system."""
        feature_set = self.__api.get_feature_set()
        return FeatureSet(feature_set)

    def get_locations(self):
        """Fetch the locations associated with the alarm system."""
        locations = self.__api.get_locations()
        return [Location(location) for location in locations]

    def get_panel_info(self):
        """Fetch basic information about the alarm system."""
        gpi = self.__api.get_panel_info()
        return PanelInfo(gpi)

    def get_panels(self):
        """Fetch a list of panels associated with the user."""
        panels = self.__api.get_panels()
        return [Panel(panel) for panel in panels]

    def get_process_status(self, process_token):
        """Fetch the status information associated with a process token."""
        processes = self.__api.get_process_status(process_token)
        return [Process(process) for process in processes]

    def get_rest_versions(self):
        """Fetch the supported API versions."""
        return self.api.get_version_info()["rest_versions"]

    def get_status(self):
        """Fetch the current state of the alarm system."""

        status = self.__api.get_status()
        return Status(status)

    def get_troubles(self):
        """Fetch all the troubles that are available."""
        troubles = self.__api.get_troubles()
        return [Trouble(trouble) for trouble in troubles]

    def get_users(self):
        """Fetch a list of users in the alarm system."""
        users = self.__api.get_users()
        return [User(user) for user in users["users"]]

    def get_wakeup_sms(self):
        """Fetch a list of users in the alarm system."""
        wakeup_sms = self.__api.get_wakeup_sms()
        return WakeupSMS(wakeup_sms)

    def panel_add(self, alias, panel_serial, master_user_code, access_proof=None):
        """Add a new alarm panel to the user account. A master user code is required."""
        return self.__api.panel_add(alias, panel_serial, access_proof, master_user_code)

    def panel_login(self, panel_serial, user_code):
        """Establish a connection between the alarm panel and the API server."""
        return self.__api.panel_login(panel_serial, user_code)

    def panel_rename(self, alias, panel_serial):
        """Rename an alarm panel."""
        return self.__api.panel_rename(alias, panel_serial)

    def panel_unlink(self, panel_serial, password, app_id):
        """Unlink an alarm panel from the user account."""
        return self.__api.panel_unlink(panel_serial, password, app_id)

    def password_reset(self, email):
        """Send a password reset link to the email address provided in the email argument."""
        return self.__api.password_reset(email)

    def password_reset_complete(self, reset_password_code, new_password):
        """Complete the password reset by entering the reset code received in the email and a new password."""
        return self.__api.password_reset_complete(reset_password_code, new_password)[
            "user_token"
        ]

    def set_bypass_zone(self, zone, set_enabled):
        """Enabled or disable zone bypassing (for example, bypass a sensor to disable it)."""
        return self.__api.set_bypass_zone(zone, set_enabled)["process_token"]

    def set_name_user(self, user_id, name):
        """Set the name of a user by user ID."""
        return self.__api.set_name("USER", user_id, name)["process_token"]

    def set_rest_version(self, version="latest"):
        """
        Fetch the supported versions from the API server and automatically
        configure the library to use the latest version supported by the server,
        unless overridden in the version parameter.
        """
        rest_versions = self.api.get_version_info()["rest_versions"]
        rest_versions.sort(key=float)
        if version == "latest":
            self.__api.set_rest_version(rest_versions[-1])
        elif version in rest_versions:
            self.__api.set_rest_version(version)
        else:
            raise UnsupportedRestAPIVersionError(
                f"Rest API version {version} is not supported by server."
            )

    def set_user_code(self, user_id, user_code):
        """Set the code of a user by user ID."""
        return self.__api.set_user_code(user_code, user_id)["process_token"]
