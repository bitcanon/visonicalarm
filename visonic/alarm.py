import json
import requests

from dateutil import parser
from dateutil.relativedelta import *

from visonic.devices import *
from visonic.core import APIv9
from visonic.exceptions import *
from visonic.classes import *
from pprint import pprint


class Setup(object):
    """ Class definition of the main alarm system. """

    # API Connection
    __api = None
    __panel_id = None

    def __init__(self, hostname, user_code, app_id, panel_id, user_email=None, user_password=None):
        """ Initiate the connection to the Visonic REST API 9.0 """
        self.__panel_id = panel_id
        self.__api = APIv9(hostname, user_code, app_id, panel_id, user_email, user_password)

    # System properties
    @property
    def api(self):
        """ Return the API for direct access. """
        return self.__api

    def rest_api_version(self):
        """ Check which versions of the API that the server support. """
        return self.api.get_version_info()['rest_versions']

    def login(self):
        """ Connect and login to the alarm system and get the static system info. """

        # Check that the server support API version 9.0.
        rest_versions = self.__api.get_version_info()['rest_versions']

        if '9.0' not in rest_versions:
            raise UnsupportedRestAPIVersionError('Rest API version 9.0 is not supported by server.')

        # Try to authenticate with provided user credentials
        if not self.__api.authenticate():
            raise AuthenticationFailedError()

        # Try to login and get a session token.
        # This will raise an exception on failure.
        if not self.__api.login():
            raise LoginFailedError()

        # Get some basic alarm panel information
        panel_info = self.get_panel_info()
        self.__system_manufacturer = panel_info.manufacturer
        self.__system_model = panel_info.model
        self.__system_serial = panel_info.serial

    def connected(self):
        """ Check if the API server is connected to the alarm panel """
        return self.get_status().connected

    def get_devices(self):
        """ Fetch all the devices that are available. """
        device_list = []

        devices = self.__api.get_devices()

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
                device_list.append(generic_device)

        return device_list

    def get_events(self, timestamp_hour_offset=2):
        """ Get the last couple of events (60 events on my system). """
        event_list = []

        events = self.__api.get_events()

        for event in events:
            # Event timestamp
            dt = parser.parse(event['datetime'])
            dt = dt + relativedelta(hours=timestamp_hour_offset)
            timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
            event['datetime'] = timestamp

            new_event = Event(
                id=event['event'],
                type_id=event['type_id'],
                label=event['label'],
                description=event['description'],
                appointment=event['appointment'],
                datetime=event['datetime'],
                video=event['video'],
                device_type=event['device_type'],
                zone=event['zone'],
                partitions=event['partitions'],
                name=event['name'],
            )

            event_list.append(new_event)

        return event_list

    def get_locations(self):
        """ Fetch the locations associated with the alarm system. """
        location_list = []
        for location in self.__api.get_locations():
            location_list.append(Location(location['hel_id'], location['name'].capitalize(), location['is_editable']))
        return location_list

    def get_panel_info(self):
        """ Fetch basic information about the alarm system. """
        gpi = self.__api.get_panel_info()

        return PanelInfo(gpi['current_user'], gpi['manufacturer'], gpi['model'], gpi['serial'])

    def get_process_status(self, process_token):
        """ Fetch the status information associated with a process token. """
        process_list = []
        for process in self.__api.get_process_status(process_token):
            new_process = Process(
                token=process['token'],
                status=process['status'],
                message=process['message'],
                error=process['error'],
            )
            process_list.append(new_process)
        return process_list

    def get_status(self):
        """ Fetch the current state of the alarm system. """

        status = self.__api.get_status()

        partition_list = []

        # Create the partitions
        for partition in status['partitions']:
            new_part = Partition(
                id=partition['id'], 
                state=partition['state'], 
                status=partition['status'], 
                ready=partition['ready'], 
                options=partition['options'],
            )
            partition_list.append(new_part)

        # Create the status
        new_status = Status(
            connected=status['connected'],
            bba_connected=status['connected_status']['bba']['is_connected'],
            bba_state=status['connected_status']['bba']['state'],
            gprs_connected=status['connected_status']['gprs']['is_connected'],
            gprs_state=status['connected_status']['gprs']['state'],
            discovery_completed=status['discovery']['completed'],
            discovery_stages=status['discovery']['stages'],
            discovery_in_queue=status['discovery']['in_queue'],
            discovery_triggered=status['discovery']['triggered'],
            partitions=partition_list,
            rssi_level=status['rssi']['level'],
            rssi_network=status['rssi']['network'],
        )

        return new_status

    def get_troubles(self):
        """ Fetch all the troubles that are available. """
        trouble_list = []
        for trouble in self.__api.get_troubles():
            new_trouble = Trouble(
                device_type=trouble['device_type'],
                location=trouble['location'],
                partitions=trouble['partitions'],
                trouble_type=trouble['trouble_type'],
                zone=trouble['zone'],
                zone_name=trouble['zone_name'],
                zone_type=trouble['zone_type'],
            )

            trouble_list.append(new_trouble)
        return trouble_list

    def get_users(self):
        """ Fetch a list of users in the alarm system. """
        users_info = self.__api.get_active_user_info()

        #print(users_info)
        user_list = []

        for user in users_info['users']:
            user = User(user['id'], user['name'], user['email'], user['partitions'])
            user_list.append(user)

        return user_list

    def arm_home(self, partition=-1):
        """ Send Arm Home command to the alarm system. """
        return self.__api.arm_home(partition)['process_token']

    def arm_away(self, partition=-1):
        """ Send Arm Away command to the alarm system. """
        return self.__api.arm_away(partition)['process_token']

    def disarm(self, partition=-1):
        """ Send Disarm command to the alarm system. """
        return self.__api.disarm(partition)['process_token']
