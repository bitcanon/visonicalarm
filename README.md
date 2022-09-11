# Visonic Alarm Library
<a href="https://www.buymeacoffee.com/bitcanon" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

## Introduction
A simple library for the Visonic PowerMaster API written in Python 3.

It's built using same technique used in the Visonic-Go app (a REST API). So if you can use the app to connect to your alarm system, the chances are you can use this library as well. I have developed and tested it with a Visonic PowerMaster-10 using a PowerLink 3 IP module.

> **Important:** The latest version of the library only has support for version 9.0 of the API running on the server side. If your alarm company still run API version 4.0 please read more below.

## API version 4.0 vs. 9.0
Finally my alarm company has upgraded their PowerManage REST API to version 9.0 so I could upgrade the Visonic Alarm library to support it.

The upgrade from API version 4.0 to 9.0 was a **major upgrade** which broke more or less the entire Visonic Alarm library. I had to rewrite large portions of the code base which means that the latest version (3.x) of Visonic Alarm for Python 3 is **not backwards compatible** with the previous versions. One of the large changes is that the API now require two sets of authentication.
1. First with **email and password** against the API server.
2. And then the **master code** between the API server and your alarm panel.

Some other changes are the way we arm and disarm the alarm system (endpoint changes). The data structures returned by the API server also differs a bit so almost all of the classes (`Status`, `Device`, `Event`, `Trouble`, `...`) have been updated to reflect these changes. See the examples in the rest of this document on how to use them.

>**Nevertheless**: the library is still really easy getting started with.

