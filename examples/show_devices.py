#!/usr/bin/env python3
from visonic import alarm

hostname  = 'your.alarmcompany.com'
user_code = '1234'
user_id   = '2d978162-b00b-42a8-a5e5-b4a99100bd3a'
panel_id  = '123ABC'

alarm = alarm.Setup(hostname, user_code, user_id, panel_id)

alarm.login()
print(f"Successfully logged in to '{hostname}'.")
print()

print('Available device(s): ')
for device in alarm.get_devices():
	print(f"Device ID         : {device.id}")
	print(f" - Zone           : {str(device.zone)}")
	print(f" - Location       : {device.location}")
	print(f" - Type           : {device.type}")
	print(f" - Device Type    : {device.device_type}")
	print(f" - Device Subtype : {device.subtype}")
	print()
