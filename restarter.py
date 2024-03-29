from datetime import datetime
import logging
import os
import sys
# import subprocess

import psutil

# function to check if service is running 
def service_is_running(check_process, pid_to_skip):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
        except psutil.NoSuchProcess:
            pass
        else:
            if (check_process in str(pinfo['cmdline'])) \
                    and (str(pinfo['pid']) != str(pid_to_skip)):
                return True
    return False


# function to start service if it's not running
def start_if_not_running(to_check_process, full_command_process, pid_to_skip):
    if not service_is_running(to_check_process, pid_to_skip):
        print(datetime.now())
        print("WARNING: " + to_check_process + " is NOT running")
        # log_cmd = str(etl_fw_process).split('.')[0] + "_output.log"
        # run_cmd = full_command_process 
        # + " 2>&1 1>" + log_cmd + " &"
        print("WARNING: Auto-restarting " + to_check_process + " by command \"" + full_command_process + "\"")
        # subprocess.Popen(run_cmd, shell=True)
        os.system(full_command_process)
    # else:
    #     print("This process is up and running - no need to start it: <" + to_check_process + ">")


def main():
    # print("start")
    if len(sys.argv) > 2:
        short_cmd = str(sys.argv[1])
        full_command = str(sys.argv[2])
    else:
        print('Not enough parameters, use like this: restarter <short_command> "full command to start" ')
        sys.exit()
    # print("short_cmd="+short_cmd)
    # print("full_command="+full_command)
    # pyradio_cmd='pyradio'
    # pyradio_cmd_full='/home/raspberry/.local/bin/pyradio >/home/raspberry/pyradio/log.txt 2>&1 &'
    start_if_not_running(short_cmd, full_command, str(os.getpid()))


# this is the start point
if __name__ == '__main__':
    main()


