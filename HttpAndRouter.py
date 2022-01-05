# This file must be executable as root from everyone
# ALL ALL = NOPASSWD: /path/to/my/program

#pip install digi-xbee

from os import system as exec
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

code = (4, 0)[exec("service apache2 start") == 0]

device = XBeeDevice("/dev/ttyUSB0", 9600)
remote = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20041C332AA"))
device.open()

device.send_data(remote, "start")

try:
    code += int(device.read_data(60).data)
except:
    code += 3

exit(code)


# Error code :
# 0 (000) = no error
# 1 (001) = server proxy error
# 2 (010) = router proxy error
# 3 (011) = server and router proxy error
# 4 (100) = http error
# 5 (101) = http and wifi error
# 6 (110) = http and dhcp error
# 7 (111) = http and dhcp and wifi error