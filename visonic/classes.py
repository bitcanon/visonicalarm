from dataclasses import dataclass
import functools
import inspect


@dataclass
class BaseClass:
    """Base class"""

    _data: dict

    def __repr__(self):
        r = ""
        attrs = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        for i, a in enumerate([attr for attr in attrs if self._is_property(attr)]):
            if i:
                r = r + ", "
            r = r + f"{a[0]} = {getattr(self, a[0])}"
        return f"{type(self).__name__}({r})"

    def __str__(self):
        r = {}
        attrs = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        for a in [attr for attr in attrs if self._is_property(attr)]:
            r[a[0]] = getattr(self, a[0])
        return f"{str(type(self))}: {r}"

    def _is_property(self, attr) -> bool:
        if not (
            attr[0].startswith("__")
            and attr[0].endswith("__")
            or attr[0].startswith("_")
        ):
            return True
        return False

    def _get_nested_key(self, path, *default):
        """Get key value in json by dotted notation or return default"""
        try:
            return functools.reduce(lambda x, y: x[y], path.split("."), self._data)
        except KeyError:
            if default:
                return default[0]
            return None


@dataclass
class Camera(BaseClass):
    """Class definition of an event in the alarm system."""

    # Camera properties
    @property
    def location(self):
        return self._data["location"].capitalize()

    @property
    def partitions(self):
        return self._data["partitions"]

    @property
    def preenroll(self):
        return self._data["preenroll"]

    @property
    def preview_path(self):
        return self._data["preview_path"]

    @property
    def status(self):
        return self._data["status"]

    @property
    def timestamp(self):
        return self._data["timestamp"]

    @property
    def zone(self):
        return self._data["zone"]

    @property
    def zone_name(self):
        return self._data["zone_name"].capitalize()


@dataclass
class Event(BaseClass):
    """Class definition of an event in the alarm system."""

    # Event properties
    @property
    def id(self):
        """User ID."""
        return self._data["event"]

    @property
    def type_id(self):
        """Event type ID."""
        return self._data["type_id"]

    @property
    def label(self):
        """Event label."""
        return self._data["label"]

    @property
    def description(self):
        """Event description."""
        return self._data["description"]

    @property
    def appointment(self):
        """Event appointment."""
        return self._data["appointment"]

    @property
    def datetime(self):
        """Event datetime."""
        return self._data["datetime"]

    @property
    def video(self):
        """Event has video."""
        return self._data["video"]

    @property
    def device_type(self):
        """Event device type."""
        return self._data["device_type"]

    @property
    def zone(self):
        """Event zone."""
        return self._data["zone"]

    @property
    def partitions(self):
        """Event partitions."""
        return self._data["partitions"]

    @property
    def name(self):
        """Event name."""
        return self._data["name"]


@dataclass
class FeatureSet(BaseClass):
    """Class definition of an event in the alarm system."""

    # Event properties
    @property
    def events_enabled(self):
        return self._data["events"]["is_enabled"]

    @property
    def datetime_enabled(self):
        return self._data["datetime"]["is_enabled"]

    @property
    def partitions_enabled(self):
        return self._data["partitions"]["is_enabled"]

    @property
    def partitions_has_labels(self):
        return self._data["partitions"]["is_labels_enabled"]

    @property
    def partitions_max_count(self):
        return self._data["partitions"]["max_partitions"]

    @property
    def devices_enabled(self):
        return self._data["devices"]["is_enabled"]

    @property
    def sirens_can_enable(self):
        return self._data["sirens"]["can_enable"]

    @property
    def sirens_can_disable(self):
        return self._data["sirens"]["can_disable"]

    @property
    def home_automation_devices_enabled(self):
        return (self._data["home_automation_devices"]["is_enabled"],)

    @property
    def state_enabled(self):
        return self._data["state"]["is_enabled"]

    @property
    def state_can_set(self):
        return self._data["state"]["can_set"]

    @property
    def state_can_get(self):
        return self._data["state"]["can_get"]

    @property
    def faults_enabled(self):
        return self._data["faults"]["is_enabled"]

    @property
    def diagnostic_enabled(self):
        return self._data["diagnostic"]["is_enabled"]

    @property
    def wifi_enabled(self):
        return self._data["wifi"]["is_enabled"]


