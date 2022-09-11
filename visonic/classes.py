class Event(object):
    """ Class definition of an event in the alarm system. """

    def __init__(self, id, type_id, label, description, appointment, datetime, video, device_type, zone, partitions, name):
        """ Set the private variable values on instantiation. """

        self.__id = id
        self.__type_id = type_id
        self.__label = label
        self.__description = description
        self.__appointment = appointment
        self.__datetime = datetime
        self.__video = video
        self.__device_type = device_type
        self.__zone = zone
        self.__partitions = partitions
        self.__name = name


    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name  = type(self).__name__
        id          = f"id = {self.id}"
        type_id     = f"type_id = {self.type_id}"
        label       = f"label = '{self.label}'"
        description = f"description = '{self.description}'"
        appointment = f"appointment = '{self.appointment}'"
        datetime    = f"datetime = '{self.datetime}'"
        video       = f"video = {self.video}"
        device_type = f"device_type = '{self.device_type}'"
        zone        = f"zone = {self.zone}"
        partitions  = f"partitions = {str(self.partitions)}"
        name  = f"partitions = {str(self.name)}"

        return f"{class_name}({id}, {type_id}, {label}, {description}, {appointment}, \
            {datetime}, {video}, {device_type}, {zone}, {partitions}, {name})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'id': self.id,
            'type_id': self.type_id,
            'label': self.label,
            'description': self.description,
            'appointment': self.appointment,
            'datetime': self.datetime,
            'video': self.video,
            'device_type': self.device_type,
            'zone': self.zone,
            'partitions': self.partitions,
            'name': self.name,
        }

   # Event properties
    @property
    def id(self):
        """ User ID. """
        return self.__id

    @property
    def type_id(self):
        """ Event type ID. """
        return self.__type_id

    @property
    def label(self):
        """ Event label. """
        return self.__label

    @property
    def description(self):
        """ Event description. """
        return self.__description

    @property
    def appointment(self):
        """ Event appointment. """
        return self.__appointment

    @property
    def datetime(self):
        """ Event datetime. """
        return self.__datetime

    @property
    def video(self):
        """ Event has video. """
        return self.__video

    @property
    def device_type(self):
        """ Event device type. """
        return self.__device_type

    @property
    def zone(self):
        """ Event zone. """
        return self.__zone

    @property
    def partitions(self):
        """ Event partitions. """
        return self.__partitions

    @property
    def name(self):
        """ Event name. """
        return self.__name


