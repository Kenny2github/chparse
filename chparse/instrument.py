from .note import Note
from . import flags

class Instrument(list):
    difficulty = flags.EXPERT
    kind = flags.GUITAR

    def __init__(self, kind=None, difficulty=None, notes=None):
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
                raise

    @staticmethod
    def _check_note(note, kind=()):
        if not isinstance(note, Note):
            raise TypeError('Expected Note, got {.__name__}'.format(type(note)))
        if kind != () and note.kind not in kind:
            raise TypeError('Expected Note of type {} but got {}'.format(
                kind.value, note.kind.value
            ))

    def append(self, note, kind=()):
        try:
            self._check_note(note, kind)
        except TypeError:
            raise

        super(type(self), self).append(note)

    def add(self, note, kind=()):
        try:
            self._check_note(note, kind)
        except TypeError:
            raise

        self.append(note)
        self.sort()
