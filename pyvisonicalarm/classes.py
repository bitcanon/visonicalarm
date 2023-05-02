from dataclasses import dataclass
import functools
import inspect

from .const import TEXT_UNKNOWN


# Decorator function to set string output to title case
def title_case(func):
    def wrapper(*args, **kwargs):
        if result := func(*args, **kwargs):
            return str(result).title()
        return result

    return wrapper


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
    @title_case
    def location(self) -> str:
        return self._data.get("location")

    @property
    def partitions(self) -> list[int]:
        return self._data.get("partitions", [])

    @property
    def preenroll(self) -> bool:
        return self._data.get("preenroll", False)

    @property
    def preview_path(self) -> str:
        return self._data.get("preview_path")

    @property
    def status(self) -> str:
        return self._data.get("status")

    @property
    def timestamp(self) -> str:
        # TODO: COnvert to datetime
        return self._data.get("timestamp")

    @property
    def zone(self) -> int:
        return self._data.get("zone")

    @property
    @title_case
    def zone_name(self) -> str:
        return self._data.get("zone_name")


@dataclass
class Event(BaseClass):
    """Class definition of an event in the alarm system."""

    # Event properties
    @property
    def id(self) -> int:
        """User ID."""
        return self._data.get("event", 0)

    @property
    def type_id(self) -> int:
        """Event type ID."""
        return self._data.get("type_id", 0)

    @property
    @title_case
    def label(self) -> str:
        """Event label."""
        return self._data.get("label")

    @property
    def description(self) -> str:
        """Event description."""
        return self._data.get("description")

    @property
    @title_case
    def appointment(self) -> str:
        """Event appointment."""
        return self._data.get("appointment")

    @property
    def datetime(self) -> str:
        """Event datetime."""
        # TODO: make datetime
        return self._data.get("datetime")

    @property
    def video(self) -> bool:
        """Event has video."""
        return self._data.get("video", False)

    @property
    @title_case
    def device_type(self) -> str:
        """Event device type."""
        return self._data.get("device_type")

    @property
    def zone(self) -> int:
        """Event zone."""
        return self._data.get("zone")

    @property
    def partitions(self) -> list[int]:
        """Event partitions."""
        return self._data.get("partitions")

    @property
    def name(self) -> str:
        """Event name."""
        return self._data.get("name")


@dataclass
class FeatureSet(BaseClass):
    """Class definition of an event in the alarm system."""

    # Event properties
    @property
    def events_enabled(self):
        return self._get_nested_key("events.is_enabled")

    @property
    def datetime_enabled(self):
        return self._get_nested_key("datetime.is_enabled")

    @property
    def partitions_enabled(self):
        return self._get_nested_key("partitions.is_enabled")

    @property
    def partitions_has_labels(self):
        return self._get_nested_key("partitions.is_labels_enabled")

    @property
    def partitions_max_count(self):
        return self._get_nested_key("partitions.max_partitions")

    @property
    def devices_enabled(self):
        return self._get_nested_key("devices.is_enabled")

    @property
    def sirens_can_enable(self):
        return self._get_nested_key("sirens.can_enable")

    @property
    def sirens_can_disable(self):
        return self._get_nested_key("sirens.can_disable")

    @property
    def home_automation_devices_enabled(self):
        return self._get_nested_key("home_automation_devices.is_enabled")

    @property
    def state_enabled(self):
        return self._get_nested_key("state.is_enabled")

    @property
    def state_can_set(self):
        return self._get_nested_key("state.can_set")

    @property
    def state_can_get(self):
        return self._get_nested_key("state.can_get")

    @property
    def faults_enabled(self):
        return self._get_nested_key("faults.is_enabled")

    @property
    def diagnostic_enabled(self):
        return self._get_nested_key("diagnostic.is_enabled")

    @property
    def wifi_enabled(self):
        return self._get_nested_key("wifi.is_enabled")


@dataclass
class Location(BaseClass):
    """Class definition of a location in the alarm system."""

    # Location properties
    @property
    def id(self):
        """Location ID."""
        return self._data.get("hel_id")

    @property
    @title_case
    def name(self):
        """Location name."""
        return self._data.get("name")

    @property
    def is_editable(self):
        """Location is editable."""
        return self._data.get("is_editable")


@dataclass
class PanelInfoPartition(BaseClass):
    @property
    def id(self) -> int:
        return self._data.get("id")

    @property
    def active(self) -> bool:
        return self._data.get("active")

    @property
    def exit_delay_time(self) -> int:
        return self._data.get("exit_delay_time")

    @property
    def state_set(self) -> str:
        return self._data.get("state_set")

    @property
    def name(self) -> str:
        return self._data.get("name")


@dataclass
class PanelInfoFeatures(BaseClass):
    @property
    def video_on_demand(self) -> bool:
        return self._data.get("video_on_demand")

    @property
    def alert(self) -> bool:
        return self._data.get("alert")

    @property
    def enabling_siren(self) -> bool:
        return self._data.get("enabling_siren")

    @property
    def disabling_siren(self) -> bool:
        return self._data.get("disabling_siren")

    @property
    def wi_fi_connection(self) -> bool:
        return self._data.get("wi_fi_connection")

    @property
    def set_date_time(self) -> bool:
        return self._data.get("set_date_time")

    @property
    def outputs_setup(self) -> bool:
        return self._data.get("outputs_setup")


