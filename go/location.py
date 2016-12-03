from go.utils import bold


class LocationError(Exception):
    pass


class BColor:
    RED = 91
    GREEN = 92
    YELLOW = 93
    BLUE = 94
    MAGENTA = 95


class Location(object):
    TYPES = {
        'black': bold('o', BColor.RED),
        'white': bold('o', BColor.BLUE),
        'empty': '.',
    }

    def __init__(self, type):
        if type not in self.TYPES:
            raise LocationError('Type must be one of the following: {0}'.format(
                self.TYPES.keys(),
            ))
        self.type = type

    def __eq__(self, other):
        return self.type == other.type

    def __hash__(self):
        return hash(self.type)

    def __str__(self):
        return self.TYPES[self.type]

    def __repr__(self):
        return self.type.title()