## Need support for API 4.0?
Even though the latest version of the library no longer support API version 4.0 you can still run it, simply install a previous version:
```
pip install visonicalarm==2.0.1
```
The documentation for this version can be found [here](https://github.com/bitcanon/visonicalarm/blob/master/README_API4.0.md).

## Installation
Install the latest version with pip3:
```
pip install visonicalarm
```

## Basics
### Setup
Use the same settings you are using to login to the Visonic-Go app.

```python
from visonic import alarm

hostname      = 'your.alarmcompany.com'
user_code     = '1234'
app_id        = '00000000-0000-0000-0000-000000000000'
panel_id      = '123ABC'
user_email    = "firstname.lastname@email.com"
user_password = "An.Extremely.Long.Random.and.Secure.Password!"

alarm = alarm.Setup(hostname, user_code, app_id, panel_id, user_email, user_password)
```
The `app_id` is a UUID (**U**niversally **U**nique **ID**entifier) that should be unique to each app communicating with the API server.

Create a UUID with a simple one liner:
```
python -c "import uuid; print(uuid.uuid4())"
```
This will output a UUID (for example: `e9bce150-57c9-47b9-8447-129158356c63`) that can be used to replace the zeroed `app_id`.

>1. It's important that you create an account in the app prior to setting up the library.
>2. All of the following code assume you have completed the Setup step prior to calling any of the methods.

### Pre-flight checks
Before you connect to the API server you can check which version(s) of the API your alarm company support. You do this by calling the `rest_api_version()` method.
```python
print('Supported REST API version(s): ' + ', '.join(alarm.rest_api_version()))
```

### Login
Once the library has been setup and configured, it is time to connect to the API server.
```python
alarm.login()
```
This will try to login with the configuration entered in the Setup step above.

> Note that this method will raise an exception if the login fail. See exceptions section below.

### Exceptions
All of the methods callable from the library will throw exceptions on failure. A full list of exceptions can be found [here](https://github.com/bitcanon/visonicalarm/blob/master/visonic/exceptions.py).
```python
from visonic.exceptions import *
...
try:
    alarm.login()
except BadRequestError as e:
    print(e)
```

### Printing Objects and Properties
The objects representing various entities in the alarm system can be output with the `print()` method for easy inspection of its properties.

As an example, you can output the properties of a user object by passing it to the `print()` method:
```python
print(user)
# Output: <class 'visonic.classes.User'>: {'id': 1, 'name': 'John Doe', 'email': 'john@doe.com', 'partitions': [1, 2, 3, 4, 5]}
```
Also, the properties are easily accessed from the object:
```python
print('User ID:    ' + str(user.id))
print('User Name:  ' + user.name)
print('Email:      ' + user.email)
print('Partitions: ' + str(user.partitions))
```
This is the same for all object classes in the library: Users, devices, events, locations, troubles, and so on...
## Alarm

### Alarm Panel
After calling the `login()` method it takes a few moments for the API server to connect to the alarm panel in your house. To check of the connection has been made, call the `connected()` method:
```python
if alarm.connected():
    print('Alarm Panel connected')
else:
    print('Alarm Panel disconnected')
```
>Use the `connected()` method to make sure you are connected to the alarm panel before calling arm/disarm methods to avoid exceptions.

### Devices
These are the devices connected to your alarm system (contacts, cameras, keypads, and so on).

A device is defined in the `Device` base class and, more specifically, in one of its sub-classes (`CameraDevice`, `ContactDevice`, `GenericDevice`, `GSMDevice`, `KeyFobDevice`, `PGMDevice` and `SmokeDevice`).

Get a `list` of all devices by calling the `get_devices()` method.
```python
for device in alarm.get_devices():
    print(device)
```
Output:
```
<class 'visonic.devices.ContactDevice'>: {'device_number': 14, 'device_type': 'ZONE', 'enrollment_id': '100-0305', 'id': 12340, 'name': '', 'partitions': [1], 'preenroll': False, 'removable': True, 'renamable': True, 'subtype': 'CONTACT', 'warnings': None, 'zone_type': 'PERIMETER', 'location': 'Garage', 'soak': False}
<class 'visonic.devices.CameraDevice'>:  {'device_number': 15, 'device_type': 'ZONE', 'enrollment_id': '120-2041', 'id': 12341, 'name': '', 'partitions': [1], 'preenroll': False, 'removable': True, 'renamable': True, 'subtype': 'MOTION_CAMERA', 'warnings': None, 'zone_type': 'INTERIOR_FOLLOW', 'location': 'Vardagsrum', 'soak': False, 'vod': {}}
<class 'visonic.devices.SmokeDevice'>:   {'device_number': 16, 'device_type': 'ZONE', 'enrollment_id': '300-3546', 'id': 12343, 'name': '', 'partitions': [1], 'preenroll': False, 'removable': True, 'renamable': True, 'subtype': 'SMOKE', 'warnings': None, 'zone_type': 'FIRE', 'location': 'Vardagsrum', 'soak': False}
...
```

### Events
Events are generated when the alarm system is armed, disarmed, phone line changes (GSM), and so on.

An event is defined in the `Event` class. Get a `list` of all events by calling the `get_events()` method.
```python
for event in alarm.get_events():
    print(event)
```
Output:
```
<class 'visonic.classes.Event'>: {'id': 333801, 'type_id': 89, 'label': 'DISARM', 'description': 'Disarm', 'appointment': 'Mikael Schultz', 'datetime': '2022-09-11 06:59:08', 'video': False, 'device_type': 'USER', 'zone': 1, 'partitions': [1], 'name': 'Mikael Schultz'}
<class 'visonic.classes.Event'>: {'id': 334310, 'type_id': 86, 'label': 'ARM', 'description': 'Arm Away', 'appointment': 'User 2', 'datetime': '2022-09-11 07:55:55', 'video': False, 'device_type': 'USER', 'zone': 2, 'partitions': [1], 'name': None}
...
```

### Locations
A location is defined in the `Location` class. Get a `list` of all locations by calling the `get_locations()` method.
```python
for location in alarm.get_locations():
    print(location)
```
Output:
```
<class 'visonic.classes.Location'>: {'id': 0, 'name': 'Entry', 'is_editable': False}
<class 'visonic.classes.Location'>: {'id': 1, 'name': 'Backdoor', 'is_editable': False}
...
```

### Panel Information
The general panel information is defined in the `PanelInfo` class. Get the panel information by calling the `get_panel_info()` method.
```python
panel_info = alarm.get_panel_info()
print(panel_info)
```
Output:
```
<class 'visonic.classes.PanelInfo'>: {'current_user': 'master_user', 'manufacturer': 'Visonic', 'model': 'PowerMaster 10', 'serial': '123ABC'}
```

### Status
The status of the alarm system is defined in the `Status` class. Get the current status by calling the `get_status()` method.

This method will allow you to view the current status of the PowerLink 3 IP module (`bba`), mobile module (`gprs`) as well as all partitions (defined in the `Partition` class) in the alarm system.

> If you don't have a multi partition alarm system, the `-1` partition will always be used.

```python
status = alarm.get_status()
print(status)
```
Output:
```
<class 'visonic.classes.Status'>: {'connected': True, 'bba_connected': True, 'bba_state': 'online', 'gprs_connected': False, 'gprs_state': 'online', 'discovery_completed': True, 'discovery_stages': 17, 'discovery_in_queue': 0, 'discovery_triggered': None, 'partitions': [Partition(id = -1, state = 'DISARM', status = '', ready = True, options = [])], 'rssi_level': 'ok', 'rssi_network': 'Unknown'}
```

Since the partitions are located in a list you can iterate over them like this:
```python
for partition in status.partitions:
    print(partition)
```
Output:
```
<class 'visonic.classes.Partition'>: {'id': -1, 'state': 'DISARM', 'status': '', 'ready': True, 'options': []}
```

>**Single partition system?** Just run `print(status.partitions[0].state)` to get the current arm state.

### Users
A user is defined in the `User` class. Get a `list` of all users by calling the `get_users()` method.
```python
for user in alarm.get_users():
    print(user)
```
Output:
```
<class 'visonic.classes.User'>: {'id': 1, 'name': 'John Doe', 'email': 'john@doe.com', 'partitions': [1, 2, 3, 4, 5]}
<class 'visonic.classes.User'>: {'id': 2, 'name': '', 'email': '', 'partitions': [1]}
...
```

## Arming and Disarming
There are two ways to arm you alarm system.
- **Arm Home:** This will arm your perimeter protection (often doors and windows). You can still move around inside the house.
- **Arm Away:** This will arm the entire alarm system (doors, windows, motion, cameras, etc). Moving around in the house will trigger the alarm to go off.

### Arm Home
To arm the alarm system in *home mode* just call the `arm_home()` method. 

```python
alarm.arm_home()
```
When using a multi partition alarm system, just pass the partition ID as an argument to the `arm_home()` method.
```python
alarm.arm_home(partition=2)
```

Poll the `state` property of your partition in the `get_status()` method to watch the state changing.
```python
alarm.get_status().partitions[0].state  # Output: 'HOME'
```

### Arm Away
To arm the alarm system in *away mode* just call the `arm_away()` method. 

```python
alarm.arm_away()
```
When using a multi partition alarm system, just pass the partition ID as an argument to the `arm_away()` method.
```python
alarm.arm_away(partition=2)
```

Poll the `state` property of your partition in the `get_status()` method to watch the state changing.
```python
alarm.get_status().partitions[0].state  # Output: 'AWAY'
```

### Disarm
To disarm the alarm system just call the `disarm()` method. 

```python
alarm.disarm()
```
When using a multi partition alarm system, just pass the partition ID as an argument to the `disarm()` method.
```python
alarm.disarm(partition=2)
```

Poll the `state` property of your partition in the `get_status()` method to watch the state changing.
```python
alarm.get_status().partitions[0].state  # Output: 'DISARM'
```

## Examples

Find more examples here: [/visonicalarm/examples](https://github.com/bitcanon/visonicalarm/tree/master/examples)
