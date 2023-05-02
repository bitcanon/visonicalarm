__VERSION__ = "4.0.0b0"

import enum


TEXT_UNKNOWN = "Unknown"
TEXT_OPEN = "Open"
TEXT_CLOSED = "Closed"
TEXT_STATUS_HOME = "HOME"
TEXT_STATUS_AWAY = "AWAY"
TEXT_STATUS_DISARM = "DISARM"


class RequestType:
    GET = "GET"
    POST = "POST"


class VisonicURL:
    BASE = "https://{}/rest_api"  #'https://[hostname]/rest_api/[rest_version]

    ACCESS_GRANT = "access/grant"
    ACCESS_REVOKE = "access/revoke"
    ACTIVATE_SIREN = "activate_siren"
    ALARMS = "alarms"
    ALERTS = "alerts"
    APP_TYPE = "apptype"
    AUTH = "auth"
    CAMERAS = "cameras"
    DEVICES = "devices"
    DISABLE_SIREN = "disable_siren"
    EVENTS = "events"
    FEATURE_SET = "feature_set"
    HOME_AUTOMATION_DEVICES = "home_automation_devices"
    LOCATIONS = "locations"
    MAKE_VIDEO = "make_video"
    NOTIFICATIONS_EMAIL = "notifications/email"
    PANEL_LOGIN = "panel/login"
    PANEL_ADD = "panel/add"
    PANEL_INFO = "panel_info"
    PANEL_RENAME = "panel/rename"
    PANEL_UNLINK = "panel/unlink"
    PANELS = "panels"
    PASSWORD_RESET = "password/reset"
    PASSWORD_RESET_COMPLETE = "password/reset/complete"
    PROCESS_STATUS = "process_status?process_tokens={}"
    SET_BYPASS_ZONE = "set_bypass_zone"
    SET_NAME = "set_name"
    SET_STATE = "set_state"
    SET_USER_CODE = "set_user_code"
    SMART_DEVICES = "smart_devices"
    SMART_DEVICES_SETTINGS = "smart_devices/settings"
    STATUS = "status"
    TROUBLES = "troubles"
    USERS = "users"
    VERSION = "version"
    WAKEUP_SMS = "wakeup_sms"
