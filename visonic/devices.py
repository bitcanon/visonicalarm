class Device(object):
    """ Base class definition of a device in the alarm system. """

    # Property variables
    __bypass = None
    __device_number = None
    __device_type = None
    __enrollment_id = None
    __id = None
    __name = None
    __partitions = None
    __preenroll = None
    __removable = None
    __renamable = None
    __subtype = None
    __warnings = None
    __zone_type = None

    def __init__(self, bypass, device_number, device_type, enrollment_id, id,
                 name, partitions, preenroll, removable, renamable,
                 subtype, warnings, zone_type):
        """ Set the private variable values on instantiation. """

        self.__bypass = bypass
        self.__device_number = device_number
        self.__device_type = device_type
        self.__enrollment_id = enrollment_id
        self.__id = id
        self.__name = name
        self.__partitions = partitions
        self.__preenroll = preenroll
        self.__removable = removable
        self.__renamable = renamable
        self.__subtype = subtype
        self.__warnings = warnings
        self.__zone_type = zone_type

    def __str__(self):
        """ Define how the print() method should print the object. """
        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented when output to console. """

        class_name = type(self).__name__
        bypass = f"bypass = '{self.bypass}'"
        device_number = f"device_number = '{self.device_number}'"
        device_type = f"device_type = {self.device_type}"
        enrollment_id = f"enrollment_id = '{self.enrollment_id}'"
        id = f"id = '{self.id}'"
        name = f"name = '{self.name}'"
        partitions = f"partitions = '{self.partitions}'"
        preenroll = f"preenroll = {self.preenroll}"
        removable = f"removable = {self.removable}"
        renamable = f"renamable = {self.renamable}"
        subtype = f"subtype = {self.subtype}"
        warnings = f"warnings = {self.warnings}"
        zone_type = f"zone_type = {self.zone_type}"

        return f"{class_name}({bypass}, {device_number}, {device_type}, {enrollment_id}, {id}, {name}, {partitions}, {preenroll}, {removable}, {renamable}, {subtype}, {warnings}, {zone_type})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'bypass': self.bypass,
            'device_number': self.device_number,
            'device_type': self.device_type,
            'enrollment_id': self.enrollment_id,
            'id': self.id,
            'name': self.name,
            'partitions': self.partitions,
            'preenroll': self.preenroll,
            'removable': self.removable,
            'renamable': self.renamable,
            'subtype': self.subtype,
            'warnings': self.warnings,
            'zone_type': self.zone_type,
        }

    # Device properties
    @property
    def bypass(self):
        return self.__bypass

    @property
    def device_number(self):
        return self.__device_number

    @property
    def device_type(self):
        return self.__device_type

    @property
    def enrollment_id(self):
        return self.__enrollment_id

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def partitions(self):
        return self.__partitions

    @property
    def preenroll(self):
        return self.__preenroll

    @property
    def removable(self):
        return self.__removable

    @property
    def renamable(self):
        return self.__renamable

    @property
    def subtype(self):
        return self.__subtype

    @property
    def warnings(self):
        return self.__warnings

    @property
    def zone_type(self):
        return self.__zone_type


class CameraDevice(Device):
    """ Camera device class definition. """
    __location = None
    __soak = None
    __vod = None

    def __init__(self, bypass, device_number, device_type, enrollment_id, id,
                 name, partitions, preenroll, removable, renamable,
                 subtype, warnings, zone_type, location, soak, vod):
        Device.__init__(self, bypass, device_number, device_type, enrollment_id, id,
                        name, partitions, preenroll, removable, renamable,
                        subtype, warnings, zone_type)
        self.__location = location
        self.__soak = soak
        self.__vod = vod

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        value_dict = self.as_dict()
        value_dict['location'] = self.__location
        value_dict['soak'] = self.__soak
        value_dict['vod'] = self.__vod
        return object_type + ": " + str(value_dict)


class ContactDevice(Device):
    """ Contact device class definition. """

    __location = None
    __soak = None

    def __init__(self, bypass, device_number, device_type, enrollment_id, id,
                 name, partitions, preenroll, removable, renamable,
                 subtype, warnings, zone_type, location, soak):
        Device.__init__(self, bypass, device_number, device_type, enrollment_id, id,
                        name, partitions, preenroll, removable, renamable,
                        subtype, warnings, zone_type)
        self.__location = location
        self.__soak = soak

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        value_dict = self.as_dict()
        value_dict['location'] = self.__location
        value_dict['soak'] = self.__soak
        return object_type + ": " + str(value_dict)

    @property
    def state(self):
        """ Returns the current state of the contact. """
        if self.warnings is None:
            return 'CLOSED'
        for warning in self.warnings:
            if warning['type'] == 'OPENED':
                return 'OPENED'


class GenericDevice(Device):
    """ Smoke device class definition. """
    pass


class GSMDevice(Device):
    """ GSM device class definition. """
    __signal_level = None

    def __init__(self, bypass, device_number, device_type, enrollment_id, id,
                 name, partitions, preenroll, removable, renamable,
                 subtype, warnings, zone_type, signal_level):
        Device.__init__(self, bypass, device_number, device_type, enrollment_id, id,
                        name, partitions, preenroll, removable, renamable,
                        subtype, warnings, zone_type)
        self.__signal_level = signal_level

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        value_dict = self.as_dict()
        value_dict['signal_level'] = self.__signal_level
        return object_type + ": " + str(value_dict)


class KeyFobDevice(Device):
    """ KeyFob device class definition. """
    __owner_id = None
    __owner_name = None

    def __init__(self, bypass, device_number, device_type, enrollment_id, id,
                 name, partitions, preenroll, removable, renamable,
                 subtype, warnings, zone_type, owner_id, owner_name):
        Device.__init__(self, bypass, device_number, device_type, enrollment_id, id,
                        name, partitions, preenroll, removable, renamable,
                        subtype, warnings, zone_type)
        self.__owner_id = owner_id
        self.__owner_name = owner_name

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        value_dict = self.as_dict()
        value_dict['owner_id'] = self.__owner_id
        value_dict['owner_name'] = self.__owner_name
        return object_type + ": " + str(value_dict)


class PGMDevice(Device):
    """ PGM device class definition. """
    __parent_id = None
    __parent_port = None

    def __init__(self, bypass, device_number, device_type, enrollment_id, id,
                 name, partitions, preenroll, removable, renamable,
                 subtype, warnings, zone_type, parent_id, parent_port):
        Device.__init__(self, bypass, device_number, device_type, enrollment_id, id,
                        name, partitions, preenroll, removable, renamable,
                        subtype, warnings, zone_type)
        self.__parent_id = parent_id
        self.__parent_port = parent_port

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        value_dict = self.as_dict()
        value_dict['parent_id'] = self.__parent_id
        value_dict['parent_port'] = self.__parent_port
        return object_type + ": " + str(value_dict)


class SmokeDevice(Device):
    """ Smoke device class definition. """
    __location = None
    __soak = None

    def __init__(self, bypass, device_number, device_type, enrollment_id, id,
                 name, partitions, preenroll, removable, renamable,
                 subtype, warnings, zone_type, location, soak):
        Device.__init__(self, bypass, device_number, device_type, enrollment_id, id,
                        name, partitions, preenroll, removable, renamable,
                        subtype, warnings, zone_type)
        self.__location = location
        self.__soak = soak

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        value_dict = self.as_dict()
        value_dict['location'] = self.__location
        value_dict['soak'] = self.__soak
        return object_type + ": " + str(value_dict)
