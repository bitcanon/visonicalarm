class Device(object):
    """ Base class definition of a device in the alarm system. """

    # Property variables
    __id = None
    __zone = None
    __location = None
    __device_type = None
    __type = None
    __subtype = None
    __preenroll = None
    __soak = None
    __bypass = None
    __alarms = None
    __alerts = None
    __troubles = None
    __bypass_availability = None
    __partitions = None

    def __init__(self, id, zone, location, device_type, type, subtype,
                 preenroll, soak, bypass, alarms, alerts, troubles,
                 bypass_availability, partitions):
        """ Set the private variable values on instantiation. """

        self.__id = id
        self.__zone = zone
        self.__location = location
        self.__device_type = device_type
        self.__type = type
        self.__subtype = subtype
        self.__preenroll = preenroll
        self.__soak = soak
        self.__bypass = bypass
        self.__alarms = alarms
        self.__alerts = alerts
        self.__troubles = troubles
        self.__bypass_availability = bypass_availability
        self.__partitions = partitions

    def __str__(self):
        """ Define how the print() method should print the object. """
        object_type = str(type(self))
        return object_type + ": " + str(self.as_dict())

    def __repr__(self):
        """ Define how the object is represented when output to console. """

        class_name          = type(self).__name__
        id                  = f"id = '{self.id}'"
        zone                = f"zone = {self.zone}"
        location            = f"location = '{self.location}'"
        device_type         = f"device_type = '{self.device_type}'"
        type_               = f"type = '{self.type}'"
        subtype             = f"subtype = '{self.subtype}'"
        preenroll           = f"preenroll = {self.preenroll}"
        soak                = f"soak = {self.soak}"
        bypass              = f"bypass = {self.bypass}"
        alarms              = f"alarms = {self.alarms}"
        alerts              = f"alerts = {self.alerts}"
        troubles            = f"troubles = {self.troubles}"
        bypass_availability = f"bypass_availability = {self.bypass_availability}"
        partitions          = f"partitions = {str(self.partitions)}"

        return f"{class_name}({id}, {zone}, {location}, {device_type}, {type_}, {subtype}, {preenroll}, {soak}, {bypass}, {alarms}, {alerts}, {troubles}, {bypass_availability}, {partitions})"

    def as_dict(self):
        """ Return the object properties in a dictionary. """
        return {
            'id': self.id,
            'zone': self.zone,
            'location': self.location,
            'device_type': self.device_type,
            'type': self.type,
            'subtype': self.subtype,
            'preenroll': self.preenroll,
            'soak': self.soak,
            'bypass': self.bypass,
            'alarms': self.alarms,
            'alerts': self.alerts,
            'troubles': self.troubles,
            'bypass_availability': self.bypass_availability,
            'partitions': self.partitions,
        }

    # Device properties
    @property
    def id(self):
        """ Device ID. """
        return self.__id

    @property
    def zone(self):
        """ Device zone. """
        return self.__zone

    @property
    def location(self):
        """ Device location. """
        return self.__location

    @property
    def device_type(self):
        """ Device: device type. """
        return self.__device_type

    @property
    def type(self):
        """ Device type. """
        return self.__type

    @property
    def subtype(self):
        """ Device subtype. """
        return self.__subtype

    @property
    def preenroll(self):
        """ Device pre_enroll. """
        return self.__preenroll

    @property
    def soak(self):
        """ Device soak. """
        return self.__soak

    @property
    def bypass(self):
        """ Device bypassed. """
        return self.__bypass

    @property
    def alarms(self):
        """ Device alarm count. """
        return self.__alarms

    @property
    def alerts(self):
        """ Device alert count. """
        return self.__alerts

    @property
    def troubles(self):
        """ Device trouble count. """
        return self.__troubles

    @property
    def bypass_availability(self):
        """ Device bypass_availability. """
        return self.__bypass_availability

    @property
    def partitions(self):
        """ Device partitions. """
        return self.__partitions


class CameraDevice(Device):
    """ Camera device class definition. """
    pass


class ContactDevice(Device):
    """ Contact device class definition. """

    def __str__(self):
        """ Define how the print() method should print the object. """

        object_type = str(type(self))
        value_dict = self.as_dict()
        value_dict['state'] = self.state
        return object_type + ": " + str(value_dict)

    @property
    def state(self):
        """ Returns the current state of the contact. """

        if self.troubles:
            if 'OPENED' in self.troubles:
                return 'opened'
        else:
            return 'closed'


class GenericDevice(Device):
    """ Smoke device class definition. """
    pass


class SmokeDevice(Device):
    """ Smoke device class definition. """
    pass

