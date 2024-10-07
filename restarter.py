from datetime import datetime
import os
import sys
import time
# import subprocess

import psutil

# function to check if service is running 
def service_is_running(check_process, command_to_skip):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
        except psutil.NoSuchProcess:
            pass
        else:
            if (check_process in str(pinfo['cmdline'])) \
                    and (command_to_skip not in str(pinfo['cmdline'])):
                time.sleep(1)
                return True
    return False


# function to start service if it's not running
def start_if_not_running(to_check_process, full_command_process, command_to_skip):
    if not service_is_running(to_check_process, command_to_skip):
        time.sleep(1)
        print(datetime.now())
        print("WARNING: Auto-restarting " + to_check_process + " by command \"" + full_command_process + "\"")
        os.system(full_command_process)
    # else:
    #     print("This process is up and running - no need to start it: <" + to_check_process + ">")


def main():
    if len(sys.argv) > 2:
        short_cmd = str(sys.argv[1])
        full_command = str(sys.argv[2])
    else:
        print('Not enough parameters, use like this: restarter <short_command> "full command to start" ')
        sys.exit()
    start_if_not_running(short_cmd, full_command, 'restarter/restarter.py')


# this is the start point
if __name__ == '__main__':
    main()


