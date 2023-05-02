#!/usr/bin/env python3
from getpass import getpass
import inspect
from time import sleep
from visonic import alarm
from visonic.exceptions import *

hostname = "your.alarmcompany.com"
user_code = None
app_id = "00000000-0000-0000-0000-000000000000"
panel_id = "123ABC"
user_email = "user@example.com"
user_password = "An.Extremely.Long.Random.and.Secure.Password!"

alarm = alarm.Setup(hostname, app_id)


def arm():
    """Arm in home mode and print progress to command line output."""

    # Call connect() to ensure we are connected to the alarm panel prior to arming
    if connect():
        # Is the alarm system ready to be armed?
        if alarm.get_status().partitions[0].ready:
            alarm.arm_home()
        else:
            print("NOT READY: Unable to arm, check that doors and windows are closed.")
            print()
            input("Press <Enter> to continue...")
            return
    else:
        print("ERROR: Unable to connect to API server or alarm panel.")
        return

    print("Arming in Home mode, please wait..", end="", flush=True)

    while True:
        arm_state = alarm.get_status().partitions[0].state
        if arm_state != "HOME":
            print(".", end="", flush=True)
        else:
            print("ARMED!", flush=True)
            break
        sleep(2)
    print()
    input("Press <Enter> to continue...")


def disarm():
    """Disarm the alarm and print progress to command line output."""

    # Call connect() to ensure we are connected to the alarm panel prior to disarming
    if connect():
        alarm.disarm()
    else:
        print("ERROR: Unable to connect to API server or alarm panel.")
        return

    print("Disarming..", end="", flush=True)

    while True:
        arm_state = alarm.get_status().partitions[0].state
        if arm_state != "DISARM":
            print(".", end="", flush=True)
        else:
            print("done!", flush=True)
            break
        sleep(1)
    print()
    input("Press <Enter> to continue...")


def print_status():
    """Print the current status of the alarm system."""
    status = alarm.get_status()
    print(f"===========================")
    print(f"=== Alarm System Status ===")
    print(f"===========================")
    print(
        f' API Server   : Connection {"established" if status.connected else "pending"}'
    )
    print(
        f' Ethernet     : {"Connected" if status.bba_connected else "Not connected"} (hardware module {status.bba_state})'
    )
    print(
        f' GPRS         : {"Connected" if status.gprs_connected else "Not connected"} (hardware module {status.gprs_state})'
    )
    print()
    print(f" Discovery")
    print(f"  - Completed : {status.discovery_completed}")
    print(f"  - Stages    : {status.discovery_stages}")
    print(f"  - In queue  : {status.discovery_in_queue}")
    print(f"  - Triggered : {status.discovery_triggered}")
    print()
    print(f" Partitions")
    for partition in status.partitions:
        print(
            f'  - ID: {partition.id}    : {partition.state} ({"Ready" if partition.ready else "Not ready"})'
        )
    print()
    print(f" RSSI")
    print(f"  - Level     : {status.rssi_level.capitalize()}")
    print(f"  - Network   : {status.rssi_network}")

    print()
    input("Press <Enter> to continue...")


def print_class_list(class_list):
    if class_list:
        if not isinstance(class_list, list):
            class_list = [class_list]

        for item in class_list:
            print(item._data)
            print(f"{''.ljust(60,'-')}")
            print(f"Class : {type(item)}")
            print(f"{''.ljust(60,'-')}")
            attributes = inspect.getmembers(item, lambda a: not (inspect.isroutine(a)))
            for a in attributes:
                if not (
                    a[0].startswith("__")
                    and a[0].endswith("__")
                    or a[0].startswith("_")
                ):
                    if (
                        type(getattr(item, str(a[0]))) == list
                        and getattr(item, str(a[0]))
                        and type(getattr(item, str(a[0]))[0]) not in [int, str]
                    ):
                        print(str(a[0]).title())
                        for i, entry in enumerate(getattr(item, str(a[0]))):
                            label = f"    [{i}]"
                            print(
                                f"{label.ljust(35,' ')} : {getattr(item, str(a[0]))[i]}"
                            )
                    else:
                        print(
                            f"{str(a[0]).replace('_',' ',-1).title().ljust(35,' ')} : {getattr(item, str(a[0]))}"
                        )
    else:
        print(f"{''.ljust(20,'-')}")
        print(f"No Data")
        print(f"{''.ljust(20,'-')}")

    print()
    input("Press <Enter> to continue...")


def connect():
    """Ensure that we are authenticated and that the alarm panel is connected."""
    connected = False
    while not connected:
        try:
            alarm.panel_login(panel_id, user_code)
            if not alarm.connected():
                print("Connecting to alarm panel.", end="", flush=True)
                while True:
                    if not alarm.connected():
                        print(".", end="", flush=True)
                    else:
                        print("done!", flush=True)
                        connected = True
                        break
                    sleep(1)
            else:
                connected = True
        except UserAuthRequiredError:
            print(f"Authenticating using '{user_email}'...")
            try:
                alarm.authenticate(user_email, user_password)
                print("Successfully authenticated.")
            except WrongUsernameOrPasswordError as e:
                print("ERROR: " + e.message)
                return False
        except UserCodeIncorrectError as e:
            print("ERROR: " + e.message)
            return False
        except UserCodeRequiredError as e:
            print("ERROR: " + e.message)
            return False
        except LoginTemporaryBlockedError as e:
            print("ERROR: " + e.message)
            return False

    return True


def main():
    """Simple menu system allowing for controlling the alarm system."""

    print(f"Connecting to '{hostname}'...")
    print(f'Supported REST API version(s): {", ".join(alarm.get_rest_versions())}')

    global user_code
    user_code = getpass("Enter your master code: ")

    if not connect():
        return

    print(f"Connected to '{hostname}'.")
    print()

    while True:
        # Get the current arm status
        arm_state = (
            "Disarmed"
            if alarm.get_status().partitions[0].state == "DISARM"
            else "Armed"
        )

        print(f"===========================")
        print(f"=== Alarm Control Panel ===")
        print(f"===========================")
        print()
        print(f"  Current State: {arm_state}")
        print()
        print("  [1] Arm Home")
        print("  [2] Disarm")
        print("  [3] Show Status")
        print("  [4] List Devices")
        print("  [5] Show Events")
        print("  [6] Show Feature Set")
        print("  [7] Show Locations")
        print("  [8] Show Troubles")
        print("  [9] Show Users")
        print("  [I] Panels Info")
        print("  [P] Panels")
        print("  [S] Status")
        print("  [0] Exit")
        print()
        action = input("  Enter Number: ")
        print()

        if action == "1":
            arm()
        elif action == "2":
            disarm()
        elif action == "3":
            print_status()
        elif action == "4":
            print_class_list(alarm.get_devices())
        elif action == "5":
            print_class_list(alarm.get_events())
        elif action == "6":
            print_class_list(alarm.get_feature_set())
        elif action == "7":
            print_class_list(alarm.get_locations())
        elif action == "8":
            print_class_list(alarm.get_troubles())
        elif action == "9":
            print_class_list(alarm.get_users())
        elif action.lower() == "i":
            print_class_list(alarm.get_panel_info())
        elif action.lower() == "p":
            print_class_list(alarm.get_panels())
        elif action.lower() == "s":
            print_class_list(alarm.get_status())
        elif action == "0":
            print("Connection to the API server was terminated...")
            break
        else:
            print("Invalid option, please enter a number.")
            print()
            input("Press <Enter> to continue...")

        print()


if __name__ == "__main__":
    # Execute if run as a script
    main()
