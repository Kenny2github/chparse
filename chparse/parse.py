"""Parse (or unparse) a file to/from a Chart object!"""
import re
from .note import Note, Event
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
        line = fileobj.readline()
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
            elif isinstance(inst, tuple):
                chart._raw_sync_track = inst[1]
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
        lines = ['[' + raw_name + ']\n']
        line = ''
        while line != '}':
            line = fileobj.read_line()
            lines.append(line)
        lines = ''.join(lines)
        return (flags.SYNC, lines)
    if raw_name == flags.EVENTS:
        inst = Instrument(kind=raw_name, difficulty=flags.NA)
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
            if (inst.kind in (flags.GHL_GUITAR, flags.GHL_BASS)
                    and raw_fret <= 5) or (raw_fret <= 4):
                inst.append(Note(time, kind=flags.NoteTypes(kind),
                                 fret=int(raw_fret), length=int(length),
                                 flag=flags.GHLIVE))
            else:
                flag = flags.Flags(int(raw_fret)) | flags.GHLIVE
                inst[-1].flag = flag
    return inst

def dump(chart, fileobj):
    fileobj.write('[' + flags.METADATA.value + ']\n')
    fileobj.write('{\n')
    for key, value in chart.__dict__.items():
        fileobj.write('  {} = {}\n'.format(
            key, ((('"' + value + '"') if ' ' in value else value)
                  if isinstance(value, str)
                  else value)
        ))
    fileobj.write('}\n\n')
    fileobj.write(chart._raw_sync_track + '\n')
    for diffic in (flags.NA, flags.EASY, flags.MEDIUM,
                   flags.HARD, flags.EXPERT):
        for kind, inst in chart.instruments[diffic].items():
            fileobj.write(str(inst) + '\n\n')
