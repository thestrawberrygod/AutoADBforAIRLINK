import psutil
import pkg_resources
import socket
import pyfiglet
from pyfiglet import Figlet
import sys,colorama
import simple_chalk as chalk
import subprocess
import logging
logger = logging.getLogger('my-logger')
logger.propagate = False
colorama.init()
def start():
    rows = []
    lc = psutil.net_connections('inet')
    for c in lc:
        if "OVR" in lc:
            print(lc)
        (ip, port) = c.laddr
        if ip == '0.0.0.0' or ip == '::':
            if c.type == socket.SOCK_STREAM and c.status == psutil.CONN_LISTEN:
                proto_s = 'tcp'
            elif c.type == socket.SOCK_DGRAM:
                proto_s = 'udp'
            else:
                continue
            pid_s = str(c.pid) if c.pid else '(unknown)'
            command = f'tasklist /fi "pid eq {pid_s}"'
            pi=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            if "OVR" in str(pi.stdout.read()):
                print('Oculus port Found',port )
                localip = socket.gethostbyname(socket.gethostname())
                print("Ip found",localip)
                return(localip,port)
    input("Unable to find OCULUS port, make sure the air link option is on.(Press enter to quit)")


if __name__ == "__main__":
    f = Figlet()
    print(chalk.redBright(f.renderText('UwU')))
    print("-------------------------------------------")
    localip,port = start()
    print("-------------------------------------------")
    input('All the parameters were found, make sure your headset is plugged in, press enter afterwards')
    command = f'adb shell am start -a android.intent.action.VIEW -d "xrstreamingclient://{localip}:{port}" com.oculus.xrstreamingclient'
    pi=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    if "Starting: Intent" in str(pi.stdout.read()):
        print("Succesfully sent the commands to the headset, please disconnect it now.")
        input("END")
    elif "Starting: Intent" not in str(pi.stdout.read()):
        print("Something went wrong")
        input("END")
