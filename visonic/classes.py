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

        return f"{class_name}({device_type}, {zone_type}, {zone}, {location}, {trouble_type}, {partitions})"

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

        return f"{class_name}({id}, {type_id}, {label}, {description}, {appointment}, {datetime}, {video}, {device_type}, {zone}, {partitions})"

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

        return f"{class_name}({id}, {name}, {is_editable})"

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
