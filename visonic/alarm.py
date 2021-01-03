import json
import requests

from dateutil import parser
from dateutil.relativedelta import *

from visonic.devices import *
from visonic.core import APIv4
from visonic.exceptions import *


class Setup(object):
    """ Class definition of the main alarm system. """

    # API Connection
    __api = None

    # Property variables
    __system_name = None
    __system_serial = None
    __system_model = None
    __system_ready = False
    __system_state = None
    __system_active = False
    __system_connected = False
    __system_devices = []
    __is_master_user = False

    def __init__(self, hostname, user_code, user_id, panel_id, partition='ALL'):
        """ Initiate the connection to the Visonic API """
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
    def ready(self):
        """ If the system is ready to be armed. If doors or windows are open
        the system can't be armed. """
        return self.__system_ready

    @property
    def state(self):
        """ Current state of the alarm system. """
        return self.__system_state

    @property
    def active(self):
        """ If the alarm system is active or not. """
        return self.__system_active

    @property
    def session_token(self):
        """ Return the current session token. """
        return self.__api.session_token

    @property
    def connected(self):
        """ If the alarm system is connected to the API server or not. """
        return self.__system_connected

    @property
    def devices(self):
        """ A list of devices connected to the alarm system and their state. """
        return self.__system_devices

    @property
    def is_master_user(self):
        """ Check if the authenticated user is a master user. """
        return self.__is_master_user

    def get_device_by_id(self, id):
        """ Get a device by its ID. """
        for device in self.__system_devices:
            if device.id == id:
                return device
        return None

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

    def sync_time(self):
        """
        Synchronize the time and date of the alarm panel with the
        date and time of the computer running the script.
        """
        self.__api.set_date_time()

    def connect(self):
        """ Connect to the alarm system and get the static system info. """

        # Check that the server support API version 4.0.
        rest_versions = self.__api.get_version_info()['rest_versions']

        if '4.0' in rest_versions:
            print('Rest API version 4.0 is supported.')
        else:
            raise UnsupportedRestAPIVersionError('Rest API version 4.0 is not supported by server.')

        # Check that the panel ID of your device is registered with the server.
        if not self.__api.get_panel_exists():
            raise InvalidPanelIDError('The Panel ID could not be found on the server.')

        # Try to login and get a session token.
        # This will raise an exception on failure.
        self.__api.login()

        # Check if logged in user is a Master User.
        self.__is_master_user = self.__api.is_master_user()

        # Get general panel information
        gpi = self.__api.get_general_panel_info()
        self.__system_name = gpi['name']
        self.__system_serial = gpi['serial']
        self.__system_model = gpi['model']

        self.update_status()

    def get_last_event(self, timestamp_hour_offset=0):
        """ Get the last event. """

        events = self.__api.get_events()

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

    def print_system_information(self):
        """ Print system information. """

        print()
        print('---------------------------------')
        print(' Connection specific information ')
        print('---------------------------------')
        print('Host:          {0}'.format(self.__api.hostname))
        print('User Code:     {0}'.format(self.__api.user_code))
        print('User ID:       {0}'.format(self.__api.user_id))
        print('Panel ID:      {0}'.format(self.__api.panel_id))
        print('Partition:     {0}'.format(self.__api.partition))
        print('Session-Token: {0}'.format(self.__api.session_token))
        print()
        print('----------------------------')
        print(' General system information ')
        print('----------------------------')
        print('Name:         {0}'.format(self.__system_name))
        print('Serial:       {0}'.format(self.__system_serial))
        print('Model:        {0}'.format(self.__system_model))
        print('Ready:        {0}'.format(self.__system_ready))
        print('State:        {0}'.format(self.__system_state))
        print('Active:       {0}'.format(self.__system_active))
        print('Connected:    {0}'.format(self.__system_connected))
        print('Master User:  {0}'.format(self.__is_master_user))

    def print_system_devices(self, detailed=False):
        """ Print information about the devices in the alarm system. """

        for index, device in enumerate(self.__system_devices):
            print()
            print('--------------')
            print(' Device #{0} '.format(index+1))
            print('--------------')
            print('ID:             {0}'.format(device.id))
            print('Zone:           {0}'.format(device.zone))
            print('Location:       {0}'.format(device.location))
            print('Device Type:    {0}'.format(device.device_type))
            print('Type:           {0}'.format(device.type))
            print('Subtype:        {0}'.format(device.subtype))
            print('Alarms:         {0}'.format(device.alarms))
            print('Alerts:         {0}'.format(device.alerts))
            print('Troubles:       {0}'.format(device.troubles))
            if detailed:
                print('Pre-enroll:     {0}'.format(device.pre_enroll))
                print('Soak:           {0}'.format(device.soak))
                print('Bypass:         {0}'.format(device.bypass))
                print('Bypass Avail.:  {0}'.format(device.bypass_availability))
                print('Partitions:     {0}'.format(device.partitions))
            if isinstance(device, ContactDevice):
                print('State:          {0}'.format(device.state))

    def print_events(self):
        """ Print a list of all recent events. """

        events = self.__api.get_events()

        for index, event in enumerate(events):
            print()
            print('--------------')
            print(' Event #{0} '.format(index+1))
            print('--------------')
            print('Event:         {0}'.format(event['event']))
            print('Type ID:       {0}'.format(event['type_id']))
            print('Label:         {0}'.format(event['label']))
            print('Description:   {0}'.format(event['description']))
            print('Appointment:   {0}'.format(event['appointment']))
            print('Datetime:      {0}'.format(event['datetime']))
            print('Video:         {0}'.format(event['video']))
            print('Device Type:   {0}'.format(event['device_type']))
            print('Zone:          {0}'.format(event['zone']))
            print('Partitions:    {0}'.format(event['partitions']))

    def update_status(self):
        """ Update all variables that are populated by the call
        to the status() API method. """

        status = self.__api.get_status()
        partition = status['partitions'][0]
        self.__system_ready = partition['ready_status']
        self.__system_state = partition['state']
        self.__system_active = partition['active']
        self.__system_connected = status['is_connected']

    def update_devices(self):
        """ Update all devices in the system with fresh information. """

        devices = self.__api.get_all_devices()

        # Clear the list since there is no way to uniquely identify the devices.
        self.__system_devices.clear()

        for device in devices:
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
                self.__system_devices.append(contact_device)
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
                self.__system_devices.append(camera_device)
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
                self.__system_devices.append(smoke_device)
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
                self.__system_devices.append(generic_device)


