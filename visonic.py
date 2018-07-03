import json
import requests

from time import sleep

class connect(object):
   """ The class that is operating against the Visonic API """

   # Web Client configuration
   __app_type     = 'com.visonic.PowerMaxApp'
   __user_agent   = 'Visonic-GO/2.6.8 CFNetwork/808.1.4 Darwin/16.1.0'
   __hostname     = 'visonic.tycomonitor.com'
   __user_code    = '1234'
   __user_id      = '00000000-0000-0000-0000-000000000000'
   __panel_id     = '123456'
   __partition    = 'P1'

   # Connection settings
   __max_connection_attempts = 20

   # The Visonic API URLs used
   __login_url    = None
   __status_url   = None
   __arm_away_url = None
   __arm_home_url = None
   __disarm_url   = None

   # API session token
   __session_token = None

   def __init__(self, hostname, user_code, user_id, panel_id, partition):
      """ Class constructor """

      # Set connection specific details
      self.__hostname = hostname
      self.__user_code = user_code
      self.__user_id = user_id
      self.__panel_id = panel_id
      self.__partition = partition

      # Visonic API URLs that should be used
      self.__login_url    = 'https://' + self.__hostname + '/rest_api/3.0/login'
      self.__status_url   = 'https://' + self.__hostname + '/rest_api/3.0/status'
      self.__arm_away_url = 'https://' + self.__hostname + '/rest_api/3.0/arm_away'
      self.__arm_home_url = 'https://' + self.__hostname + '/rest_api/3.0/arm_home'
      self.__disarm_url   = 'https://' + self.__hostname + '/rest_api/3.0/disarm'

   def __get_session_token(self):
      """ Retrieve a session token to be used by the other API requests """

      # Setup authentication information
      login_info = {
         'user_code': self.__user_code,
         'app_type': self.__app_type,
         'user_id': self.__user_id,
         'panel_web_name': self.__panel_id
      }

      login_json = json.dumps(login_info, separators=(',', ':'))

      #print(login_json)

      # Header information used by the Visonic App
      api_headers = {
         'Host': self.__hostname,
         'Content-Type': 'application/json',
         'Accept': '*/*',
         'User-Agent': self.__user_agent,
         'Accept-Language': 'en-gb',
         'Content-Length': str(len(login_json))
      }

      # Connect to the API and try to get a session token
      response = requests.post(self.__login_url, headers=api_headers, data=login_json)

      # Check HTTP response code
      if self.__status_code_ok(response):
         data = json.loads(response.content.decode('utf-8'))
         session_token = data['session_token']
         return session_token
      else:
         return None

   def __get_status(self):
      """
      Get the current alarm status. This will get the information via the Visonic API and
      simultaneously connect to the Visonic Alarm System in order to get the fresh status.

      The object returned from the server looks something like this:
      {
         'is_connected': True,
         'exit_delay': 30,
         'partitions': [{
            'partition': 'ALL',
            'active': True,
            'state': 'Disarm',
            'ready_status': True
         }]
      }
      """

      # Prepare the header to be send
      status_headers = {
         'Host': self.__hostname,
         'Accept': '*/*',
         'User-Agent': self.__user_agent,
         'Accept-Language': 'en-gb',
         'Session-Token': self.__session_token
      }

      # Alarm status variables we want to populate
      is_connected = False
      is_active    = False
      armed_state  = 'unknown'
      partition    = 'unknown'
      ready_status = False
      exit_delay   = 0
      conn_retries = 0

      # Poll the API and wait for the is_connected variable to be True so the
      # Visonic Alarm System is connected to the central servers.
      while conn_retries < self.__max_connection_attempts and is_connected is False:
         response = requests.get(self.__status_url, headers=status_headers)
         conn_retries += 1

#         print(response.json())

         if self.__status_code_ok(response):
#            print('Response is OK (200)')
            data = json.loads(response.content.decode('utf-8'))
            is_connected = data['is_connected']
            exit_delay   = data['exit_delay']
            partitions   = data['partitions']

            if is_connected:
               print('Connected to your Visonic Alarm system! :)')

               # Current state of the alarm
               state = partitions[0]['state']
               if state == 'Disarm':
                  armed_state = 'disarmed'
               elif state == 'Home':
                  armed_state = 'armed_home'
               elif state == 'Away':
                  armed_state = 'armed_away'
               elif state == 'ExitDelayHome':
                  armed_state = 'arming_exit_delay_home'
               elif state == 'ExitDelayAway':
                  armed_state = 'arming_exit_delay_away'
               else:
                  armed_state = state

               # Is the alarm ready to be armed? If False there is probably door
               # or window sensors that are open
               ready_status = partitions[0]['ready_status']

               # The partition reported by the alarm system
               partition = partitions[0]['partition']

               # Is the alarm system active
               is_active = partitions[0]['active']

               # Dictionary with the alarm state
               alarm_status = { 'state': armed_state,
                                'ready_status': ready_status,
                                'partition': partition,
                                'is_connected': is_connected,
                                'is_active': is_active,
                                'exit_delay': exit_delay,
                                'session_token': self.__session_token }

               return alarm_status
            else:
               print('Not yet connected, retrying [{0}]...'.format(conn_retries))
               sleep(1)
         else:
            # Connection failed and we return an unknown state
            alarm_status = { 'state': armed_state,
                             'ready_status': ready_status,
                             'partition': partition,
                             'is_connected': is_connected,
                             'is_active': is_active,
                             'exit_delay': exit_delay,
                             'session_token': self.__session_token }

            return alarm_status

   def __status_code_ok(self, response):
      """ Check the status code of the HTTP response """

      if response.status_code >= 500:
         print('[{0}] Server Error'.format(response.status_code))
         return False
      elif response.status_code == 404:
         print('[{0}] URL not found: [{1}]'.format(response.status_code,api_url))
         return False
      elif response.status_code == 401:
         print('[{0}] Authentication Failed'.format(response.status_code))
         return False
      elif response.status_code == 400:
         print('[{0}] Bad Request: {1} ({2})'.format(response.status_code,
                                               response.json()['error_message'],
                                               response.json()['error_reason_code']))
         return False
      elif response.status_code >= 300:
         print('[{0}] Unexpected Redirect: {1} ({2})'.format(response.status_code,
                                                  response.json()['error_message'],
                                                  response.json()['error_reason_code']))
         return False
      elif response.status_code == 200:
         return True
      else:
         print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
         return False

   def login(self):
      """ Try to login and get a session token """

      self.__session_token = self.__get_session_token()
      if self.__session_token is None:
         return False
      else:
         return True

   def status(self):
      """ Get the status of the alarm """

      # If login is successful we can return the status
      if self.login():
         return self.__get_status()
      else:
         return None