class Location(object):
    """ Class definition of a location in the alarm system. """

    def __init__(self, id, name, is_editable):
        """ Set the private variable values on instantiation. """

        self.__id = id
        self.__name = name
        self.__is_editable = is_editable

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """
        
        class_name   = type(self).__name__
        id           = f"id = {self.id}"
        name         = f"name = '{self.name}'"
        is_editable  = f"is_editable = {self.is_editable}"

        return f"{class_name}({id}, {name}, {is_editable})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'id': self.id,
            'name': self.name,
            'is_editable': self.is_editable,
        }

   # Location properties
    @property
    def id(self):
        """ Device ID. """
        return self.__id

    @property
    def name(self):
        """ Device name. """
        return self.__name

    @property
    def is_editable(self):
        """ Device is editable. """
        return self.__is_editable


class PanelInfo(object):
    """ Class definition of the general alarm system information. """

    def __init__(self, current_user, manufacturer, model, serial):
        """ Set the private variable values on instantiation. """

        self.__current_user = current_user
        self.__manufacturer = manufacturer
        self.__model = model
        self.__serial = serial

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name             = type(self).__name__
        current_user           = f"current_user = '{self.current_user}'"
        manufacturer           = f"manufacturer = '{self.manufacturer}'"
        model                  = f"model = '{self.model}'"
        serial                 = f"serial = {self.serial}"

        return f"{class_name}({current_user}, {manufacturer}, {model}, {serial})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'current_user': self.current_user,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'serial': self.serial,
        }

    # PanelInfo properties
    @property
    def current_user(self):
        return self.__current_user

    @property
    def manufacturer(self):
        return self.__manufacturer

    @property
    def model(self):
        """ Model name. """
        return self.__model

    @property
    def serial(self):
        return self.__serial


class Partition(object):
    """ Class definition of a partition in the alarm system. """

    def __init__(self, id, state, status, ready, options):
        """ Set the private variable values on instantiation. """

        self.__id = id
        self.__state = state
        self.__status = status
        self.__ready = ready
        self.__options = options

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name = type(self).__name__
        id         = f"id = {self.id}"
        state      = f"state = '{self.state}'"
        status     = f"status = '{self.status}'"
        ready      = f"ready = {self.ready}"
        options    = f"options = {self.options}"

        return f"{class_name}({id}, {state}, {status}, {ready}, {options})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'id': self.id,
            'state': self.state,
            'status': self.status,
            'ready': self.ready,
            'options': self.options,
        }

    # Partition properties
    @property
    def id(self):
        return self.__id

    @property
    def state(self):
        return self.__state

    @property
    def status(self):
        return self.__status

    @property
    def ready(self):
        return self.__ready

    @property
    def options(self):
        return self.__options


class Process(object):
    """ Class definition of a process in the alarm system. """

    def __init__(self, token, status, message, error):
        """ Set the private variable values on instantiation. """

        self.__token = token
        self.__status = status
        self.__message = message
        self.__error = error

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name = type(self).__name__
        token   = f"token = '{self.token}'"
        status  = f"status = '{self.status}'"
        message = f"message = '{self.message}'"
        error   = f"error = '{self.error}'"

        return f"{class_name}({token}, {status}, {message}, {error})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'token': self.token,
            'status': self.status,
            'message': self.message,
            'error': self.error,
        }

    # Partition properties
    @property
    def token(self):
        return self.__token

    @property
    def status(self):
        return self.__status

    @property
    def message(self):
        return self.__message

    @property
    def error(self):
        return self.__error


class Status(object):
    """ Class definition representing the status of the alarm system. """

    def __init__(self, connected, bba_connected, bba_state, gprs_connected, gprs_state, discovery_completed, discovery_stages, discovery_in_queue, discovery_triggered, partitions, rssi_level, rssi_network):
        """ Set the private variable values on instantiation. """
        self.__connected = connected
        self.__bba_connected = bba_connected
        self.__bba_state = bba_state
        self.__gprs_connected = gprs_connected
        self.__gprs_state = gprs_state
        self.__discovery_completed = discovery_completed
        self.__discovery_stages = discovery_stages
        self.__discovery_in_queue = discovery_in_queue
        self.__discovery_triggered = discovery_triggered
        self.__partitions = partitions
        self.__rssi_level = rssi_level
        self.__rssi_network = rssi_network

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name = type(self).__name__
        connected = f"connected = {self.connected}"
        bba_connected = f"bba_connected = {self.bba_connected}"
        bba_state = f"bba_state = {self.bba_state}"
        gprs_connected = f"gprs_connected = {self.gprs_connected}"
        gprs_state = f"gprs_state = {self.gprs_state}"
        discovery_completed = f"discovery_completed = {self.discovery_completed}"
        discovery_stages = f"discovery_stages = {self.discovery_stages}"
        discovery_in_queue = f"discovery_in_queue = {self.discovery_in_queue}"
        discovery_triggered = f"discovery_triggered = {self.discovery_triggered}"
        partitions = f"partitions = [{str(self.partitions)}]"
        rssi_level = f"rssi_level = {self.rssi_level}"
        rssi_network = f"rssi_network = {self.rssi_network}"

        return f"{class_name}({connected}, {bba_connected}, {bba_state}, {gprs_connected}, \
                 {gprs_state}, {discovery_completed}, {discovery_stages}, {discovery_in_queue}, \
                 {discovery_triggered}, {partitions}, {rssi_level}, {rssi_network})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'connected': self.connected,
            'bba_connected': self.bba_connected,
            'bba_state': self.bba_state,
            'gprs_connected': self.gprs_connected,
            'gprs_state': self.gprs_state,
            'discovery_completed': self.discovery_completed,
            'discovery_stages': self.discovery_stages,
            'discovery_in_queue': self.discovery_in_queue,
            'discovery_triggered': self.discovery_triggered,
            'partitions': self.partitions,
            'rssi_level': self.rssi_level,
            'rssi_network': self.rssi_network,
        }

    # Status properties
    @property
    def connected(self):
        return self.__connected

    @property
    def bba_connected(self):
        return self.__bba_connected

    @property
    def bba_state(self):
        return self.__bba_state

    @property
    def gprs_connected(self):
        return self.__gprs_connected

    @property
    def gprs_state(self):
        return self.__gprs_state

    @property
    def discovery_completed(self):
        return self.__discovery_completed

    @property
    def discovery_stages(self):
        return self.__discovery_stages

    @property
    def discovery_in_queue(self):
        return self.__discovery_in_queue

    @property
    def discovery_triggered(self):
        return self.__discovery_triggered

    @property
    def partitions(self):
        return self.__partitions

    @property
    def rssi_level(self):
        return self.__rssi_level

    @property
    def rssi_network(self):
        return self.__rssi_network


class Trouble(object):
    """ Class definition of a trouble in the alarm system. """

    def __init__(self, device_type, location, partitions, trouble_type, zone, zone_name, zone_type):
        """ Set the private variable values on instantiation. """

        self.__device_type = device_type
        self.__location = location
        self.__partitions = partitions
        self.__trouble_type = trouble_type
        self.__zone = zone
        self.__zone_name = zone_name
        self.__zone_type = zone_type

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name   = type(self).__name__
        device_type  = f"device_type = '{self.device_type}'"
        location     = f"location = '{self.location}'"
        partitions   = f"partitions = {str(self.partitions)}"
        trouble_type = f"trouble_type = '{self.trouble_type}'"
        zone         = f"zone = {self.zone}"
        zone_name    = f"zone_name = '{self.zone_name}'"
        zone_type    = f"zone_type = '{self.zone_type}'"

        return f"{class_name}({device_type}, {location}, {partitions}, \
            {trouble_type}, {zone}, {zone_name}, {zone_type})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'device_type': self.device_type,
            'location': self.location,
            'partitions': self.partitions,
            'trouble_type': self.trouble_type,
            'zone': self.zone,
            'zone_name': self.zone_name,
            'zone_type': self.zone_type,
        }

    # Trouble properties
    @property
    def device_type(self):
        """ Device type. """
        return self.__device_type

    @property
    def location(self):
        """ Location. """
        return self.__location

    @property
    def partitions(self):
        """ Partitions. """
        return self.__partitions

    @property
    def trouble_type(self):
        """ Trouble type. """
        return self.__trouble_type

    @property
    def zone(self):
        """ Zone ID. """
        return self.__zone

    @property
    def zone_name(self):
        """ Zone type. """
        return self.__zone_name

    @property
    def zone_type(self):
        """ Zone type. """
        return self.__zone_type


class User(object):
    """ Class definition of a user in the alarm system. """

    def __init__(self, id, name, email, partitions):
        """ Set the private variable values on instantiation. """

        self.__id = id
        self.__name = name
        self.__email = email
        self.__partitions = partitions

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name  = type(self).__name__
        id          = f"id = {self.id}"
        name        = f"name = '{self.name}'"
        email       = f"email = '{self.name}'"
        partitions  = f"partitions = {self.is_active}"

        return f"{class_name}({id}, {name}, {email}, {partitions})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'partitions': self.partitions,
        }

   # User properties
    @property
    def id(self):
        """ User ID. """
        return self.__id

    @property
    def name(self):
        """ User name. """
        return self.__name

    @property
    def email(self):
        """ User email. """
        return self.__email

    @property
    def partitions(self):
        """ Device is active. """
        return self.__partitions
