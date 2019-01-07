# zabbix-sensors
Zabbix template &amp; scripts to discover &amp; monitor Linux sensors

Features:
* Low-level discovery of sensors: temperature (with thresholds), fans and power
* Triggers on temperature & fans (detect stopped fan, adjustable)

Usage:
* Put *sensors.conf* in */etc/zabbix/zabbix_agentd.d* folder
* Put *discover-sensors.py* in */etc/zabbix/scripts* folder (or in any other, but then you'll need to adjust *sensors.conf*)
* Import & link template

Requirements:
* **lm-sensors** installed

Macros to control behavior:
* **{$SENSORS_CRIT}**: override discovered crit thresholds
* **{$SENSORS_HIGH}**: override discovered max thresholds
* **{$SENSORS_FAN_STOP_TRIG}**: set to 1 to enable fan stop trigger

Notes:
* All the needed data can be obtained directly from SysFS, but *sensors* binary does a lot of work under the hoods to obtain the bus type etc, so it's not easy to get device names like *coretemp-isa-0000* from SysFS manually and they're required by Zabbix's *sensor* function.
* The actual arguments to the discovery script are not used, but are there rather to fullfill Zabbix's unique key constraints.
* Power sensors are not working now in Zabbix (tested in 4.0.3) for some reason (or I'm doing something wrong).
