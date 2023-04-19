from dataclasses import dataclass


@dataclass
class Camera(object):
    """Class definition of an event in the alarm system."""

    _camera: dict

    # Camera properties
    @property
    def location(self):
        return self._camera["location"].capitalize()

    @property
    def partitions(self):
        return self._camera["partitions"]

    @property
    def preenroll(self):
        return self._camera["preenroll"]

    @property
    def preview_path(self):
        return self._camera["preview_path"]

    @property
    def status(self):
        return self._camera["status"]

    @property
    def timestamp(self):
        return self._camera["timestamp"]

    @property
    def zone(self):
        return self._camera["zone"]

    @property
    def zone_name(self):
        return self._camera["zone_name"].capitalize()


@dataclass
class Event(object):
    """Class definition of an event in the alarm system."""

    _event: dict

    # Event properties
    @property
    def id(self):
        """User ID."""
        return self._event["event"]

    @property
    def type_id(self):
        """Event type ID."""
        return self._event["type_id"]

    @property
    def label(self):
        """Event label."""
        return self._event["label"]

    @property
    def description(self):
        """Event description."""
        return self._event["description"]

    @property
    def appointment(self):
        """Event appointment."""
        return self._event["appointment"]

    @property
    def datetime(self):
        """Event datetime."""
        return self._event["datetime"]

    @property
    def video(self):
        """Event has video."""
        return self._event["video"]

    @property
    def device_type(self):
        """Event device type."""
        return self._event["device_type"]

    @property
    def zone(self):
        """Event zone."""
        return self._event["zone"]

    @property
    def partitions(self):
        """Event partitions."""
        return self._event["partitions"]

    @property
    def name(self):
        """Event name."""
        return self._event["name"]


@dataclass
class FeatureSet(object):
    """Class definition of an event in the alarm system."""

    _feature_set: dict

    # Event properties
    @property
    def events_enabled(self):
        return self._feature_set["events"]["is_enabled"]

    @property
    def datetime_enabled(self):
        return self._feature_set["datetime"]["is_enabled"]

    @property
    def partitions_enabled(self):
        return self._feature_set["partitions"]["is_enabled"]

    @property
    def partitions_has_labels(self):
        return self._feature_set["partitions"]["is_labels_enabled"]

    @property
    def partitions_max_count(self):
        return self._feature_set["partitions"]["max_partitions"]

    @property
    def devices_enabled(self):
        return self._feature_set["devices"]["is_enabled"]

    @property
    def sirens_can_enable(self):
        return self._feature_set["sirens"]["can_enable"]

    @property
    def sirens_can_disable(self):
        return self._feature_set["sirens"]["can_disable"]

    @property
    def home_automation_devices_enabled(self):
        return (self._feature_set["home_automation_devices"]["is_enabled"],)

    @property
    def state_enabled(self):
        return self._feature_set["state"]["is_enabled"]

    @property
    def state_can_set(self):
        return self._feature_set["state"]["can_set"]

    @property
    def state_can_get(self):
        return self._feature_set["state"]["can_get"]

    @property
    def faults_enabled(self):
        return self._feature_set["faults"]["is_enabled"]

    @property
    def diagnostic_enabled(self):
        return self._feature_set["diagnostic"]["is_enabled"]

    @property
    def wifi_enabled(self):
        return self._feature_set["wifi"]["is_enabled"]


@dataclass
class Location(object):
    """Class definition of a location in the alarm system."""

    _location: dict

    # Location properties
    @property
    def id(self):
        """Location ID."""
        return self._location["hel_id"]

    @property
    def name(self):
        """Location name."""
        return self._location["name"].capitalize()

    @property
    def is_editable(self):
        """Location is editable."""
        return self._location["is_editable"]


@dataclass
class PanelInfo(object):
    """Class definition of the general alarm system information."""

    _gpi: dict

    # PanelInfo properties
    @property
    def current_user(self):
        """Current User"""
        return self._gpi["current_user"]

    @property
    def manufacturer(self):
        """Manufacturer"""
        return self._gpi["manufacturer"]

    @property
    def model(self):
        """Model name"""
        return self._gpi["model"]

    @property
    def serial(self):
        """Serial no"""
        return self._gpi["serial"]


