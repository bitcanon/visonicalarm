# Visonic Alarm Library

## Introduction
A simple library for the Visonic PowerMaster API written in Python 3.

It is built using same technique used in the Visonic-Go app. So if you can use the app to connect to your alarm system, the chances are you can use this library as well. I have developed and tested it with a Visonic PowerMaster-10 using a PowerLink 3 IP module.

> The library currently only support verion 4.0 of the API running on the server side. As of now that is the only version my alarm company is supporting and thus I have no other version to develop against. It seems that some alarm companies has been rolling out version 8.0 of the API (requiring username and password authentication), which will be supported in the future.

## Installation
Install the latest version with pip3:
```
$ pip3 install visonicalarm
```

## Basics
### Setup
Use the same settings you are using to login to the Visonic-Go app.
```python
from visonic import alarm

hostname  = 'your.alarmcompany.com'
user_code = '1234'
user_id   = '2d978962-daa6-4e18-a5e5-b4a99100bd3b'
panel_id  = '123ABC'

alarm = alarm.Setup(hostname, user_code, user_id, panel_id)
```
The `user_id` is a GUID (Globally Unique IDentifier) that should be unique to each app communicating with the API server. You can get a GUID from [https://www.guidgen.com](https://www.guidgen.com) and paste into your code.

>All of the following code assume you have completed the Setup step prior to calling any of the methods.

### Pre-flight checks
Before you connect to the API server you can check which version(s) of the API your alarm company support. You do this by calling the `rest_api_version()` method.
```python
print('Supported REST API version(s): ' + ', '.join(alarm.rest_api_version()))
```

You can also check if your alarm panel is registered with the alarm server by calling the `check_panel_id()` method.
```python
if alarm.check_panel_id(panel_id):
    print("Panel is registed with the API server.")
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
try:
    alarm.login()
except ConnectionTimeoutError:
    print('Connection to host timed out.')
except NotRestAPIError:
    print('The host is not a REST API server.')
except UnsupportedRestAPIVersionError:
    print('Unsupported REST API version.')
except InvalidPanelIDError:
    print('The Panel ID is not registered with the API server.')
except InvalidUserCodeError:
    print('The user code supplied is invalid.')
except LoginAttemptsLimitReachedError:
    print('To many login attempts. Please wait a few minutes and try again.')
```

### Print Objects
The objects representing various entities in the alarm system can be output with the `print()` method for easy inspection of its properties.

As an example, you can output the properties of a user object by passing it to the `print()` method:
```python
print(user)
# Output: <class 'visonic.classes.User'>: {'id': 1, 'name': 'User 1', 'is_active': True}
```
Also, the properties are easily accessed from the user object:
```python
print('User ID:   ' + user.id)
print('User Name: ' + user.name)
print('Is Active: ' + str(user.is_active))
```
## Alarm

### Locations
A location is defined in the `Location` class. Get a list of all locations by calling the `get_locations()` method.
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

### Users
A user is defined in the `User` class. Get a list of all users by calling the `get_users()` method.
```python
for user in alarm.get_users():
    print(user)
```
Output:
```
<class 'visonic.classes.User'>: {'id': 1, 'name': 'User 1', 'is_active': True}
<class 'visonic.classes.User'>: {'id': 2, 'name': 'User 2', 'is_active': False}
...
```

You can override the names of the users by calling the `get_users()` method with a dictionary mapping and ID with a name.
```python
for user in alarm.get_users({1: 'Bob', 2: 'Alice'}):
    print(user)
```
Output:
```
<class 'visonic.classes.User'>: {'id': 1, 'name': 'Bob', 'is_active': True}
<class 'visonic.classes.User'>: {'id': 2, 'name': 'Alice', 'is_active': False}
<class 'visonic.classes.User'>: {'id': 3, 'name': 'User 3', 'is_active': False}
...
```

### Events
Events are generated when the alarm system is armed, disarmed, phone line changes (GSM), and so on.

An event is defined in the `Event` class. Get a list of all events by calling the `get_events()` method.
```python
for event in alarm.get_events():
    print(event)
```
Output:
```
<class 'visonic.classes.Event'>: {'id': 19000001, 'type_id': 86, 'label': 'ARM', 'description': 'Armed away', 'appointment': 'User 1', 'datetime': '2000-01-01 06:00:00', 'video': False, 'device_type': 'USER', 'zone': 1, 'partitions': ['ALL']}
<class 'visonic.classes.Event'>: {'id': 19000002, 'type_id': 89, 'label': 'DISARM', 'description': 'Disarm', 'appointment': 'User 1', 'datetime': '2000-01-01 07:00:00', 'video': False, 'device_type': 'USER', 'zone': 1, 'partitions': ['ALL']}
...
```

## System

### Set the time
You can update the time of the alarm system by calling the `set_time()` method. It accepts a datetime object that will be used to set the time.
```python
try:
    alarm.set_time(datetime.now())
except PermissionDeniedError:
    print('Permission denied. Please login using a master user and try again.')
```
> Note: You must be logged in with a master user in order to set the time.
