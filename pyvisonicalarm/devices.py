from dataclasses import dataclass
from .classes import BaseClass, title_case
from .const import TEXT_CLOSED, TEXT_OPEN, TEXT_UNKNOWN


@dataclass
class Device(BaseClass):
    """Base class definition of a device in the alarm system."""

    # Device properties
    @property
    def bypass(self) -> bool | None:
        return self._get_nested_key("traits.bypass.enabled", None)

    @property
    def device_number(self) -> int:
        return self._data.get("device_number", 0)

    @property
    def device_type(self) -> str:
        return self._data.get("device_type")

    @property
    def enrollment_id(self) -> str:
        return self._data.get("enrollment_id")

    @property
    def id(self) -> int:
        return self._data.get("id", 0)

    @property
    @title_case
    def location(self) -> str:
        return self._get_nested_key("traits.location.name")

    @property
    def name(self) -> str:
        return self._data.get("name", TEXT_UNKNOWN)

    @property
    def partitions(self) -> list:
        return self._data.get("partitions", [])

    @property
    def preenroll(self) -> bool:
        return self._data.get("preenroll", False)

    @property
    def removable(self) -> bool:
        return self._data.get("removable", False)

    @property
    def renamable(self) -> bool:
        return self._data.get("renamable", False)

    @property
    def soak(self) -> bool:
        return self._get_nested_key("traits.soak.enabled", False)

    @property
    def subtype(self) -> str:
        return self._data.get("subtype", TEXT_UNKNOWN)

    @property
    def warnings(self) -> list:
        return self._data.get("warnings", [])

    @property
    def zone_type(self) -> str:
        return self._data.get("zone_type", TEXT_UNKNOWN)


@dataclass
class CameraDevice(Device):
    """Camera device class definition."""


@dataclass
class ContactDevice(Device):
    """Contact device class definition."""

    @property
    def state(self) -> str:
        """Returns the current state of the contact."""
        if not self.warnings:
            return TEXT_CLOSED
        for warning in self.warnings:
            if warning["type"] == TEXT_OPEN:
                return TEXT_OPEN


@dataclass
class MotionDevice(Device):
    """Motion sensor device class definition."""

    @property
    def brightness(self) -> int:
        return self._get_nested_key("traits.meteo_info.brightness.value")

    @property
    def temperature(self) -> float:
        return self._get_nested_key("traits.meteo_info.temperature.value")


@dataclass
class GenericDevice(Device):
    """Smoke device class definition."""


@dataclass
class GSMDevice(Device):
    """GSM device class definition."""

    @property
    def signal_level(self) -> str | None:
        return self._get_nested_key("traits.signal_level.level")


@dataclass
class KeyFobDevice(Device):
    """KeyFob device class definition."""

    @property
    def owner_id(self) -> int:
        return self._get_nested_key("traits.owner.id", 0)

    @property
    def owner_name(self) -> str:
        return self._get_nested_key("traits.owner.name", TEXT_UNKNOWN)


@dataclass
class PGMDevice(Device):
    """PGM device class definition."""

    @property
    def parent_id(self) -> int:
        return self._get_nested_key("traits.parent.id", 0)

    @property
    def parent_port(self) -> int:
        return self._get_nested_key("traits.parent.port", 0)


@dataclass
class SmokeDevice(Device):
    """Smoke device class definition."""
