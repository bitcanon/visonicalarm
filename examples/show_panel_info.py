#!/usr/bin/env python3
from visonic import alarm

hostname  = 'your.alarmcompany.com'
user_code = '1234'
user_id   = '2d978162-b00b-42a8-a5e5-b4a99100bd3a'
panel_id  = '123ABC'

alarm = alarm.Setup(hostname, user_code, user_id, panel_id)

alarm.login()
print(f"Successfully logged in to '{hostname}'.")

panel_info = alarm.get_panel_info()

print("General Panel Information:")
print(f' - Panel Name     : {panel_info.name}')
print(f' - Serial Numer   : {panel_info.serial}')
print(f' - Model          : {panel_info.model}')
print(f' - Alarm Count    : {panel_info.alarm_amount}')
print(f' - Alert Count    : {panel_info.alert_amount}')
print(f' - Trouble Count  : {panel_info.trouble_amount}')
print(f' - Camera Count   : {panel_info.camera_amount}')
print(f' - Bypass Mode    : {panel_info.bypass_mode}')
print(f' - Partition Mode : {panel_info.enabled_partition_mode}')
