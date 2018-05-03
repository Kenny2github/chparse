from enum import Enum, IntFlag

class NoteTypes(Enum):
    EVENT = 'E'
    NOTE = 'N'
    STAR = 'S'

EVENT = NoteTypes.EVENT
NOTE = NoteTypes.NOTE
STAR = NoteTypes.STAR

class Flags(IntFlag):
    FORCED = 5
    TAP = 6
    OPEN = 7
    GHLIVE = 10
    LIVEFORCED = 8

FORCED = Flags.FORCED
TAP = Flags.TAP
OPEN = Flags.OPEN
GHLIVE = Flags.GHLIVE
LIVEFORCED = Flags.LIVEFORCED

class Difficulties(Enum):
    EXPERT = 'Expert'
    HARD = 'Hard'
    MEDIUM = 'Medium'
    EASY = 'Easy'

EXPERT = Difficulties.EXPERT
HARD = Difficulties.HARD
MEDIUM = Difficulties.MEDIUM
EASY = Difficulties.EASY

class Instruments(Enum):
    GUITAR = 'Single'
    GUITAR_COOP = 'DoubleGuitar'
    BASS = 'DoubleBass'
    RHYTHM = 'DoubleRhythm'
    KEYBOARD = 'Keyboard'
    DRUMS = 'Drums'
    GHL_GUITAR = 'GHLGuitar'
    GHL_BASS = 'GHLBass'

GUITAR = Instruments.GUITAR
GUITAR_COOP = Instruments.GUITAR_COOP
BASS = Instruments.BASS
RHYTHM = Instruments.RHYTHM
KEYBOARD = Instruments.KEYBOARD
DRUMS = Instruments.DRUMS
GHL_GUITAR = Instruments.GHL_GUITAR
GHL_BASS = Instruments.GHL_BASS
