from array import array
from ast import Bytes
import serial as sr
import time
import CommandTank as cd
from time import sleep as sp

# DCBA
# 0000
# 0101 = Moteur A et C (5)

# A = 1 0001
# B = 2 0010
# C = 4 0100
# D = 8 1000

# 8 + 1 = 1001

class opcode:
    OUTPUT_POWER = 'A3 00'
    START_MOTOR = 'A6 00'
    OUTPUT_STEP_SPEED = 'AE 00'
    STOP_MOTOR = ''

opcode.OUTPUT_POWER

print("Connection au port COM3...")
conn = sr.Serial('COM3', timeout = 2)

print("Connected")

#conn_out.write(b'12000001800000AE000681320082840382B40001')
foward_moving = bytes.fromhex('1200 0001 8000 00 AE00 02 0132 0082 8403 82B4 0001')
backward_moving = bytes.fromhex('1200 0001 8000 00 AE00 01 32 0082 8403 82B4 0001')
command = bytes.fromhex('0C000001800000A4000114A60001')

#conn.write(foward_moving)
#conn.write(backward_moving)
conn.write(command)
conn.close()