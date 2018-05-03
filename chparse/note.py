from . import flags

class Note(object):
    time = 0
    kind = flags.NOTE
    fret = 0
    length = 0
    flags = 0

    def __init__(self, time, kind=flags.NOTE, fret=0, length=0, flag=0):
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
            result += flags.OPEN.value
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
            result2 += str(flags.TAP.value)
        elif self.is_forced:
            result2 += str(flags.FORCED.value)
        else:
            return result
        result2 += ' 0'
        result += '\n' + result2
        return result

    @property
    def is_tap(self):
        return flags.TAP in self.flag

    @property
    def is_open(self):
        return flags.OPEN in self.flag

    @property
    def is_live(self):
        return flags.GHLIVE in self.flag

    @property
    def is_forced(self):
        return (
            (flags.LIVEFORCED in self.flag)
            if (self.is_live)
            else (flags.FORCED in self.flag)
        )

class Event(object):
    time = 0
    event = ''

    def __init__(self, time, evt):
        self.time = time
        self.event = evt

    def __repr__(self):
        return '<Event {} = E {}>'.format(self.time, self.event)

    def __str__(self):
        return '  {} = E {}'.format(self.time, self.event)
