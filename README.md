# Visonic Alarm Library

## Introduction
A simple library for the Visonic PowerMaster API written in Python 3.

It is built using same technique used in the Visonic-GO app. So if you can use the app to connect to your alarm system, the chances are you can use this library as well. I have developed and tested it with a Visonic PowerMaster-10 using a PowerLink 3 IP module.

> The library currently only support verion 4.0 of the API running on the server side. As of now that is the only version my alarm company is supporting and thus I have no other version to develop against. It seems that some alarm companies has been rolling out version 8.0 of the API (requiring username and password authentication), which will be supported in the future.

## Installation
Install the latest version with pip3:
```
$ pip3 install visonicalarm
```

## Code examples
### Setup
Use the same settings you are using to login to the Visonic-GO app.
```python
from visonic import alarm

hostname  = 'your.alarmcompany.com'
user_code = '1234'
user_id   = '2d978962-daa6-4e18-a5e5-b4a99100bd3b'
panel_id  = '123ABC'

alarm = alarm.Setup(hostname, user_code, user_id, panel_id)
```
The `user_id` is a GUID (Globally Unique IDentifier) that should be unique to each app communicating with the API server. You can get a GUID from [https://www.guidgen.com](https://www.guidgen.com) and paste into your code.

>All of the following code is assuming you have completed this Setup step prior to calling any of the methods.

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

### Set the time
You can update the time of the alarm system by calling the `set_time()` method. It accepts a datetime object that will be used to set the time.
```python
try:
    alarm.set_time(datetime.now())
except PermissionDeniedError:
    print('Permission denied. Please login using a master user and try again.')
```
> Note: You must be logged in with a master user in order to set the time.
