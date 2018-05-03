"""Enum constants for the package."""
from enum import Enum, IntFlag

class NoteTypes(Enum):
    """Different Note types."""
    EVENT = 'E'
    NOTE = 'N'
    STAR = 'S'

EVENT = NoteTypes.EVENT
NOTE = NoteTypes.NOTE
STAR = NoteTypes.STAR

class Flags(IntFlag):
    """Possible Note flags."""
    FORCED = 5
    TAP = 6
    OPEN = 7
    GHLIVE = 10
    LIVEFORCED = 8
    NONE = 0

FORCED = Flags.FORCED
TAP = Flags.TAP
OPEN = Flags.OPEN
GHLIVE = Flags.GHLIVE
LIVEFORCED = Flags.LIVEFORCED
NONE = Flags.NONE

class Difficulties(Enum):
    """Possible Instrument difficulties."""
    EXPERT = 'Expert'
    HARD = 'Hard'
    MEDIUM = 'Medium'
    EASY = 'Easy'
    NA = None

EXPERT = Difficulties.EXPERT
HARD = Difficulties.HARD
MEDIUM = Difficulties.MEDIUM
EASY = Difficulties.EASY
NA = Difficulties.NA

class Instruments(Enum):
    """Possible Instrument kinds."""
    GUITAR = 'Single'
    GUITAR_COOP = 'DoubleGuitar'
    BASS = 'DoubleBass'
    RHYTHM = 'DoubleRhythm'
    KEYBOARD = 'Keyboard'
    DRUMS = 'Drums'
    GHL_GUITAR = 'GHLGuitar'
    GHL_BASS = 'GHLBass'
    METADATA = 'Song'
    SYNC = 'SyncTrack'
    EVENTS = 'Events'

GUITAR = Instruments.GUITAR
GUITAR_COOP = Instruments.GUITAR_COOP
BASS = Instruments.BASS
RHYTHM = Instruments.RHYTHM
KEYBOARD = Instruments.KEYBOARD
DRUMS = Instruments.DRUMS
GHL_GUITAR = Instruments.GHL_GUITAR
GHL_BASS = Instruments.GHL_BASS
METADATA = Instruments.METADATA
SYNC = Instruments.SYNC
EVENTS = Instruments.EVENTS
