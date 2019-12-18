"""Contains the Instrument class."""
from .note import Note, Event, SyncEvent
from . import flags

class Instrument(list):
    """Represents a single track (e.g. ExpertSingle)."""
    difficulty = flags.EXPERT
    kind = flags.GUITAR

    def __init__(self, kind=None, difficulty=None, notes=None):
        super(__class__, self).__init__()
        if kind is not None:
            if not isinstance(kind, flags.Instruments):
                raise TypeError('Expected an instrument ennum, got {}'.format(
                    type(kind).__name__
                ))
            self.kind = kind
        if difficulty is not None:
            if not isinstance(difficulty, flags.Difficulties):
                raise TypeError('Expected a difficulty enum, got {}'.format(
                    type(difficulty).__name__
                ))
            self.difficulty = difficulty
        if notes is not None:
            try:
                self.extend(notes)
            except TypeError:
                raise TypeError('expected iterable notes list, got '
                                + type(notes).__name__) from None

    def __repr__(self):
        first_notes = list(self[:5])
        return '<Instrument, first notes: {}>'.format(
            repr(first_notes)
        )

    def __str__(self):
        if self.kind == flags.EVENTS:
            result = '[' + self.kind.value + ']\n{\n'
            for note in self:
                result += str(note) + '\n'
            result += '}'
            return result
        result = '['
        result += self.difficulty.value or ''
        result += self.kind.value
        result += ']\n{\n'
        for note in self:
            result += str(note) + '\n'
        result += '}'
        return result

    @staticmethod
    def _check_note(note, kind=()):
        if not isinstance(note, (Note, Event, SyncEvent)):
            raise TypeError('Expected Note, got {.__name__}'.format(type(note)))
        if kind != () and note.kind not in kind:
            raise TypeError('Expected Note of type {} but got {}'.format(
                kind.value, note.kind.value
            ))

    def append(self, note, kind=()):
        self._check_note(note, kind)
        super(__class__, self).append(note)

    def add(self, note, kind=()):
        """Add a note to this track.
        It will be automatically inserted in the correct position.
        """
        self._check_note(note, kind)
        self.append(note)
        self.sort()
