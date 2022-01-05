import asyncio
import cv2
import websockets
import socket
from os import system
from time import sleep
from asyncio import run
from base64 import b64encode as b64E
from asyncio import Future as runForever
from TankAPI import Ev3Controller as Tank

from threading import Thread

# Var
keycode = 0
tank = Tank()
webcam = cv2.VideoCapture(0)
controller = "controller"
client = ""
power = 0

commandList = []

actions = {
    0: sleep,
    1: tank.Move,
    2: tank.TurnLeftOnHimself,
    3: tank.TurnLeft,
    4: tank.Move,
    5: sleep,
    6: tank.TurnLeft,
    7: sleep,
    8: tank.TurnRightOnHimself,
    9: tank.TurnRight,
    10: sleep,
    11: sleep,
    12: tank.TurnRight,
    13: sleep,
    14: sleep,
    15: tank.StopAll,

    20  : 0,
    21  : 100,
    22  : 100,
    23  : 100,
    24  : -100,
    25  : 0,
    26  : -100,
    27  : 0,
    28  : 100,
    29  : 100,
    30 : 0,
    31 : 0,
    32 : -100,
    33 : 0,
    34 : 0
}

# async def main():
#     f1 = asyncio.create_task(FrontSocket("0.0.0.0", 443))
#     f2 = asyncio.create_task(BackSocket())
#     await asyncio.wait([f1,f2])

async def FrontSocket(ip, port):
    print("Receiver started")
    async with websockets.serve(Receiver, ip, port):
        await runForever()

def BackSocket():
    print("Startsocket started")
    HOST = '127.0.0.1'
    PORT = 8082

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        global commandList
        global controller
        global power
        
        sock.bind((HOST,PORT))
        sock.listen()
        print("Socket listen")

        while(True):
            conn = sock.accept()

            with conn:
                try:
                    #Send user info to socket
                    userData = str.encode("[info]" + controller + "|" + client + "|" + str(power))
                    conn.send(userData)

                    #send all commands
                    if commandList:
                        for command in commandList:
                            mes = str.encode("[comm]" + str(command))
                            conn.send(mes)
                            conn.recv(1024).decode('UTF-8')

                        commandList = []
                except Exception as e:
                    print(str(e))
                finally:
                    conn.send(str.encode("[end]"))
                    conn.close()

def UpdateBattery():
    global power
    while(True):
        sleep(5)
        power = tank.GetBattery()
        print(str(power))


async def Receiver(websocket, path):
    print("Receiver started")
    global keycode
    async for Mes in websocket:
        try:
            if (Mes != "i"): print(Mes)
            if (Mes == "i"):
                check, frame = webcam.read()
                obj = b64E(cv2.imencode('.jpg', frame)[1].tobytes())
                await websocket.send(str(obj))

            elif (Mes.startswith("[A]")):
                n = int(Mes.replace("[A]", ""))
                keycode += n
                actions[15]()
                actions[keycode](actions[keycode + 20])
                commandList.append(keycode)

            elif (Mes.startswith("[D]")):
                n = int(Mes.replace("[D]", ""))
                actions[15]()
                if (n != 15):
                    keycode -= n
                    actions[keycode](actions[keycode + 20])
                else:
                    keycode = 0
                    
            elif (Mes.startswith("[L]")):
                run(tank.Stream())

            elif (Mes.startswith("[S]")):
                run(tank.Sound(Mes.replace("[S]", "")))

            elif (Mes.startswith("[V]")):
                v = Mes.replace("[V]", "").split("|")
                run(tank.Speak(v[1], v[0]))
                
            elif(Mes.startwith("[C]")):
                controller = Mes.replace("[C]", "").split("|")

        except Exception as e:
            ret = str(e)

system("chmod +x ./sound/ffmpeg ./sound/raw2rsf")
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()

# run(StartSocket())
# Thread(target=UpdateBattery).start()
# Thread(target=BackSocket).start()

run(FrontSocket("0.0.0.0", 443))
