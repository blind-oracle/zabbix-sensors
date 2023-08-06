#!/usr/bin/env python3

import json
import re
import os

DIR = "/sys/class/hwmon"


def read(fn):
    with open(fn) as f:
        return f.read()


def read_parse(fn):
    x = read(fn).strip()
    try:
        return int(x)
    except BaseException:
        return x


def list_hwmon():
    return sorted([f for f in os.listdir(DIR) if f.startswith("hwmon")])


def process_sensors(path):
    r = {}
    for fn in os.listdir(path):
        m = re.match(r"^(fan|in|temp|power)(\d+)_(.*)$", fn)
        if not m:
            continue

        t, i, rd = m.group(1, 2, 3)

        sens = f"{t}{i}"
        if sens not in r:
            r[sens] = {"sensor_type": t}

        r[sens][rd] = read_parse(f"{path}/{fn}")

    return r


def process_hwmon(n):
    path = f"{DIR}/{n}"
    if not os.path.exists(f"{path}/name"):
        return None, None

    name = read(f"{path}/name").strip()
    return name, process_sensors(path)


r = {}

for hwm in list_hwmon():
    name, sensors = process_hwmon(hwm)
    if not sensors:
        continue

    name = f"{hwm}-{name}"
    r[name] = sensors

print(json.dumps(r, indent=2, sort_keys=True))
