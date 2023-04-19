from dataclasses import dataclass

from .classes import BaseClass


@dataclass
class BaseDevice(BaseClass):
    """Base class definition of a device in the alarm system."""

    _device: dict

    # Device properties
    @property
    def bypass(self) -> bool:
        return (
            self._device["traits"]["bypass"]["enabled"]
            if "bypass" in self._device["traits"]
            else False
        )

    @property
    def device_number(self) -> int:
        return self._device["device_number"]

    @property
    def device_type(self) -> str:
        return self._device["device_type"]

    @property
    def enrollment_id(self) -> str:
        return self._device["enrollment_id"]

    @property
    def id(self) -> int:
        return self._device["id"]

    @property
    def location(self) -> str | None:
        return (
            self._device["traits"]["location"]["name"].capitalize()
            if "location" in self._device["traits"]
            else None
        )

    @property
    def name(self) -> str:
        return self._device["name"]

    @property
    def partitions(self) -> list:
        return self._device["partitions"]

    @property
    def preenroll(self) -> bool:
        return self._device["preenroll"]

    @property
    def removable(self) -> bool:
        return self._device["removable"]

    @property
    def renamable(self) -> bool:
        return self._device["renamable"]

    @property
    def soak(self) -> bool:
        return (
            self._device["traits"]["soak"]["enabled"]
            if "soak" in self._device["traits"]
            else False
        )

    @property
    def subtype(self) -> str:
        return self._device["subtype"]

    @property
    def warnings(self) -> list | None:
        return self._device["warnings"]

    @property
    def zone_type(self) -> str:
        return self._device["zone_type"]


@dataclass
class CameraDevice(BaseDevice):
    """Camera device class definition."""


@dataclass
class ContactDevice(BaseDevice):
    """Contact device class definition."""

    @property
    def state(self) -> str | None:
        """Returns the current state of the contact."""
        if self.warnings is None:
            return "CLOSED"
        for warning in self.warnings:
            if warning["type"] == "OPENED":
                return "OPENED"


@dataclass
class MotionDevice(BaseDevice):
    """Motion sensor device class definition."""

    @property
    def brightness(self) -> int | None:
        return (
            self._device["traits"]["meteo_info"]["brightness"]["value"]
            if "brightness" in self._device["traits"].get("meteo_info")
            else None
        )

    @property
    def temperature(self) -> float | None:
        return (
            self._device["traits"]["meteo_info"]["temperature"]["value"]
            if "temperature" in self._device["traits"].get("meteo_info")
            else None
        )


@dataclass
class GenericDevice(BaseDevice):
    """Smoke device class definition."""


@dataclass
class GSMDevice(BaseDevice):
    """GSM device class definition."""

    @property
    def signal_level(self) -> str | None:
        return (
            self._device["traits"]["signal_level"]["level"]
            if "signal_level" in self._device["traits"].get("signal_level")
            else None
        )


@dataclass
class KeyFobDevice(BaseDevice):
    """KeyFob device class definition."""

    @property
    def owner_id(self) -> int | None:
        return (
            self._device["traits"]["owner"]["id"]
            if "owner" in self._device["traits"].get("owner")
            else None
        )

    @property
    def owner_name(self) -> str | None:
        return (
            self._device["traits"]["owner"]["name"]
            if "owner" in self._device["traits"].get("owner")
            else None
        )


@dataclass
class PGMDevice(BaseDevice):
    """PGM device class definition."""

    @property
    def parent_id(self) -> int | None:
        return (
            self._device["traits"]["parent"]["id"]
            if "parent" in self._device["traits"].get("parent")
            else None
        )

    @property
    def parent_port(self) -> int | None:
        return (
            self._device["traits"]["parent"]["port"]
            if "parent" in self._device["traits"].get("parent")
            else None
        )


@dataclass
class SmokeDevice(BaseDevice):
    """Smoke device class definition."""
