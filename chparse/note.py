from . import flags

class Note(object):
    time = 0
    kind = flags.NOTE
    fret = 0
    length = 0
    flag = 0

    def __init__(self, time, kind=flags.NOTE, fret=0, length=0, flag=0):
        self.time = time
        self.kind = kind
        self.fret = fret
        self.length = length
        self.flags = flags

    def __repr__(self):
        result = '<Note: '
        result += str(self.time)
        result += ' = '
        result += self.kind.value + ' '
        if self.is_live:
            if self.fret <= 5:
                result += str(self.fret)
            elif self.is_forced:
                result += str(flags.LIVEFORCED.value)
            elif self.is_tap:
                result += str(flags.TAP.value)
            elif self.is_open:
                result += str(flags.OPEN.value)
        else:
            if self.fret <= 4:
                result += str(self.fret)
            elif self.is_forced:
                result += str(flags.FORCED.value)
            elif self.is_tap:
                result += str(flags.TAP.value)
            elif self.is_open:
                result += str(flags.OPEN.value)
        result += ' '
        result += str(self.length)
        result += '>'
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
