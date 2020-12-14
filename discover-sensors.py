#!/usr/bin/env python

from subprocess import check_output
import sys, json

# If there's no lm-sensors installed - return empty set
try:
    a = check_output(['/usr/bin/env', 'sensors', '-A', '-u'], encoding='utf8')
except:
    print(json.dumps({'data': []}))
    sys.exit(0)

adapter = ''
sensors = []

def reset():
    return {'id': '', 'name': '', 'high': 0.0, 'crit': 0.0}

s = reset()

def add():
    global s, sensors

    if s['id'] == '':
        return

    if 'temp' in s['id']: t = 'TEMP'
    elif 'fan' in s['id']: t = 'FAN'
    elif 'power' in s['id']: t = 'POWER'
    else: t = 'UNKNOWN'

    # Assume some defaults if not provided by sensor
    if t == 'TEMP':
        if s['crit'] == 0:
            if s['high'] == 0: s['crit'] = 95.0
            else: s['crit'] = s['high'] + 10
        if s['high'] == 0: s['high'] = 80.0

    sensors.append({
        '{#ADAPTER}': adapter,
        '{#TYPE}': t,
        '{#'+t+'_NAME}': s['name'],
        '{#'+t+'_ID}': s['id'],
        '{#'+t+'_HIGH}': s['high'],
        '{#'+t+'_CRIT}': s['crit'],
    })

    s = reset()

for l in a.split('\n'):
    if l == '':
	    continue

    if not ':' in l:
        add()
        adapter = l.strip()
        continue

    if not l.startswith(' '):
        add()
        s['name'] = l.strip().rstrip(':')
        continue

    l = l.strip()
    if '_input' in l or '_average' in l:
        s['id'] =  l.split('_')[0]
        continue

    if '_max:' in l:
        s['high'] = float(l.split(':')[1].strip())
        continue

    if '_crit:' in l:
        s['crit'] = float(l.split(':')[1].strip())
        continue

add()

print(json.dumps({'data': sensors}, indent=4, sort_keys=True))
