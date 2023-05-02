# Visonic Alarm Library
A fork from https://github.com/bitcanon/visonicalarm with much cudos for the work that has gone into this.  The fork adds further functionality and streamlines the code.  Likely it will become an async library by version 1.0.0.  It is written to support a Home Assistant integration and will change based on the need of that integration.

## Introduction
A simple library for the Visonic PowerMaster API written in Python 3.

It's built using same technique used in the Visonic-Go app (a REST API). So if you can use the phone app to connect to your alarm system, the chances are you can use this library as well. I have developed and tested it with a Visonic PowerMaster-10 and PowerMaster-30 using a PowerLink 3 IP module.

> It is probably also compatible with more devices from the PowerMaster family (PM-10, PM-30, PM-33, PM-360 and PM-360-R) but this has not been confirmed. The app also support Bentel (BW-30 and BW-64) and DSC (WP8010, WP8030 and WP8033), so these alarm system might work as well. Any feedback is welcome.

## Demo
Here is a small command-line demo application showing the most basic options that this library support. It allows you to arm and disarm the alarm system as well as show a list of devices and detailed status information.

![Alarm Control CLI Demo](https://github.com/msp/pyvisonicalarm/blob/master/docs/img/demo-cli-application.gif)

Check out the source code to the demo here: [alarm-control-demo.py](https://github.com/msp/pyvisonicalarm/blob/master/examples/alarm-control-demo.py).

## API version support

Supports PowerManage REST API to version 9.0.

## Installation

Install the latest version with `pip`:

```text
pip install pyvisonicalarm
```

## Basics

### Setup

#TODO - change this!

Use the same settings you are using when logging in to the phone app.

```python
from visonic import alarm

hostname      = 'your.alarmcompany.com'
user_code     = '1234'
app_id        = '00000000-0000-0000-0000-000000000000'
panel_id      = '123ABC'
user_email    = 'user@example.com'
user_password = 'An.Extremely.Long.Random.and.Secure.Password!'

alarm = alarm.Setup(hostname, app_id)
```
The `app_id` is a UUID (**U**niversally **U**nique **ID**entifier) that should be unique to each app communicating with the API server.

Create a UUID with a simple one liner:
```
python -c "import uuid; print(uuid.uuid4())"
```
This will output a UUID (for example: `e9bce150-57c9-47b9-8447-129158356c63`) that can be used to replace the zeroed `app_id` in the example above.

>1. It's important that you create an account in the app prior to setting up the library.
>2. All of the following code assume you have completed the Setup step prior to calling any of the methods.

### API version selection
In the `alarm.Setup()` call the library checks which version(s) the API server support and **automatically** selects the latest version by default.

The automatic version selection can be overridden by calling the `set_rest_version()` method **before** calling `authenticate()` and `login()`.
```python
alarm.set_rest_version("9.0")
```

Find out which version(s) of the API your alarm company support by calling the `get_rest_versions()` method.
```python
print('Supported REST API version(s): ' + ', '.join(alarm.get_rest_versions()))
```

### Authenticate
The next step is to **authenticate** yourself against the API server with an email address and a password. This is done using the same email and password beeing used when logging in to the phone app.
```python
alarm.authenticate(user_email, user_password)
```

> Note that this method will raise an exception if the authentication fails. See exceptions section below.

### Login
Once the authentication has succeeded, it's time to establish a connection between the API server and the alarm panel.
```python
alarm.panel_login(panel_serial, user_code)
```
The `panel_serial` is the ID of the panel (a hexadecimal number like `1A2B3C`) and the `user_code` is the master code (**it's important to use the master code**).

> Note that this method will raise an exception if the login fails. See exceptions section below.

### Exceptions
All of the methods callable from the library will throw exceptions on failure. A full list of exceptions can be found [here](https://github.com/bitcanon/visonicalarm/blob/master/visonic/exceptions.py).
```python
from visonic.exceptions import *
...
try:
    alarm.panel_login(panel_serial, user_code)
except UserCodeIncorrectError as e:
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

## Panel Initialization
Before connecting to an alarm panel it is necessary to associate it to your user account. If you want to know which panels are already associated with your account your can call the `get_panels()` method. There are methods to add, rename and delete (unlink) alarm panels.

### Add a panel
To add a new panel to your account, call the `panel_add()` method. You have to provide a valid **panel serial** number and the **master user code** in order for the process to complete successfully.
```python
alias            = 'My House'
panel_serial     = '123ABC'
master_user_code = '1234'

alarm.panel_add(alias, panel_serial, master_user_code)
```
>**Important:** You must use the **master user code** for this to work.

### Rename a panel
To rename an existing alarm panel, use the `panel_rename()` method.
```python
panel_serial = '123ABC'
alias        = 'House'

alarm.panel_rename(panel_serial, alias)
```

### Unlink a panel
To remove or unlink an alarm panel from your user account you use the `panel_unlink()` method.
```python
panel_serial  = '123ABC'
user_password = 'An.Extremely.Long.Random.and.Secure.Password!'
app_id        = '00000000-0000-0000-0000-000000000000'

alarm.panel_unlink(panel_serial, user_password, app_id)
```
>This only removes the link between your alarm system and the API server. Establish the link again by calling `panel_add()`.

## Panel Control

### Access Control
In order for a user to login to the alarm system we have to **grant** the user access to it. Also, if we want to prevent a currently active user from logging in we can **revoke** its access.

Grant access by calling `access_grant(user_id, email)`, where `user_id` is the ID of the user and `email` is the email address the user will be using to login to the system.
```python
alarm.access_grant(3, 'user@example.com')
```
Revoke access by calling `access_revoke(user_id)`, where `user_id` is the ID of the user that we no longer want to access the system.
```python
alarm.access_revoke(3)
```
>Read more about how to find user account information [here](#users).

### Alarm Panel
After calling the `login()` method it takes a few moments for the API server to connect to the alarm panel in your house. To check of the connection has been made, call the `connected()` method:
```python
if alarm.connected():
    print('Alarm Panel connected')
else:
    print('Alarm Panel disconnected')
```
>Use the `connected()` method to make sure you are connected to the alarm panel before calling arm/disarm methods to avoid exceptions.

### Cameras
A camera is defined in the `Camera` class and contains some basic information.

Get a `list` of all cameras by calling the `get_cameras()` method.
```python
for camera in alarm.get_cameras():
    print(camera)
```
Output:
```
<class 'visonic.classes.Camera'>: {'location': 'Basement', 'partitions': [1], 'preenroll': False, 'preview_path': None, 'status': 'FAILED', 'timestamp': None, 'zone': 4, 'zone_name': 'Basement'}
<class 'visonic.classes.Camera'>: {'location': 'Garage', 'partitions': [1], 'preenroll': False, 'preview_path': None, 'status': 'FAILED', 'timestamp': None, 'zone': 9, 'zone_name': 'Garage'}
...
```
>It's not fully clear what this information should be used for, but I suspect it's used for downloading images. Sadly this functions is locked on my alarm system so I can't test it.

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
#### Zone Bypassing
A device with a `device_type` of **ZONE** can be **bypassed** (which basically disables the sensor and prevent it from triggering) by calling the `set_bypass_zone(zone, set_enabled)` method. The `zone` parameter refers to the device number of the device and `set_enabled` is used to enable or disable the bypass functionality.

> This method only works if the alarm panel has zone bypassing enabled and the device supports it.

Enable zone bypass for device number 1: 
```python
token = alarm.set_bypass_zone(1, True)
```
Disable zone bypass for device number 1::
```python
token = alarm.set_bypass_zone(1, False)
```
Note that this method returns a **process token**. Check the status of the request with the method `get_process_status()`.

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

### Features
Check which features are enabled and available for interaction via the API. Among other things you can find out if your alarm system has partitions enabled and if you can turn the siren on or off.

The features of the alarm system is defined in the `FeatureSet` class. Get the available features by calling the `get_feature_set()` method.
```python
features = alarm.get_feature_set()
print(features)
```
Output:
```
<class 'visonic.classes.FeatureSet'>: {'events_enabled': True, 'datetime_enabled': False, 'partitions_enabled': False, 'partitions_has_labels': False, 'partitions_max_count': 3, 'devices_enabled': True, 'sirens_can_enable': True, 'sirens_can_disable': True, 'home_automation_devices_enabled': True, 'state_enabled': True, 'state_can_set': True, 'state_can_get': True, 'faults_enabled': True, 'diagnostic_enabled': False, 'wifi_enabled': False}
```
>**Hint:** Check `alarm.get_feature_set().partitions_enabled` to see if the alarm system is partitioned.

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

### Panels
A single alarm panel is defined in the `Panel` class. Get a `list` of panels associated with your account by calling the `get_panels()` method.
```python
for panel in alarm.get_panels():
    print(panel)
```
Output:
```
<class 'visonic.classes.Panel'>: {'panel_serial': '123ABC', 'alias': 'Home'}
<class 'visonic.classes.Panel'>: {'panel_serial': '456DEF', 'alias': 'Cabin'}
```
>Use this information to select an alarm panel to connect to when calling `login()`.

### Password
The password of a user can be reset using the API as well. This is done in two steps.
#### Step 1
Call the `password_reset(email)` method which takes an `email` address as the only parameter. A password reset email will be sent to this address in which a **password reset code** is provided.
```python
alarm.password_reset('username@example.com')
```
#### Step 2
Call the `password_reset_complete(reset_password_code, new_password)` method which takes two arguments. The `reset_password_code` is the code you received in the email message and `new_password` is the new password to set on the user account. Make sure the password is complex, otherwise an `NewPasswordStrengthError()` exception will be raised.
```python
token = alarm.password_reset_complete('ADQRSESA54', 'This.is.a.Super.Mega.s3cure.p@ssw0rd!')
print(f"User-Token: '{token}'")
```
Output:
```
User-Token: '125840b4-3028-4176-8a4f-6c705bcbbcaa'
```
>The `password_reset_complete()` method will return a new **user token** which I suspect should be used if you are changing the password of the user you are currently logged in with.

### Process Information
Some API methods return a **process token** as a return value. This makes it possible to find out how the call went and make you aware of potential errors that occured. The API methods returning a token seems to be the ones that change the state of the alarm system, such as `arm_home()`, `arm_away()` and `disarm()`.

A process is defined in the `Process` class. Get a `list` of all processes associated with a **process token** by calling the `get_process_status()` method.
```python
token = alarm.disarm()
for process in alarm.get_process_status(token):
    print(process)
```
Output:
```
<class 'visonic.classes.Process'>: {'token': '346eca73-1316-4a1e-b922-4b2061d79b71', 'status': 'start', 'message': '', 'error': None}
```

### Siren
You can turn on and off the siren connected to the alarm system by calling the `activate_siren()` and `disable_siren()` methods. Both methods return a **process token** which can be inspected with the `get_process_status()` method.
```python
alarm.activate_siren()
...
alarm.disable_siren()
```
>**Warning:** Make sure the building is empty before testing the `activate_siren()` method since it will **make a lot of noise**!

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

### Troubles
When something is in need of attention a trouble is triggered. It might be a door that's open or the control panel running on battery when a power outage occurs.

A trouble is defined in the `Trouble` class. Get a `list` of all troubles by calling the `get_troubles()` method.
```python
for trouble in alarm.get_troubles():
    print(trouble)
```
Output:
```
<class 'visonic.classes.Trouble'>: {'device_type': 'CONTROL_PANEL', 'location': None, 'partitions': [1], 'trouble_type': 'AC_FAILURE', 'zone': None, 'zone_name': None, 'zone_type': None}
<class 'visonic.classes.Trouble'>: {'device_type': 'ZONE', 'location': 'Front door', 'partitions': [1], 'trouble_type': 'OPENED', 'zone': 3, 'zone_name': '', 'zone_type': 'PERIMETER'}
```

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
#### Change the name of a user
It's possible to change the name of a user by calling the `set_name_user(user_id, name)` method. You have to provide the `id` of the user as well as the new `name`.
```python
token = alarm.set_name_user(4, 'bitcanon')
```
Note that this method returns a **process token**. Check the status of the request with the method `get_process_status()`.
```python
result = alarm.get_process_status(token)
print(result)
```
Output:
```
[Process(token = '4efc2e3a-13ef-47aa-8d25-92eb8dfa2791', status = 'succeeded', message = '', error = 'None')]
```
#### Set the user code
To set or change a user code you use the `set_user_code(user_id, user_code)` method. This method has several usages; of course to change the code of a user, but also to _add and remove a user_. There is a finite number of user accounts in the alarm panel (8 in my case) and they are considered to exist if they have a user code **not** equal to `0000`. So in short, add a user by setting a user code, and remove a user by setting the user code to `0000`.

Note that this method returns a **process token**. Check the status of the request with the method `get_process_status()`.

Add user or change user code: 
```python
token = alarm.set_user_code(4, '8675')
```
Remove user:
```python
token = alarm.set_user_code(4, '0000')
```

### Wakeup SMS
Get the information needed to send a wakeup SMS, which is defined in the `WakeupSMS` class. Get the `phone_number` and `message` required by calling the `get_wakeup_sms()` method.

```python
sms = alarm.get_wakeup_sms()
print(sms)
```
Output:
```
<class 'visonic.classes.WakeupSMS'>: {'phone_number': '+467190123456789', 'message': 'CONNECT;ABCD;AB-1;SEQ-1234;'}
```

## Arming and Disarming
There are two ways to arm your alarm system.
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

Find more examples here: [/visonicalarm/examples](https://github.com/msp1974/pyvisonicalarm/tree/master/examples)
