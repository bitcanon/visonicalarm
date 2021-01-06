class PanelInfo(object):
    """ Class definition of the general alarm system information. """

    def __init__(self, name, serial, model, alarm_amount, alert_amount, 
        trouble_amount, camera_amount, bypass_mode, enabled_partition_mode):
        """ Set the private variable values on instantiation. """

        self.__name = name
        self.__serial = serial
        self.__model = model
        self.__alarm_amount = alarm_amount
        self.__alert_amount = alert_amount
        self.__trouble_amount = trouble_amount
        self.__camera_amount = camera_amount
        self.__bypass_mode = bypass_mode
        self.__enabled_partition_mode = enabled_partition_mode

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name             = type(self).__name__
        name                   = f"name = '{self.name}'"
        serial                 = f"serial = '{self.serial}'"
        model                  = f"model = '{self.model}'"
        alarm_amount           = f"alarm_amount = {self.alarm_amount}"
        alert_amount           = f"alert_amount = {self.alert_amount}"
        trouble_amount         = f"trouble_amount = {self.trouble_amount}"
        camera_amount          = f"camera_amount = {self.camera_amount}"
        bypass_mode            = f"bypass_mode = '{self.bypass_mode}'"
        enabled_partition_mode = f"enabled_partition_mode = {self.enabled_partition_mode}"

        return f"{class_name}({name}, {serial}, {model}, {alarm_amount}, {alert_amount}, \
            {trouble_amount}, {camera_amount}, {bypass_mode}, {enabled_partition_mode})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'name': self.name,
            'serial': self.serial,
            'model': self.model,
            'alarm_amount': self.alarm_amount,
            'alert_amount': self.alert_amount,
            'trouble_amount': self.trouble_amount,
            'camera_amount': self.camera_amount,
            'bypass_mode': self.bypass_mode,
            'enabled_partition_mode': self.enabled_partition_mode,
        }

    # Event properties
    @property
    def name(self):
        """ Partition name. """
        return self.__name

    @property
    def serial(self):
        """ System serial number. """
        return self.__serial

    @property
    def model(self):
        """ Model name. """
        return self.__model

    @property
    def alarm_amount(self):
        """ Number of active alarms. """
        return self.__alarm_amount

    @property
    def alert_amount(self):
        """ Number of active alerts. """
        return self.__alert_amount

    @property
    def trouble_amount(self):
        """ Number of active troubles. """
        return self.__trouble_amount

    @property
    def camera_amount(self):
        """ Number of cameras. """
        return self.__camera_amount

    @property
    def bypass_mode(self):
        """ Bypass mode enabled. """
        return self.__bypass_mode

    @property
    def enabled_partition_mode(self):
        """ Partitions enabled in the alarm system. """
        return self.__enabled_partition_mode


class Partition(object):
    """ Class definition of a partition in the alarm system. """

    def __init__(self, name, active, state, ready_status):
        """ Set the private variable values on instantiation. """

        self.__name = name
        self.__active = active
        self.__state = state
        self.__ready_status = ready_status

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name   = type(self).__name__
        name         = f"name = '{self.name}'"
        active       = f"active = {self.active}"
        state        = f"state = '{self.state}'"
        ready_status = f"ready_status = {self.ready_status}"

        return f"{class_name}({name}, {active}, {state}, {ready_status})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'name': self.name,
            'active': self.active,
            'state': self.state,
            'ready_status': self.ready_status
        }

    # Event properties
    @property
    def name(self):
        """ Partition name. """
        return self.__name

    @property
    def active(self):
        """ Partition is active. """
        return self.__active

    @property
    def state(self):
        """ Current alarm state. """
        return self.__state

    @property
    def ready_status(self):
        """ The alarm system is ready to be armed. """
        return self.__ready_status


class Status(object):
    """ Class definition representing the status of the alarm system. """

    def __init__(self, is_connected, exit_delay, partitions):
        """ Set the private variable values on instantiation. """

        self.__is_connected = is_connected
        self.__exit_delay = exit_delay
        self.__partitions = partitions

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name   = type(self).__name__
        is_connected = f"is_connected = {self.is_connected}"
        exit_delay   = f"exit_delay = {self.exit_delay}"
        partitions   = f"partitions = [{str(self.partitions)}]"

        return f"{class_name}({is_connected}, {exit_delay}, {partitions})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'is_connected': self.is_connected,
            'exit_delay': self.exit_delay,
            'partitions': self.partitions
        }

    # Event properties
    @property
    def is_connected(self):
        """ Alarm system is connected. """
        return self.__is_connected

    @property
    def exit_delay(self):
        """ Exit delays configured (in seconds). """
        return self.__exit_delay

    @property
    def partitions(self):
        """ The partitions in the alarm system. """
        return self.__partitions


class Trouble(object):
    """ Class definition of a trouble in the alarm system. """

    def __init__(self, device_type, zone_type, zone, location, trouble_type, partitions):
        """ Set the private variable values on instantiation. """

        self.__device_type = device_type
        self.__zone_type = zone_type
        self.__zone = zone
        self.__location = location
        self.__trouble_type = trouble_type
        self.__partitions = partitions

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name   = type(self).__name__
        device_type  = f"device_type = '{self.device_type}'"
        zone_type    = f"zone_type = '{self.zone_type}'"
        zone         = f"zone = {self.zone}"
        location     = f"location = '{self.location}'"
        trouble_type = f"trouble_type = '{self.trouble_type}'"
        partitions   = f"partitions = {str(self.partitions)}"

        return f"{class_name}({device_type}, {zone_type}, \
            {zone}, {location}, {trouble_type}, {partitions})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'device_type': self.device_type,
            'zone_type': self.zone_type,
            'zone': self.zone,
            'location': self.location,
            'trouble_type': self.trouble_type,
            'partitions': self.partitions
        }

    # Event properties
    @property
    def device_type(self):
        """ Device type. """
        return self.__device_type

    @property
    def zone_type(self):
        """ Zone type. """
        return self.__zone_type

    @property
    def zone(self):
        """ Zone ID. """
        return self.__zone

    @property
    def location(self):
        """ Location. """
        return self.__location

    @property
    def trouble_type(self):
        """ Trouble type. """
        return self.__trouble_type

    @property
    def partitions(self):
        """ Partitions. """
        return self.__partitions


class Event(object):
    """ Class definition of an event in the alarm system. """

    def __init__(self, id, type_id, label, description, appointment, datetime, video, device_type, zone, partitions):
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

        return f"{class_name}({id}, {type_id}, {label}, {description}, {appointment}, \
            {datetime}, {video}, {device_type}, {zone}, {partitions})"

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
            'partitions': self.partitions
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


class User(object):
    """ Class definition of a user in the alarm system. """

    def __init__(self, id, name, is_active):
        """ Set the private variable values on instantiation. """

        self.__id = id
        self.__name = name
        self.__is_active = is_active

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented on output to console. """

        class_name = type(self).__name__
        id         = f"id = {self.id}"
        name       = f"name = '{self.name}'"
        is_active  = f"is_active = {self.is_active}"

        return f"{class_name}({id}, {name}, {is_active})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'id': self.id,
            'name': self.name,
            'is_active': self.is_active,
        }

   # Device properties
    @property
    def id(self):
        """ User ID. """
        return self.__id

    @property
    def name(self):
        """ User name. """
        return self.__name

    @property
    def is_active(self):
        """ Device is active. """
        return self.__is_active


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

   # Device properties
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
