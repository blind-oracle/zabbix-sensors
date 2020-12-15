#!/usr/bin/env python3

from subprocess import check_output, CalledProcessError, DEVNULL
import sys
import json
import re


def run(fmt):
    return check_output([
        '/usr/bin/env',
        'sensors',
        '--no-adapter',
        fmt],
        encoding='utf8',
        stderr=DEVNULL,
    )


def parse_raw():
    d = run('-u').split('\n')

    adapter = ""
    sensor = ""

    r = {}
    for l in d:
        l = l.strip()

        if re.match(r'^[^:]+$', l):
            adapter = l
            r[adapter] = {}
        elif re.match(r'^.*:$', l):
            sensor = l[:-1]
            r[adapter][sensor] = {}
        elif re.match(r'.*: \d+\.\d+$', l):
            k, v = l.split(":")
            r[adapter][sensor][k] = float(v)

    return r


def parse_json():
    return json.loads(run('-j'))


def die(e):
    print(f"There was an error executing 'sensors': {e}")
    sys.exit(1)


# Try to use JSON output, fallback to raw if that fails
try:
    r = parse_json()
except CalledProcessError:
    try:
        r = parse_raw()
    except Exception as e:
        die(e)
except Exception as e:
    die(e)

o = []
for a, av in r.items():
    for s, sv in av.items():
        t = None
        name = None
        min, crit, high = 0.0, 0.0, 0.0

        for e, v in sv.items():
            if name is None:
                name = e.split('_')[0]

            # Guess sensor type
            if t is None:
                if re.match(r'^temp\d+', e):
                    t = 'TEMP'
                elif re.match(r'^fan\d+', e):
                    t = 'FAN'
                elif re.match(r'^in\d+', e):
                    t = 'VOLTAGE'
                elif re.match(r'^power\d+', e):
                    t = 'POWER'
                else:
                    t = 'UNKNOWN'

            # Thresholds
            if e.endswith('_min'):
                min = v
            elif e.endswith('_max'):
                high = v
            elif e.endswith('_crit'):
                crit = v

        # Try to set some thresholds if not provided
        if not crit and high:
            crit = high * 1.1
        elif not high and crit:
            high = crit * 0.9
        elif not high and not crit and t == 'TEMP':
            high, crit = 80.0, 90.0

        o.append({
            '{#ADAPTER}': a,
            '{#TYPE}': t,
            '{#NAME}': s,
            '{#MIN}': min,
            '{#HIGH}': high,
            '{#CRIT}': crit,
            # ID has a type prefix because Zabbix requires unique keys even between different discoveries
            f'{{#{t}_ID}}': name,
        })

print(json.dumps(o, indent=4))
