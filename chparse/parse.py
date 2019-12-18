"""Parse (or unparse) a file to/from a Chart object!"""
import re
from .note import Note, Event, SyncEvent
from .instrument import Instrument
from .chart import Chart
from . import flags

class ParseError(Exception):
    """The chart is invalid."""
    pass

def load(fileobj):
    """Load a chart from a file object."""
    if not hasattr(fileobj, 'readline'):
        raise TypeError('fileobj must be a file object '
                        '(or something with a "readline" method)')
    instruments = []
    chart = None
    line = True
    while line:
        line = fileobj.readline().strip().strip('\ufeff')
        if not line:
            break
        if line.startswith('['):
            try:
                inst = _parse_raw_inst(fileobj, line)
            except Exception as exc:
                raise ParseError(str(exc))
            if isinstance(inst, dict): #metadata arrived
                chart = Chart(inst)
                for i in instruments:
                    chart.add_instrument(i)
            elif chart is None:
                instruments.append(inst)
            else:
                chart.add_instrument(inst)
    return chart

def _parse_raw_inst(fileobj, first_line):
    try:
        raw_name = flags.Instruments(re.match(r'\[([a-zA-Z]+)\]', first_line)
                                     .group(1))
    except ValueError:
        return _parse_inst(fileobj, first_line)
    if raw_name == flags.METADATA:
        line = ''
        data = {}
        while line != '}':
            line = fileobj.readline().strip()
            if line in '{}':
                continue
            match = re.search(r'([A-Za-z]+[A-Za-z0-9_]*)\s*=\s*(.*)', line)
            name = match.group(1)
            value = match.group(2)
            try:
                value = int(value)
            except ValueError:
                value = value.strip('"')
            data[name] = value
        return data
    if raw_name == flags.SYNC:
        inst = Instrument(kind=raw_name, difficulty=flags.NA)
        line = ''
        while line != '}':
            line = fileobj.readline().strip()
            if line in '{}':
                continue
            match = re.search(r'([0-9]+)\s*=\s*([A-Z]{1,2})\s+([0-9]+)', line)
            time = int(match.group(1))
            kind = flags.NoteTypes(match.group(2))
            value = int(match.group(3))
            inst.append(SyncEvent(time, kind, value))
            inst.sort()
        return inst
    if raw_name == flags.EVENTS:
        inst = Instrument(kind=raw_name, difficulty=flags.NA)
        line = ''
        while line != '}':
            line = fileobj.readline().strip()
            if line in '{}':
                continue
            match = re.search(r'([0-9]+)\s*=\s*'
                              + flags.EVENT.value
                              + r'\s+("?.*"?)',
                              line)
            time = int(match.group(1))
            evt = match.group(2).strip('"')
            inst.append(Event(time, evt))
            inst.sort() #just in case
        return inst
    return None

def _parse_inst(fileobj, first_line):
    raw_name = re.match(r'\[([A-Za-z]+)\]', first_line).group(1)
    difficulty, kind = re.match('([A-Z][a-z]+)([A-Z][A-Za-z]+)',
                                raw_name).groups()
    inst = Instrument(kind=flags.Instruments(kind),
                      difficulty=flags.Difficulties(difficulty))
    line = ''
    while line != '}':
        line = fileobj.readline().strip()
        if line in '{}':
            continue
        match = re.search(r'([0-9]+)\s*=\s*([A-Z])\s+'
                          + r'([0-9]+)\s+([0-9]+)', line)
        if match is not None:
            time, kind, raw_fret, length = match.groups()
            time, raw_fret, length = int(time), int(raw_fret), int(length)
            if inst.kind in (flags.GHL_GUITAR, flags.GHL_BASS):
                extraflags = {flags.GHLIVE}
            else:
                extraflags = set()
            if (flags.GHLIVE in extraflags and raw_fret <= 5) or (raw_fret <= 4):
                inst.append(Note(time, kind=flags.NoteTypes(kind),
                                 fret=raw_fret, length=length,
                                 flags=extraflags))
            elif flags.Flags(raw_fret) == flags.OPEN:
                extraflags.add(flags.OPEN)
                inst.append(Note(time, kind=flags.NoteTypes(kind),
                                 fret=0, length=length,
                                 flags=extraflags))
            else:
                inst[-1].flags |= extraflags
                inst[-1].flags.add(flags.Flags(raw_fret))
        else:
            time, kind, evt = re.search(r'([0-9]+)\s*=\s*(E)\s+"?([a-zA-Z]+)"?',
                                        line).groups()
            inst.append(Event(int(time), evt.strip('"')))
    return inst

def dump(chart, fileobj):
    """Dump a Chart to a file (or other object with a write() method)."""
    chart.dump(fileobj)
