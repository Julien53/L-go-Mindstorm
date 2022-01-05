# This script will be on a mini computer (not the raspberry)
# which will be used as a router

# This script will be used as an interface to 
# receive commands from the raspberry pi via XBee

from time import sleep
from os import system as exec
from subprocess import check_output as outExec
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

device = XBeeDevice("/dev/ttyUSB0", 9600)
remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20041C3338D"))
device.open()
pid = 0

def start():
    exec("ssh root@10.2.0.164 \"/etc/init.d/carproxy start $(hostname -i)\"")
    exec("/etc/init.d/carproxy start 10.0.0.2")
    return (0 + (1, 0)[outExec("ssh root@10.2.0.164 \"/etc/init.d/carproxy status &> /dev/null; echo $?;\"", shell=True, executable="/bin/bash").decode('UTF-8').split('\n')[0] == 0] + (2, 0)[exec("/etc/init.d/carproxy status") == 0])
    
while True:
    if (exec("ps | grep " + str(pid) + " | grep openvpn") == 0):
        break
    else:
        pid = outExec("{ openvpn /root/vpn-dinf-linux.ovpn & pid=$!; disown; } &> /dev/null; echo $pid;", shell=True, executable="/bin/bash").decode('UTF-8').split('\n')[0]

while True:
    try:
        message = device.read_data(60).data.decode('UTF-8')
        if (message == "start"):
            device.send_data(remote, str(start()))
    except:
        sleep(5)

# Error code :
# 0 (000) = no error
# 1 (001) = server proxy error
# 2 (010) = router proxy error
# 3 (011) = server and router proxy error
# 4 (100) = http error
# 5 (101) = http and wifi error
# 6 (110) = http and dhcp error
# 7 (111) = http and dhcp and wifi error