import json
import requests

from dateutil import parser
from dateutil.relativedelta import *

from visonic.devices import *
from visonic.core import API
from visonic.exceptions import *
from visonic.classes import *


class Setup(object):
    """ Class definition of the main alarm system. """

    # API Connection
    __api = None

    def __init__(self, hostname, app_id, api_version='latest'):
        """ Initiate the connection to the REST API. """
        self.__api = API(hostname, app_id)
        self.set_rest_version(api_version)

    # System properties
    @property
    def api(self):
        """ Return the API for direct access. """
        return self.__api

    def access_grant(self, user_id, email):
        """ Grant a user access to the alarm panel via the API. """
        return self.__api.access_grant(user_id, email)

    def access_revoke(self, user_id):
        """ Revoke access to the alarm panel via the API for a user. """
        return self.__api.access_revoke(user_id)

    def activate_siren(self):
        """ Activate the siren (sound the alarm). """
        return self.__api.activate_siren()['process_token']

    def arm_home(self, partition=-1):
        """ Send Arm Home command to the alarm system. """
        return self.__api.arm_home(partition)['process_token']

    def arm_away(self, partition=-1):
        """ Send Arm Away command to the alarm system. """
        return self.__api.arm_away(partition)['process_token']

    def authenticate(self, email, password):
        """ Try to authenticate against the API with an email address and password. """
        return self.__api.authenticate(email, password)

    def connected(self):
        """ Check if the API server is connected to the alarm panel """
        return self.get_status().connected

    def disable_siren(self, mode='all'):
        """ Disable the siren (mute the alarm). """
        return self.__api.disable_siren(mode=mode)['process_token']

    def disarm(self, partition=-1):
        """ Send Disarm command to the alarm system. """
        return self.__api.disarm(partition)['process_token']

    def get_cameras(self):
        """ Fetch all the devices that are available. """
        camera_list = []

        cameras = self.__api.get_cameras()

        for camera in cameras:
            new_camera = Camera(
                location=camera['location'].capitalize(),
                partitions=camera['partitions'],
                preenroll=camera['preenroll'],
                preview_path=camera['preview_path'],
                status=camera['status'],
                timestamp=camera['timestamp'],
                zone=camera['zone'],
                zone_name=camera['zone_name'].capitalize(),
            )
            camera_list.append(new_camera)

        return camera_list

    def get_devices(self):
        """ Fetch all the devices that are available. """
        device_list = []

        devices = self.__api.get_devices()

        for device in devices:
            if device['subtype'] == 'CONTACT':
                contact_device = ContactDevice(
                    bypass=device['traits']['bypass']['enabled'] if 'bypass' in device['traits'] else False,
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
                    location=device['traits']['location']['name'].capitalize() if 'location' in device['traits'] else None,
                    soak=device['traits']['soak']['enabled'] if 'soak' in device['traits'] else False,
                )
                device_list.append(contact_device)
            elif device['subtype'] == 'MOTION_CAMERA':
                contact_device = CameraDevice(
                    bypass=device['traits']['bypass']['enabled'] if 'bypass' in device['traits'] else False,
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
                    location=device['traits']['location']['name'].capitalize() if 'location' in device['traits'] else None,
                    soak=device['traits']['soak']['enabled'] if 'soak' in device['traits'] else False,
                    vod=device['traits']['vod'] if 'vod' in device['traits'] else None,
                )
                device_list.append(contact_device)
            elif device['subtype'] == 'SMOKE':
                contact_device = SmokeDevice(
                    bypass=device['traits']['bypass']['enabled'] if 'bypass' in device['traits'] else False,
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
                    location=device['traits']['location']['name'].capitalize() if 'location' in device['traits'] else None,
                    soak=device['traits']['soak']['enabled'] if 'soak' in device['traits'] else False,
                )
                device_list.append(contact_device)
            elif device['subtype'] == 'BASIC_KEYFOB':
                contact_device = KeyFobDevice(
                    bypass=device['traits']['bypass']['enabled'] if 'bypass' in device['traits'] else False,
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
                    owner_id=device['traits']['owner']['id'] if 'owner' in device['traits'] else None,
                    owner_name=device['traits']['owner']['name'] if 'owner' in device['traits'] else None,
                )
                device_list.append(contact_device)
            elif device['device_type'] == 'GSM':
                contact_device = GSMDevice(
                    bypass=device['traits']['bypass']['enabled'] if 'bypass' in device['traits'] else False,
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
                    signal_level=device['traits']['signal_level']['level'] if 'signal_level' in device['traits'] else None,
                )
                device_list.append(contact_device)
            elif device['device_type'] == 'PGM':
                contact_device = PGMDevice(
                    bypass=device['traits']['bypass']['enabled'] if 'bypass' in device['traits'] else False,
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
                    parent_id=device['traits']['parent']['id'] if 'parent' in device['traits'] else None,
                    parent_port=device['traits']['parent']['port'] if 'parent' in device['traits'] else None,
                )
                device_list.append(contact_device)
            else:
                generic_device = GenericDevice(
                    bypass=device['traits']['bypass']['enabled'] if 'bypass' in device['traits'] else False,
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

    def get_feature_set(self):
        """ Fetch the locations associated with the alarm system. """
        feature_set = self.__api.get_feature_set()
        features = FeatureSet(
            events_enabled=feature_set['events']['is_enabled'],
            datetime_enabled=feature_set['datetime']['is_enabled'],
            partitions_enabled=feature_set['partitions']['is_enabled'],
            partitions_has_labels=feature_set['partitions']['is_labels_enabled'],
            partitions_max_count=feature_set['partitions']['max_partitions'],
            devices_enabled=feature_set['devices']['is_enabled'],
            sirens_can_enable=feature_set['sirens']['can_enable'],
            sirens_can_disable=feature_set['sirens']['can_disable'],
            home_automation_devices_enabled=feature_set['home_automation_devices']['is_enabled'],
            state_enabled=feature_set['state']['is_enabled'],
            state_can_set=feature_set['state']['can_set'],
            state_can_get=feature_set['state']['can_get'],
            faults_enabled=feature_set['faults']['is_enabled'],
            diagnostic_enabled=feature_set['diagnostic']['is_enabled'],
            wifi_enabled=feature_set['wifi']['is_enabled'],
        )
        return features

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

    def get_panels(self):
        """ Fetch a list of panels associated with the user. """
        panel_list = []

        for panel in self.__api.get_panels():
            new_panel = Panel(
                panel_serial=panel['panel_serial'],
                alias=panel['alias'],
            )
            panel_list.append(new_panel)

        return panel_list

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

    def get_rest_versions(self):
        """ Fetch the supported API versions. """
        return self.api.get_version_info()['rest_versions']

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
        users_info = self.__api.get_users()

        user_list = []

        for user in users_info['users']:
            user = User(user['id'], user['name'], user['email'], user['partitions'])
            user_list.append(user)

        return user_list

    def get_wakeup_sms(self):
        """ Fetch a list of users in the alarm system. """
        wakeup_sms = self.__api.get_wakeup_sms()
        sms = WakeupSMS(
            phone_number=wakeup_sms['phone'],
            message=wakeup_sms['sms'],
        )
        return sms

    def panel_add(self, alias, panel_serial, master_user_code, access_proof=None):
        """ Add a new alarm panel to the user account. A master user code is required. """
        return self.__api.panel_add(alias, panel_serial, access_proof, master_user_code)

    def panel_login(self, panel_serial, user_code):
        """ Establish a connection between the alarm panel and the API server. """
        return self.__api.panel_login(panel_serial, user_code)

    def panel_rename(self, alias, panel_serial):
        """ Rename an alarm panel. """
        return self.__api.panel_rename(alias, panel_serial)

    def panel_unlink(self, panel_serial, password, app_id):
        """ Unlink an alarm panel from the user account. """
        return self.__api.panel_unlink(panel_serial, password, app_id)

    def password_reset(self, email):
        """ Send a password reset link to the email address provided in the email argument. """
        return self.__api.password_reset(email)

    def password_reset_complete(self, reset_password_code, new_password):
        """ Complete the password reset by entering the reset code received in the email and a new password. """
        return self.__api.password_reset_complete(reset_password_code, new_password)['user_token']

    def set_bypass_zone(self, zone, set_enabled):
        """ Enabled or disable zone bypassing (for example, bypass a sensor to disable it). """
        return self.__api.set_bypass_zone(zone, set_enabled)['process_token']

    def set_name_user(self, user_id, name):
        """ Set the name of a user by user ID. """
        return self.__api.set_name('USER', user_id, name)['process_token']

    def set_rest_version(self, version='latest'):
        """ 
        Fetch the supported versions from the API server and automatically 
        configure the library to use the latest version supported by the server,
        unless overridden in the version parameter.
        """
        rest_versions = self.api.get_version_info()['rest_versions']
        rest_versions.sort(key=float)
        if version == "latest":
            self.__api.set_rest_version(rest_versions[-1])
        elif version in rest_versions:
            self.__api.set_rest_version(version)
        else:
            raise UnsupportedRestAPIVersionError(f'Rest API version {version} is not supported by server.')

    def set_user_code(self, user_id, user_code):
        """ Set the code of a user by user ID. """
        return self.__api.set_user_code(user_code, user_id)['process_token']

