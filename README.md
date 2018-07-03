# Visonic Alarm Library

## Information
A simple library for the Visonic PowerMaster API written in Python 3. It is only tested with a PowerMaster-10 using a PowerLink 3 IP module. The PowerLink 3 is a requirement for this library to work.

## Installation
Install with pip3
```
$ sudo pip3 install visonicalarm
```

## Code examples
### Current status
Getting the current alarm status. Available states are 'armed_away', 'armed_home', 'arming_exit_delay_away', 'arming_exit_delay_home' or 'disarmed'.
```python
#!/usr/bin/env python3
import visonicalarm

hostname  = 'visonic.tycomonitor.com'
user_code = '1234'
user_id   = '2d978962-daa6-4e18-a5e5-b4a99100bd3b'
panel_id  = '123456'
partition = 'P1'

visonic_alarm = visonicalarm.connect(hostname, user_code, user_id, panel_id, partition)

current_status = visonic_alarm.status()

if current_status:
    print(current_status)
```
Example output:
```
{'state': 'disarmed', 'ready_status': False, 'partition': 'ALL', 'is_connected': True, 'is_active': True, 'exit_delay': 30, 'session_token': '1a45ae0d-2d5e-4b19-9cec-f56612fa45de'}
```