@dataclass
class Location(BaseClass):
    """Class definition of a location in the alarm system."""

    # Location properties
    @property
    def id(self):
        """Location ID."""
        return self._data["hel_id"]

    @property
    def name(self):
        """Location name."""
        return self._data["name"].capitalize()

    @property
    def is_editable(self):
        """Location is editable."""
        return self._data["is_editable"]


@dataclass
class PanelInfo(BaseClass):
    """Class definition of the general alarm system information."""

    # PanelInfo properties
    @property
    def current_user(self):
        """Current User"""
        return self._data["current_user"]

    @property
    def manufacturer(self):
        """Manufacturer"""
        return self._data["manufacturer"]

    @property
    def model(self):
        """Model name"""
        return self._data["model"]

    @property
    def serial(self):
        """Serial no"""
        return self._data["serial"]


@dataclass
class Panel(BaseClass):
    """Class definition of the general alarm system information."""

    # Panel properties
    @property
    def panel_serial(self):
        return self._data["panel_serial"]

    @property
    def alias(self):
        return self._data["alias"]


@dataclass
class Partition(BaseClass):
    """Class definition of a partition in the alarm system."""

    # Partition properties
    @property
    def id(self):
        return self._data["id"]

    @property
    def state(self):
        return self._data["state"]

    @property
    def status(self):
        return self._data["status"]

    @property
    def ready(self):
        return self._data["ready"]

    @property
    def options(self):
        return self._data["options"]


@dataclass
class Process(BaseClass):
    """Class definition of a process in the alarm system."""

    # Partition properties
    @property
    def token(self):
        return self._data["token"]

    @property
    def status(self):
        return self._data["status"]

    @property
    def message(self):
        return self._data["message"]

    @property
    def error(self):
        return self._data["error"]


@dataclass
class Status(BaseClass):
    """Class definition representing the status of the alarm system."""

    # Status properties
    @property
    def connected(self):
        return self._data["connected"]

    @property
    def bba_connected(self):
        return (
            self._data["connected_status"]["bba"]["is_connected"]
            if "bba" in self._data["connected_status"]
            else False
        )

    @property
    def bba_state(self):
        return (
            self._data["connected_status"]["bba"]["state"]
            if "bba" in self._data["connected_status"]
            else "unknown"
        )

    @property
    def gprs_connected(self):
        return (
            self._data["connected_status"]["gprs"]["is_connected"]
            if "gprs" in self._data["connected_status"]
            else False
        )

    @property
    def gprs_state(self):
        return (
            self._data["connected_status"]["gprs"]["state"]
            if "gprs" in self._data["connected_status"]
            else "unknown"
        )

    @property
    def discovery_completed(self):
        return self._data["discovery"]["completed"]

    @property
    def discovery_stages(self):
        return self._data["discovery"]["stages"]

    @property
    def discovery_in_queue(self):
        return self._data["discovery"]["in_queue"]

    @property
    def discovery_triggered(self):
        return self._data["discovery"]["triggered"]

    @property
    def partitions(self):
        return [Partition(partition) for partition in self._data["partitions"]]

    @property
    def rssi_level(self):
        return self._data["rssi"]["level"]

    @property
    def rssi_network(self):
        return self._data["rssi"]["network"]


@dataclass
class Trouble(BaseClass):
    """Class definition of a trouble in the alarm system."""

    # Trouble properties
    @property
    def device_type(self):
        """Device type."""
        return self._data["device_type"]

    @property
    def location(self):
        """Location."""
        return self._data["location"]

    @property
    def partitions(self):
        """Partitions."""
        return self._data["partitions"]

    @property
    def trouble_type(self):
        """Trouble type."""
        return self._data["trouble_type"]

    @property
    def zone(self):
        """Zone ID."""
        return self._data["zone"]

    @property
    def zone_name(self):
        """Zone type."""
        return self._data["zone_name"]

    @property
    def zone_type(self):
        """Zone type."""
        return self._data["zone_type"]


@dataclass
class User(BaseClass):
    """Class definition of a user in the alarm system."""

    # User properties
    @property
    def id(self):
        """User ID."""
        return self._data["id"]

    @property
    def name(self):
        """User name."""
        return self._data["name"]

    @property
    def email(self):
        """User email."""
        return self._data["email"]

    @property
    def partitions(self):
        """Device is active."""
        return self._data["partitions"]


@dataclass
class WakeupSMS(BaseClass):
    """Class definition of a wakeup SMS in the alarm system."""

    # Wakeup SMS properties
    @property
    def phone_number(self):
        return self._data["phone"]

    @property
    def message(self):
        return self._data["sms"]
