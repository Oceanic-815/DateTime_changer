"""
The script moves the system date forward and the time backward to provoke backup start by schedule and speed up testing.
For example, we have a backup plan which starts at 10:00:00 PM every day. To speed up testing, we need to move system
date one day forward and the time backward to 09:59:00 PM after each backup start. So, this script moves system date 1
day forward and the time backward. The time should be specified as a parameter.
Usage: DateTime_changer.exe -t:21:59:00
"""
#  TODO Disable auto sync the time
import datetime
import os
import sys
import getopt

time_str = None
os.system("")

try:
    opts, args = getopt.getopt(sys.argv[1:], "t:h")
    for name, value in opts:
        if name == "-t":
            time_str = value[1:]
            print("Success!")
        elif name == "-h":
            print('Usage:>> scriptname -t:"21:59:00"')
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
    print('Usage:>> scriptname -t:21:59:00')
