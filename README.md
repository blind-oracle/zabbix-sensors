# zabbix-sensors

Zabbix template &amp; scripts to discover &amp; monitor Linux sensors

## Features

- Low-level discovery of sensors: temperature (with thresholds), fans, voltage and power
- Triggers on temperature, fans and voltage (detect stopped fan, adjustable)

## Usage

- Put _sensors.conf_ in _/etc/zabbix/zabbix_agentd.d_ folder
- Put _sensors.py_ in _/etc/zabbix/scripts_ folder (or in any other, but then you'll need to adjust _sensors.conf_)
- Import & link template

## Requirements

- Python3

## Macros

- **{$SENSORS_CRIT}**: override discovered temperature crit thresholds
- **{$SENSORS_HIGH}**: override discovered temperature high thresholds
- **{$SENSORS_FAN_STOP_TRIG}**: set to 1 to enable fan stop trigger

## Notes

- All the needed data can be obtained directly from SysFS, but _sensors_ binary does a lot of work under the hoods to obtain the bus type etc, so it's not easy to get device names like _coretemp-isa-0000_ from SysFS manually and they're required by Zabbix's _sensor_ function
- The actual arguments to the discovery script are not used, but are there rather to fullfill Zabbix's unique key constraints
- Power moght not work for whatever reason

## Update 2023-06

- Script was rewritten to gather data directly from `sysfs` instead of using `sensors` binary
- Updated templates for `6.0` and `6.4`

## Update 2020-12

- Script was rewritten from scratch to make use of new `sensors` argument `-j` to export in JSON format. If it's not supported then it'll fall back to parse raw text output of `-u` - this will stick for some time for backwards compatibility
- Move to Python3
