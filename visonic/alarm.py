import json
import requests

from dateutil import parser
from dateutil.relativedelta import *

from visonic.devices import *
from visonic.core import APIv4
from visonic.exceptions import *
from visonic.classes import *


class Setup(object):
    """ Class definition of the main alarm system. """

    # API Connection
    __api = None
    __panel_id = None

    # Property variables
    __system_name = None
    __system_serial = None
    __system_model = None
    __is_master_user = False

    def __init__(self, hostname, user_code, user_id, panel_id, partition='ALL'):
        """ Initiate the connection to the Visonic API """
        self.__panel_id = panel_id
        self.__api = APIv4(hostname, user_code, user_id, panel_id, partition)

    # System properties
    @property
    def serial_number(self):
        """ Serial number of the system. """
        return self.__system_serial

    @property
    def name(self):
        """ Name of the system. """
        return self.__system_name

    @property
    def model(self):
        """ Model of the system. """
        return self.__system_model

    @property
    def session_token(self):
        """ Return the current session token. """
        return self.__api.session_token

    @property
    def devices(self):
        """ A list of devices connected to the alarm system and their state. """
        return self.__system_devices

    @property
    def is_master_user(self):
        """ Check if the authenticated user is a master user. """
        return self.__is_master_user

    def rest_api_version(self):
        """ Check which versions of the API that the server support. """
        return self.__api.get_version_info()['rest_versions']

    def check_panel_id(self, panel_id):
        """ Check if the panel ID exists on the alarm server. """
        return self.__api.get_panel_exists(panel_id)

    def get_locations(self):
        """ Fetch the locations associated with the alarm system. """
        location_list = []
        for loc in self.__api.get_locations():
            location = Location(loc['hel_id'], loc['name'].capitalize(), loc['is_editable'])
            location_list.append(location)
        return location_list

    def disarm(self):
        """ Send Disarm command to the alarm system. """
        self.__api.disarm(self.__api.partition)

    def arm_home(self):
        """ Send Arm Home command to the alarm system. """
        self.__api.arm_home(self.__api.partition)

    def arm_home_instant(self):
        """ Send Arm Home Instant command to the alarm system. """
        self.__api.arm_home_instant(self.__api.partition)

    def arm_away(self):
        """ Send Arm Away command to the alarm system. """
        self.__api.arm_away(self.__api.partition)

    def arm_away_instant(self):
        """ Send Arm Away Instant command to the alarm system. """
        self.__api.arm_away_instant(self.__api.partition)

    def set_time(self, current_time):
        """
        Set the time of the alarm system.
        """
        result = self.__api.set_date_time(current_time)
        if result['process_token']:
            True
        else:
            False

    def get_panel_info(self):
        """ Fetch basic information about the alarm system. """

        # Get general panel information
        gpi = self.__api.get_general_panel_info()

        return PanelInfo(gpi['name'], gpi['serial'], gpi['model'], gpi['alarm_amount'], gpi['alert_amount'], 
            gpi['trouble_amount'], gpi['camera_amount'], gpi['bypass_mode'], gpi['enabled_partition_mode'])

    def get_users(self, override_user_names=[]):
        """ Fetch a list of users in the alarm system. """
        users_info = self.__api.get_active_user_info()

        total_users_count = users_info['total_users_count']
        active_user_ids = users_info['active_user_ids']

        user_list = []
        for user_id in range(1, total_users_count+1):
            name = 'User '+str(user_id)
            if user_id in override_user_names:
                name = override_user_names[user_id]

            user = User(user_id, name, True if user_id in active_user_ids else False)

            user_list.append(user)
        return user_list

    def login(self):
        """ Connect and login to the alarm system and get the static system info. """

        # Check that the server support API version 4.0.
        rest_versions = self.__api.get_version_info()['rest_versions']

        if '4.0' in rest_versions:
            print('Rest API version 4.0 is supported.')
        else:
            raise UnsupportedRestAPIVersionError('Rest API version 4.0 is not supported by server.')

        # Check that the panel ID of your device is registered with the server.
        if not self.__api.get_panel_exists(self.__panel_id):
            raise InvalidPanelIDError('The Panel ID could not be found on the server.')

        # Try to login and get a session token.
        # This will raise an exception on failure.
        self.__api.login()

        # Check if logged in user is a Master User.
        self.__is_master_user = self.__api.is_master_user()

    def get_events(self):
        """ Fetch all the events that are available. """
        event_list = []
        for event in self.__api.get_events():
            new_event = Event(event['event'], event['type_id'], event['label'], 
                event['description'], event['appointment'], event['datetime'], 
                event['video'], event['device_type'], event['zone'], event['partitions'])
            event_list.append(new_event)
        return event_list

    def get_troubles(self):
        """ Fetch all the troubles that are available. """
        trouble_list = []
        for trouble in self.__api.get_troubles():
            new_trouble = Trouble(trouble['device_type'], trouble['zone_type'], trouble['zone'], 
                trouble['location'], trouble['trouble_type'], trouble['partitions'])
            trouble_list.append(new_trouble)
        return trouble_list

    def get_devices(self):
        """ Fetch all the devices that are available. """
        device_list = []

        devices = self.__api.get_all_devices()

        for device in devices:
            # Capitalize for cleaner look
            if device['location']:
                device['location'] = device['location'].capitalize()

            if device['subtype'] == 'CONTACT':
                contact_device = ContactDevice(
                    id=device['device_id'],
                    zone=device['zone'],
                    location=device['location'],
                    device_type=device['device_type'],
                    type=device['type'],
                    subtype=device['subtype'],
                    preenroll=device['preenroll'],
                    soak=device['soak'],
                    bypass=device['bypass'],
                    alarms=device['alarms'],
                    alerts=device['alerts'],
                    troubles=device['troubles'],
                    bypass_availability=device['bypass_availability'],
                    partitions=device['partitions']
                )
                device_list.append(contact_device)
            elif device['subtype'] == 'MOTION_CAMERA':
                camera_device = CameraDevice(
                    id=device['device_id'],
                    zone=device['zone'],
                    location=device['location'],
                    device_type=device['device_type'],
                    type=device['type'],
                    subtype=device['subtype'],
                    preenroll=device['preenroll'],
                    soak=device['soak'],
                    bypass=device['bypass'],
                    alarms=device['alarms'],
                    alerts=device['alerts'],
                    troubles=device['troubles'],
                    bypass_availability=device['bypass_availability'],
                    partitions=device['partitions']
                )
                device_list.append(camera_device)
            elif device['subtype'] == 'SMOKE':
                smoke_device = SmokeDevice(
                    id=device['device_id'],
                    zone=device['zone'],
                    location=device['location'],
                    device_type=device['device_type'],
                    type=device['type'],
                    subtype=device['subtype'],
                    preenroll=device['preenroll'],
                    soak=device['soak'],
                    bypass=device['bypass'],
                    alarms=device['alarms'],
                    alerts=device['alerts'],
                    troubles=device['troubles'],
                    bypass_availability=device['bypass_availability'],
                    partitions=device['partitions']
                )
                device_list.append(smoke_device)
            else:
                generic_device = GenericDevice(
                    id=device['device_id'],
                    zone=device['zone'],
                    location=device['location'],
                    device_type=device['device_type'],
                    type=device['type'],
                    subtype=device['subtype'],
                    preenroll=device['preenroll'],
                    soak=device['soak'],
                    bypass=device['bypass'],
                    alarms=device['alarms'],
                    alerts=device['alerts'],
                    troubles=device['troubles'],
                    bypass_availability=device['bypass_availability'],
                    partitions=device['partitions']
                )
                device_list.append(generic_device)

        return device_list

    def get_status(self):
        """ Fetch the current state of the alarm system. """

        status = self.__api.get_status()

        partition_list = []

        # Create the partitions
        for part in status['partitions']:
            partition = part['partition']
            active = part['active']
            state = part['state']
            ready_status = part['ready_status']
            new_part = Partition(partition, active, state, ready_status)

            partition_list.append(new_part)

        # Create the status
        is_connected = status['is_connected']
        exit_delay = status['exit_delay']
        partitions = partition_list

        return Status(is_connected, exit_delay, partitions)

    def get_last_event(self, timestamp_hour_offset=0):
        """ Get the last event. """

        events = self.__api.get_events()

        print(events)

        if events is None:
            return None
        else:
            last_event = events[-1]
            data = dict()

            # Event ID
            data['event_id'] = last_event['event']

            # Determine the arm state.
            if last_event['type_id'] == 89:
                data['action'] = 'Disarm'
            elif last_event['type_id'] == 85:
                data['action'] = 'ArmHome'
            elif last_event['type_id'] == 86:
                data['action'] = 'ArmAway'
            else:
                data['action'] = 'Unknown type_id: {0}'.format(
                    str(last_event['type_id']))

            # User that caused the event
            data['user'] = last_event['appointment']

            # Event timestamp
            dt = parser.parse(last_event['datetime'])
            dt = dt + relativedelta(hours=timestamp_hour_offset)
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
            data['timestamp'] = timestamp

            return data

