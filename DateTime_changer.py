"""
The script moves the system date forward and the time backward to provoke backup start by schedule and speed up testing.
For example, we have a backup plan which starts at 10:00:00 PM every day. To speed up testing, we need to move system
date one day forward and the time backward to 09:59:00 PM after each backup start. So, this script moves system date 1
day forward and the time backward. The time should be specified as a parameter.
Usage: DateTime_changer.exe -t:21:59:00

Additionally, option -p changes system settings such as UAC, power management (to avoid sleep mode) and disables
time auto synchronization.
"""

import datetime
import os
import sys
import getopt
import winreg

time_str = None


def prepare():
    os.system("w32tm /unregister")
    os.system("powercfg -X -monitor-timeout-ac 0")
    os.system("powercfg -X monitor-timeout-dc 0")
    print("-Monitor power settings were changed")
    os.system("powercfg -X standby-timeout-ac 0")
    os.system("powercfg -X standby-timeout-dc 0")
    print("--Standby settings were changed")
    os.system("powercfg -X hibernate-timeout-ac 0")
    os.system("powercfg -X hibernate-timeout-dc 0")
    print("---Hibernate settings were changed")
    try:  # Disable UAC via Registry
        opened_key_for_edit = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                             "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 0,
                                             winreg.KEY_SET_VALUE)
        winreg.SetValueEx(opened_key_for_edit, "EnableLUA", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(opened_key_for_edit, "ConsentPromptBehaviorAdmin", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(opened_key_for_edit, "PromptOnSecureDesktop", 0, winreg.REG_DWORD, 0)
        print("----UAC disabled. Reboot is required")
        winreg.CloseKey(opened_key_for_edit)
    except Exception:
        raise


try:
    opts, args = getopt.getopt(sys.argv[1:], "t:hp")
    for name, value in opts:
        if name == "-t":
            time_str = value[1:]
            print("Success!")
        elif name == "-p":
            prepare()
        elif name == "-h":
            print(
                'Usage:\n> scriptname -t:21:59:00\nAlso, there is an option -p that changes Power management settings,'
                'disables Time autosync and UAC.\n When UAC becomes disabled, a system reboot is usually required.')

except getopt.GetoptError:
    print("Option not recognized")
    print('Usage:>> scriptname -t:21:59:00')

date_str = datetime.datetime.now()

date_str += datetime.timedelta(days=1)
a = date_str.strftime('%m-%d-%y')
cmd_d = 'date ' + a
try:
    cmd_t = 'time ' + time_str
    c_d = os.system(cmd_d)
    c_t = os.system(cmd_t)
except TypeError:
    print('-h for help')