@dataclass
class Panel(object):
    """Class definition of the general alarm system information."""

    _panel: dict

    # Panel properties
    @property
    def panel_serial(self):
        return self._panel["panel_serial"]

    @property
    def alias(self):
        return self._panel["alias"]


@dataclass
class Partition(object):
    """Class definition of a partition in the alarm system."""

    _partition: dict

    # Partition properties
    @property
    def id(self):
        return self._partition["id"]

    @property
    def state(self):
        return self._partition["state"]

    @property
    def status(self):
        return self._partition["status"]

    @property
    def ready(self):
        return self._partition["ready"]

    @property
    def options(self):
        return self._partition["options"]


@dataclass
class Process(object):
    """Class definition of a process in the alarm system."""

    _process: dict

    # Partition properties
    @property
    def token(self):
        return self._process["token"]

    @property
    def status(self):
        return self._process["status"]

    @property
    def message(self):
        return self._process["message"]

    @property
    def error(self):
        return self._process["error"]


@dataclass
class Status(object):
    """Class definition representing the status of the alarm system."""

    _status: dict

    # Status properties
    @property
    def connected(self):
        return self._status["connected"]

    @property
    def bba_connected(self):
        return (
            self._status["connected_status"]["bba"]["is_connected"]
            if "bba" in self._status["connected_status"]
            else False
        )

    @property
    def bba_state(self):
        return (
            self._status["connected_status"]["bba"]["state"]
            if "bba" in self._status["connected_status"]
            else "unknown"
        )

    @property
    def gprs_connected(self):
        return (
            self._status["connected_status"]["gprs"]["is_connected"]
            if "gprs" in self._status["connected_status"]
            else False
        )

    @property
    def gprs_state(self):
        return (
            self._status["connected_status"]["gprs"]["state"]
            if "gprs" in self._status["connected_status"]
            else "unknown"
        )

    @property
    def discovery_completed(self):
        return self._status["discovery"]["completed"]

    @property
    def discovery_stages(self):
        return self._status["discovery"]["stages"]

    @property
    def discovery_in_queue(self):
        return self._status["discovery"]["in_queue"]

    @property
    def discovery_triggered(self):
        return self._status["discovery"]["triggered"]

    @property
    def partitions(self):
        return [Partition(partition) for partition in self._status["partitions"]]

    @property
    def rssi_level(self):
        return self._status["rssi"]["level"]

    @property
    def rssi_network(self):
        return self._status["rssi"]["network"]


@dataclass
class Trouble(object):
    """Class definition of a trouble in the alarm system."""

    _trouble: dict

    # Trouble properties
    @property
    def device_type(self):
        """Device type."""
        return self._trouble["device_type"]

    @property
    def location(self):
        """Location."""
        return self._trouble["location"]

    @property
    def partitions(self):
        """Partitions."""
        return self._trouble["partitions"]

    @property
    def trouble_type(self):
        """Trouble type."""
        return self._trouble["trouble_type"]

    @property
    def zone(self):
        """Zone ID."""
        return self._trouble["zone"]

    @property
    def zone_name(self):
        """Zone type."""
        return self._trouble["zone_name"]

    @property
    def zone_type(self):
        """Zone type."""
        return self._trouble["zone_type"]


@dataclass
class User(object):
    """Class definition of a user in the alarm system."""

    _user: dict

    # User properties
    @property
    def id(self):
        """User ID."""
        return self._user["id"]

    @property
    def name(self):
        """User name."""
        return self._user["name"]

    @property
    def email(self):
        """User email."""
        return self._user["email"]

    @property
    def partitions(self):
        """Device is active."""
        return self._user["partitions"]


@dataclass
class WakeupSMS(object):
    """Class definition of a wakeup SMS in the alarm system."""

    _wakeup_sms: dict

    # Wakeup SMS properties
    @property
    def phone_number(self):
        return self._wakeup_sms["phone"]

    @property
    def message(self):
        return self._wakeup_sms["sms"]
