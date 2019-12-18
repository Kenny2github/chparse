"""Contains the Chart class."""
from .instrument import Instrument
from . import flags

class Chart:
    """Represents an entire chart."""
    instruments = {
        flags.EXPERT: {},
        flags.HARD: {},
        flags.MEDIUM: {},
        flags.EASY: {},
        flags.NA: {}
    }

    @property
    def events(self):
        """Events for the Chart, such as sections or lyrics

        This is a shortcut for chart.instruments[flags.NA][flags.EVENTS]
        """
        return self.instruments[flags.NA][flags.EVENTS]

    @property
    def sync_track(self):
        """The "sync track" for the Chart.
        Includes time signature and BPM events.

        This is a shortcut for chart.instruments[flags.NA][flags.SYNC]
        """
        return self.instruments[flags.NA][flags.SYNC]

    def __init__(self, metadata):
        self.__dict__.update(metadata)

    @staticmethod
    def _check_type(obj, cls):
        if not isinstance(obj, cls):
            raise TypeError('Expected {.__name__} but got {.__name__}'.format(
                cls, obj
            ))

    def add_instrument(self, inst):
        """Add an Instrument to the Chart."""
        self._check_type(inst, Instrument)
        self.instruments[inst.difficulty][inst.kind] = inst

    def remove_instrument(self, inst):
        """Remove an Instrument from the Chart."""
        self._check_type(inst, Instrument)
        del self.instruments[inst.difficulty][inst.kind]

    def dump(self, fileobj):
        """Dump the Chart to a file (or object with a write() method)."""
        fileobj.write('[' + flags.METADATA.value + ']\n')
        fileobj.write('{\n')
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            fileobj.write('  {} = {}\n'.format(
                key, (('"' + value + '"')
                      if isinstance(value, str)
                      else value)
            ))
        fileobj.write('}\n\n')
        for inst in self.instruments[flags.NA].values():
            fileobj.write(str(inst) + '\n\n')

        for dif, diffic in self.instruments.items():
            if dif == flags.NA:
                continue #already done
            for inst in diffic.values():
                fileobj.write(str(inst) + '\n\n')
