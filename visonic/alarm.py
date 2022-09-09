import json
import requests

from dateutil import parser
from dateutil.relativedelta import *

from visonic.devices import *
from visonic.core import APIv4, APIv9
from visonic.exceptions import *
from visonic.classes import *
from pprint import pprint


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

    def __init__(self, hostname, user_code, user_id, panel_id, user_email=None, user_password=None, partition='ALL', api_version=9):
        """ Initiate the connection to the Visonic API """
        self.__panel_id = panel_id
        if api_version == 4:
            self.__api = APIv4(hostname, user_code, user_id, panel_id, partition)
        elif api_version == 9:
            self.__api = APIv9(hostname, user_code, user_id, panel_id, partition, user_email, user_password)

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

    def disarm(self, partition='ALL'):
        """ Send Disarm command to the alarm system. """
        self.__api.disarm(partition)

    def arm_home(self, partition='ALL'):
        """ Send Arm Home command to the alarm system. """
        self.__api.arm_home(partition)

    def arm_home_instant(self, partition='ALL'):
        """ Send Arm Home Instant command to the alarm system. """
        self.__api.arm_home_instant(partition)

    def arm_away(self, partition='ALL'):
        """ Send Arm Away command to the alarm system. """
        self.__api.arm_away(partition)

    def arm_away_instant(self, partition='ALL'):
        """ Send Arm Away Instant command to the alarm system. """
        self.__api.arm_away_instant(partition)

    def set_time(self, current_time):
        """
        Set the time of the alarm system.
        """
        result = self.__api.set_date_time(current_time)

        # The API server returns a process token that we can poll to get 
        # the result of the set_time() command.
        process_status = self.__api.get_process_status(result['process_token'])[0]

        return Process(process_status['token'], process_status['status'], process_status['message'])

    def set_user_code(self, user_code, user_id):
        """
        Set a users pin code.
        """
        result = self.__api.set_user_code(user_code, user_id)

        # The API server returns a process token that we can poll to get 
        # the result of the set_user_code() command.
        process_status = self.__api.get_process_status(result['process_token'])[0]

        return Process(process_status['token'], process_status['status'], process_status['message'])


    def get_process_status(self, process_status):
        """ 
        Check the process status of a process running on the API server.
        A process will usally go through the statuses 'start', 'handled' and 'succeeded'/'failed'

        """
        process_status = self.__api.get_process_status(process_status.token)[0]

        # Return a Process object for easy access to the process status
        return Process(process_status['token'], process_status['status'], process_status['message'])

    def get_panel_info(self):
        """ Fetch basic information about the alarm system. """

        # Get general panel information
        gpi = self.__api.get_general_panel_info()

        return PanelInfo(gpi['name'], gpi['serial'], gpi['model'], gpi['alarm_amount'], gpi['alert_amount'], 
            gpi['trouble_amount'], gpi['camera_amount'], gpi['bypass_mode'], gpi['enabled_partition_mode'])

    def get_users(self):
        """ Fetch a list of users in the alarm system. """
        users_info = self.__api.get_active_user_info()

        #print(users_info)
        user_list = []

        for user in users_info['users']:
            user = User(user['id'], user['name'], user['email'], user['partitions'])
            user_list.append(user)

        return user_list

    def login(self):
        """ Connect and login to the alarm system and get the static system info. """

        # Check that the server support API version 9.0.
        rest_versions = self.__api.get_version_info()['rest_versions']

        if '9.0' not in rest_versions:
            raise UnsupportedRestAPIVersionError('Rest API version 9.0 is not supported by server.')

        # Check that the panel ID of your device is registered with the server.
        #if not self.__api.get_panel_exists(self.__panel_id):
        #    raise InvalidPanelIDError('The Panel ID could not be found on the server.')

        # Try to authenticate with provided user credentials
        if not self.__api.authenticate():
            raise AuthenticationFailedError()

        # Try to login and get a session token.
        # This will raise an exception on failure.
        if not self.__api.login():
            raise LoginFailedError()

        # Check if logged in user is a Master User.
        #self.__is_master_user = self.__api.is_master_user()

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
            if device['subtype'] == 'CONTACT':
                contact_device = ContactDevice(
                    device_number=device['device_number'],
                    device_type=device['device_type'],
                    enrollment_id=device['enrollment_id'],
                    id=device['id'],
                    name=device['name'],
                    partitions=device['partitions'],
                    preenroll=device['preenroll'],
                    removable=device['removable'],
                    renamable=device['renamable'],
                    subtype=device['subtype'],
                    warnings=device['warnings'],
                    zone_type=device['zone_type'],
                    location=device['traits']['location']['name'].capitalize(),
                    soak=device['traits']['soak']['enabled'],
                )
                device_list.append(contact_device)
            elif device['subtype'] == 'MOTION_CAMERA':
                contact_device = CameraDevice(
                    device_number=device['device_number'],
                    device_type=device['device_type'],
                    enrollment_id=device['enrollment_id'],
                    id=device['id'],
                    name=device['name'],
                    partitions=device['partitions'],
                    preenroll=device['preenroll'],
                    removable=device['removable'],
                    renamable=device['renamable'],
                    subtype=device['subtype'],
                    warnings=device['warnings'],
                    zone_type=device['zone_type'],
                    location=device['traits']['location']['name'].capitalize(),
                    soak=device['traits']['soak']['enabled'],
                    vod=device['traits']['vod'],
                )
                device_list.append(contact_device)
            elif device['subtype'] == 'SMOKE':
                contact_device = SmokeDevice(
                    device_number=device['device_number'],
                    device_type=device['device_type'],
                    enrollment_id=device['enrollment_id'],
                    id=device['id'],
                    name=device['name'],
                    partitions=device['partitions'],
                    preenroll=device['preenroll'],
                    removable=device['removable'],
                    renamable=device['renamable'],
                    subtype=device['subtype'],
                    warnings=device['warnings'],
                    zone_type=device['zone_type'],
                    location=device['traits']['location']['name'].capitalize(),
                    soak=device['traits']['soak']['enabled'],
                )
                device_list.append(contact_device)
            elif device['subtype'] == 'BASIC_KEYFOB':
                contact_device = KeyFobDevice(
                    device_number=device['device_number'],
                    device_type=device['device_type'],
                    enrollment_id=device['enrollment_id'],
                    id=device['id'],
                    name=device['name'],
                    partitions=device['partitions'],
                    preenroll=device['preenroll'],
                    removable=device['removable'],
                    renamable=device['renamable'],
                    subtype=device['subtype'],
                    warnings=device['warnings'],
                    zone_type=device['zone_type'],
                    owner_id=device['traits']['owner']['id'],
                    owner_name=device['traits']['owner']['name'],
                )
                device_list.append(contact_device)
            elif device['device_type'] == 'GSM':
                contact_device = GSMDevice(
                    device_number=device['device_number'],
                    device_type=device['device_type'],
                    enrollment_id=device['enrollment_id'],
                    id=device['id'],
                    name=device['name'],
                    partitions=device['partitions'],
                    preenroll=device['preenroll'],
                    removable=device['removable'],
                    renamable=device['renamable'],
                    subtype=device['subtype'],
                    warnings=device['warnings'],
                    zone_type=device['zone_type'],
                    signal_level=device['traits']['signal_level']['level'],
                )
                device_list.append(contact_device)
            elif device['device_type'] == 'PGM':
                contact_device = PGMDevice(
                    device_number=device['device_number'],
                    device_type=device['device_type'],
                    enrollment_id=device['enrollment_id'],
                    id=device['id'],
                    name=device['name'],
                    partitions=device['partitions'],
                    preenroll=device['preenroll'],
                    removable=device['removable'],
                    renamable=device['renamable'],
                    subtype=device['subtype'],
                    warnings=device['warnings'],
                    zone_type=device['zone_type'],
                    parent_id=device['traits']['parent']['id'],
                    parent_port=device['traits']['parent']['port'],
                )
                device_list.append(contact_device)
            else:
                generic_device = GenericDevice(
                    device_number=device['device_number'],
                    device_type=device['device_type'],
                    enrollment_id=device['enrollment_id'],
                    id=device['id'],
                    name=device['name'],
                    partitions=device['partitions'],
                    preenroll=device['preenroll'],
                    removable=device['removable'],
                    renamable=device['renamable'],
                    subtype=device['subtype'],
                    warnings=device['warnings'],
                    zone_type=device['zone_type'],
                )
                print(f"TEST: '{device['traits']}'")
                device_list.append(generic_device)

        return device_list

    def get_status(self):
        """ Fetch the current state of the alarm system. """

        status = self.__api.get_status()

        partition_list = []

        # Create the partitions
        for part in status['partitions']:
            partition = part['id']
            active = part['status']
            state = part['state']
            ready_status = part['ready']
            new_part = Partition(partition, active, state, ready_status)

            partition_list.append(new_part)

        # Create the status
        is_connected = status['connected']
        exit_delay = -1
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

