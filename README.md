# zabbix-sensors

Zabbix template &amp; scripts to discover &amp; monitor Linux sensors

## Features

- Low-level discovery of sensors: temperature (with thresholds), fans, voltage and power
- Triggers on temperature, fans and voltage (detect stopped fan, adjustable)
- Data is gathered once as a single JSON and all other items are `Dependent` - extracted from raw JSON
- All data is gathered directly from `SysFS` - no `lm-sensors` needed to function

## Usage

- Put _sensors.conf_ in _/etc/zabbix/zabbix_agentd.d_ folder
- Put _sensors.py_ in _/etc/zabbix/scripts_ folder (or in any other, but then you'll need to adjust _sensors.conf_)
- Import & link template

## Requirements

- Python3

## Macros
- `{$SENSORS_FAN_LOW}`: Low fan speed sensor threshold
- `{$SENSORS_TEMP_CRIT}`: Crit value for temp sensors
- `{$SENSORS_TEMP_HIGH}`: High value for temp sensors
- `{$SENSORS_TEMP_HYST}`: Hysteresis for temp sensors to make sure that trigger is not firing when value oscillates over threshold and back
- `{$SENSORS_VOLTAGE_HIGH}`: Voltage high threshold
- `{$SENSORS_VOLTAGE_LOW}`: Voltage low threshold

## Update 2023-06

- Script was rewritten to gather data directly from `sysfs` instead of using `sensors` binary
- Updated templates for `6.0` and `6.4`

## Update 2020-12

- Script was rewritten from scratch to make use of new `sensors` argument `-j` to export in JSON format. If it's not supported then it'll fall back to parse raw text output of `-u` - this will stick for some time for backwards compatibility
- Move to Python3
