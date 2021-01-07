#!/usr/bin/env python3
from visonic import alarm

hostname  = 'your.alarmcompany.com'
user_code = '1234'
user_id   = '2d978162-b00b-42a8-a5e5-b4a99100bd3a'
panel_id  = '123ABC'

alarm = alarm.Setup(hostname, user_code, user_id, panel_id)

alarm.login()
print(f"Successfully logged in to '{hostname}'.")

status = alarm.get_status()

if status.is_connected:
	print(f"Alarm system ({panel_id}) is connected to the REST API server.")

	print(f"Exit delay is set to {status.exit_delay} seconds.")
	print()
	print("Available partition(s):")
	for partition in status.partitions:
		print(f" - Name   : {partition.name}")
		print(f" - Active : {partition.active}")
		print(f" - State  : {partition.state}")
		print(f" - Ready  : {partition.ready_status}")
else:
	print(f"Alarm system is offline.")

