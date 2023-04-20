from visonic.devices import (
    CameraDevice,
    ContactDevice,
    GSMDevice,
    GenericDevice,
    KeyFobDevice,
    MotionDevice,
    PGMDevice,
    SmokeDevice,
)


TEXT_UNKNOWN = "Unknown"
TEXT_OPEN = "Open"
TEXT_CLOSED = "Closed"

DEVICE_TYPES = {
    "GSM": GSMDevice,
    "PGM": PGMDevice,
}

DEVICE_SUBTYPES = {
    "CONTACT": ContactDevice,
    "MC303_VANISH": ContactDevice,
    "MOTION_CAMERA": CameraDevice,
    "SMOKE": SmokeDevice,
    "BASIC_KEYFOB": KeyFobDevice,
    "KEYFOB_ARM_LED": KeyFobDevice,
    "FLAT_PIR_SMART": MotionDevice,
    "WL_SIREN": GenericDevice,
}
