class Location(object):
    """ Class definition of a location in the alarm system. """

    # Property variables
    __id = None
    __name = None
    __is_editable = None

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
