"""Contains the Note class."""
from . import flags as _flags

class Note(object):
    """Represents a single note - i.e. 0 = X 0 0"""
    time = 0
    kind = _flags.NOTE
    fret = 0
    length = 0
    flags = _flags.NONE

    def __init__(self, time, kind=_flags.NOTE,
                 fret=0, length=0, flag=_flags.NONE):
        self.time = time
        self.kind = kind
        self.fret = fret
        self.length = length
        self.flags = flag

    def __repr__(self):
        result = '<Note: '
        result += str(self.time)
        result += ' = '
        result += self.kind.value + ' '
        result += str(self.fret)
        result += ' '
        result += str(self.length)
        result += ' ('
        result += repr(self.flags)
        result += ')>'
        return result

    def __str__(self):
        result = '  ' + str(self.time)
        result += ' = '
        result += self.kind.value + ' '
        if self.is_open:
            result += str(_flags.OPEN.value) #pylint: disable=no-member
        else:
            result += str(self.fret)
        result += ' '
        result += str(self.length)
        if self.is_open:
            return result
        result2 = '  ' + str(self.time)
        result2 += ' = '
        result2 += self.kind.value + ' '
        if self.is_tap:
            result2 += str(_flags.TAP.value)
        elif self.is_forced:
            result2 += str(_flags.FORCED.value)
        else: #pylint: enable=no-member
            return result
        result2 += ' 0'
        result += '\n' + result2
        return result

    def __cmp__(self, other):
        if not isinstance(other, (Note, Event, SyncEvent)):
            raise TypeError('Cannot compare Note with {.__name__}'
                            .format(type(other)))
        return (-1
                if self.time < other.time
                else (1
                      if self.time > other.time
                      else 0
                )
        )

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    @property
    def is_tap(self):
        """Return whether this Note is a tap note."""
        return _flags.TAP in self.flags

    @property
    def is_open(self):
        """Return whether this Note is an open note."""
        return _flags.OPEN in self.flags

    @property
    def is_live(self):
        """Return whether this Note is in a GH Live track."""
        return _flags.GHLIVE in self.flags

    @property
    def is_forced(self):
        """Return whether this Note is forced (HOPO flipped)."""
        return (
            (_flags.LIVEFORCED in self.flags)
            if (self.is_live)
            else (_flags.FORCED in self.flags)
        )

class Event(object): #pylint: disable=too-few-public-methods
    """Represents the special E note for events."""
    time = 0
    event = ''

    def __init__(self, time, evt):
        self.time = time
        self.event = evt

    def __repr__(self):
        return '<Event {} = E {}>'.format(self.time, self.event)

    def __str__(self):
        return '  {} = E {}'.format(self.time, self.event)

    def __cmp__(self, other):
        if not isinstance(other, (Note, Event, SyncEvent)):
            raise TypeError('Cannot compare Event with {.__name__}'
                            .format(type(other)))
        return (-1
                if self.time < other.time
                else (1
                      if self.time > other.time
                      else 0
                )
        )

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0


class SyncEvent(object):
    """Represents the special TS and B notes in the SyncTrack instrument."""
    time = 0
    kind = _flags.BPM
    value = 0

    def __init__(self, time, kind, value):
        self.time, self.kind, self.value = time, kind, value

    def __repr__(self):
        return '<SyncEvent {} = {} {}>'.format(self.time, self.kind.value,
                                               self.value)

    def __str__(self):
        return '  {} = {} {}'.format(self.time, self.kind.value, self.value)

    def __cmp__(self, other):
        if not isinstance(other, (Note, Event, SyncEvent)):
            raise TypeError('Cannot compare SyncEvent with {.__name__}'
                            .format(type(other)))
        return (-1
                if self.time < other.time
                else (1
                      if self.time > other.time
                      else 0
                )
        )

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0
