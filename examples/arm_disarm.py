#!/usr/bin/env python3
from time import sleep
from visonic import alarm

hostname  = 'your.alarmcompany.com'
user_code = '1234'
user_id   = '2d978162-b00b-42a8-a5e5-b4a99100bd3a'
panel_id  = '123ABC'

alarm = alarm.Setup(hostname, user_code, user_id, panel_id)

def arm():
    ''' Arm in home mode and print progress to command line output. '''

    alarm.arm_home()

    print('Arming in home mode, please wait.', end='', flush=True)

    while True:
        arm_state = alarm.get_status().partitions[0].state
        if arm_state != 'Home':
            print('.', end='', flush=True)
        else:
            print('ARMED!', flush=True)
            break
        sleep(2)

def disarm():
    ''' Disarm the alarm and print progress to command line output. '''

    alarm.disarm()

    print('Disarming.', end='', flush=True)

    while True:
        arm_state = alarm.get_status().partitions[0].state
        if arm_state != 'Disarm':
            print('.', end='', flush=True)
        else:
            print('done!', flush=True)
            break
        sleep(1)

def main():
    ''' Simple menu system allowing for controlling the alarm system. '''

    alarm.login()
    print(f"Successfully logged in to '{hostname}'.")
    print()

    while True:
        print('Alarm actions:')
        print('1. Arm in home mode')
        print('2. Disarm the alarm system')
        print('3. Print current state')
        print('4. Exit')
        action = input('# ')

        if action == '1':
            arm()
        elif action == '2':
            disarm()
        elif action == '3':
            arm_state = alarm.get_status().partitions[0].state
            print(f"Current state is '{arm_state}'.")
        elif action == '4':
            print('Bye bye...')
            break
        else:
            print('Not an option, try again...')

        print()

if __name__ == '__main__':
    # Execute if run as a script
    main()
