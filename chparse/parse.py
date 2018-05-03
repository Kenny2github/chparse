import re
from .note import Note, Event
from .instrument import Instrument
from .chart import Chart
from . import flags

class ParseError(Exception):
    """The chart is invalid."""

def parse(filename_or_obj):
    fileobj = filename_or_obj
    if isinstance(fileobj, str):
        fileobj = open(fileobj)

def _parse_raw_inst(fileobj, first_line):
    try:
        raw_name = flags.Instruments(re.match(r'\[([a-zA-Z]+)\]', first_line)
                                 .group(1))
    except ValueError:
        return _parse_inst(fileobj, first_line)
    if raw_name == flags.METADATA:
        lines = []
        line = ''
        data = {}
        while line != '}':
            line = fileobj.read_line()
            if line in '{}':
                continue
            match = re.search(r'([A-Za-z]+)\s*=\s*(.*)', line)
            name = match.group(1)
            value = match.group(2)
            try:
                value = int(value)
            except ValueError:
                value = value.strip('"')
            data[name] = value
        return data
    if raw_name == flags.SYNC:
        return None
    if raw_name == flags.EVENTS:
        inst = Instrument(kind=raw_name)
        line = ''
        while line != '}':
            line = fileobj.read_line()
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

def _parse_inst(fileobj, first_line):
    raw_name = re.match(r'\[([A-Za-z]+)\]', first_line).group(1)
    difficulty, kind = re.match('([A-Z][a-z]+)([A-Z][A-Za-z]+)',
                                raw_name).groups()
    inst = Instrument(kind=flags.Instruments(kind),
                      difficulty=flags.Difficulties(difficulty))
    line = ''
    while line != '}':
        line = fileobj.read_line()
        if line in '{}':
            continue
        match = re.search(r'([0-9]+)\s*=\s*([A-Z])\s+\
(?:([0-9]+)\s+([0-9]+)|"?[a-zA-Z]+"?)', line)
        time, kind, raw_fret, length, evt = match.groups()
        time = int(time)
        if kind == flags.EVENT.value:
            inst.append(Event(time, evt.strip('"')))
        else:
            if inst.kind in (flags.GHL_GUITAR, flags.GHL_BASS):
                if raw_fret <= 5:
                    inst.append(Note(time, kind=flags.NoteTypes(kind),
                                     fret=int(raw_fret), length=int(length),
                                     flag=flags.GHLIVE))
                else:
                    flag = flags.Flags(int(raw_fret)) | flags.GHLIVE
                    inst[-1].flag = flag