@dataclass
class PanelInfo(BaseClass):
    """Class definition of the general alarm system information."""

    # PanelInfo properties
    @property
    @title_case
    def bypass_mode(self) -> str:
        """Bypass Mode"""
        return self._data.get("bypass_mode")

    @property
    @title_case
    def current_user(self) -> str:
        """Current User"""
        return self._data.get("current_user")

    @property
    def local_wakeup_needed(self) -> bool:
        """Local Wakeup Needed"""
        return self._data.get("local_wakeup_needed")

    @property
    @title_case
    def manufacturer(self) -> str:
        """Manufacturer"""
        return self._data.get("manufacturer")

    @property
    @title_case
    def model(self) -> str:
        """Model name"""
        return self._data.get("model")

    @property
    def remote_admin_requires_user_acceptance(self) -> bool:
        """Programming requires user acceptance"""
        return self._data.get(
            "remote_switch_to_programming_mode_requires_user_acceptance"
        )

    @property
    def serial(self) -> str:
        """Serial no"""
        return self._data.get("serial")

    @property
    def partitions(self) -> list[PanelInfoPartition]:
        """Partitions info"""
        return list(
            [
                PanelInfoPartition(partition)
                for partition in self._data.get("partitions")
            ]
        )

    @property
    def features(self) -> PanelInfoFeatures:
        return PanelInfoFeatures(self._data.get("features"))


@dataclass
class Panel(BaseClass):
    """Class definition of the general alarm system information."""

    # Panel properties
    @property
    def panel_serial(self) -> str:
        return self._data.get("panel_serial")

    @property
    def alias(self) -> str:
        return self._data.get("alias")


@dataclass
class Partition(BaseClass):
    """Class definition of a partition in the alarm system."""

    # Partition properties
    @property
    def id(self) -> int:
        return self._data.get("id")

    @property
    def state(self):
        return self._data.get("state")

    @property
    def status(self) -> str:
        return self._data.get("status")

    @property
    def ready(self) -> bool:
        return self._data.get("ready")

    @property
    def options(self) -> list:
        return self._data.get("options")


@dataclass
class Process(BaseClass):
    """Class definition of a process in the alarm system."""

    # Partition properties
    @property
    def token(self) -> str:
        return self._data.get("token")

    @property
    def status(self) -> str:
        return self._data.get("status")

    @property
    def message(self) -> str:
        return self._data.get("message")

    @property
    def error(self) -> str:
        return self._data.get("error")


@dataclass
class Status(BaseClass):
    """Class definition representing the status of the alarm system."""

    # Status properties
    @property
    def connected(self) -> bool:
        return self._data.get("connected")

    @property
    def bba_connected(self) -> bool:
        return self._get_nested_key("connected_status.bba.is_connected", False)

    @property
    def bba_state(self) -> str:
        return self._get_nested_key("connected_status.bba.state", TEXT_UNKNOWN)

    @property
    def gprs_connected(self) -> bool:
        return self._get_nested_key("connected_status.gprs.is_connected", False)

    @property
    def gprs_state(self) -> str:
        return self._get_nested_key("connected_status.grps.state", TEXT_UNKNOWN)

    @property
    def discovery_completed(self) -> bool:
        return self._get_nested_key("discovery.completed")

    @property
    def discovery_stages(self) -> int:
        return self._get_nested_key("discovery.stages")

    @property
    def discovery_in_queue(self) -> int:
        return self._get_nested_key("discovery.in_queue")

    @property
    def discovery_triggered(self) -> bool:
        return self._get_nested_key("discovery.triggered")

    @property
    def partitions(self) -> list[Partition]:
        return [Partition(partition) for partition in self._data.get("partitions", [])]

    @property
    def rssi_level(self) -> int:
        return self._get_nested_key("rssi.level")

    @property
    def rssi_network(self) -> str:
        return self._get_nested_key("rssi.network")


@dataclass
class Trouble(BaseClass):
    """Class definition of a trouble in the alarm system."""

    # Trouble properties
    @property
    def device_type(self) -> str:
        """Device type."""
        return self._data.get("device_type")

    @property
    @title_case
    def location(self) -> str:
        """Location."""
        return self._data.get("location")

    @property
    def partitions(self) -> list[int]:
        """Partitions."""
        return self._data.get("partitions")

    @property
    def trouble_type(self) -> str:
        """Trouble type."""
        return self._data.get("trouble_type")

    @property
    def zone(self) -> int:
        """Zone ID."""
        return self._data.get("zone")

    @property
    @title_case
    def zone_name(self) -> str:
        """Zone type."""
        return self._data.get("zone_name")

    @property
    def zone_type(self) -> str:
        """Zone type."""
        return self._data.get("zone_type")


@dataclass
class User(BaseClass):
    """Class definition of a user in the alarm system."""

    # User properties
    @property
    def id(self) -> int:
        """User ID."""
        return self._data.get("id")

    @property
    @title_case
    def name(self) -> str:
        """User name."""
        return self._data.get("name")

    @property
    def email(self) -> str:
        """User email."""
        return self._data.get("email")

    @property
    def partitions(self) -> list[int]:
        """Device is active."""
        return self._data.get("partitions")


@dataclass
class WakeupSMS(BaseClass):
    """Class definition of a wakeup SMS in the alarm system."""

    # Wakeup SMS properties
    @property
    def phone_number(self) -> str:
        return self._data.get("phone")

    @property
    def message(self) -> str:
        return self._data.get("sms")
