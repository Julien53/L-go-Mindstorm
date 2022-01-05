import cv2
import websockets
from time import sleep
from asyncio import get_event_loop
from threading import Thread
from base64 import b64encode as b64E
from TankAPI import Ev3Controller as Tank

keycode = 0
# tank = Tank()
webcam = cv2.VideoCapture(0)

tab = {
    # 0  : sleep,
    # 1  : tank.Move,
    # 2  : tank.TurnLeftOnHimself,
    # 3  : tank.TurnLeft,
    # 4  : tank.Move,
    # 5  : sleep,
    # 6  : tank.TurnLeft,
    # 7  : sleep,
    # 8  : tank.TurnRightOnHimself,
    # 9  : tank.TurnRight,
    # 10 : sleep,
    # 11 : sleep,
    # 12 : tank.TurnRight,
    # 13 : sleep,
    # 14 : sleep,
    # 15 : tank.StopAll,

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
    34 : 0,
}

async def CmdReceiver(websocket, path):
    global keycode
    global tab
    async for Mes in websocket:
        # tab[15]()
        try:
            if (Mes.startswith("[A]")):
                n = int(Mes.replace("[A]", ""))
                keycode += n
                # tab[keycode](tab[keycode + 20])

            elif (Mes.startswith("[D]")):
                n = int(Mes.replace("[D]", ""))
                keycode -= n
                # tab[15]()
                # tab[keycode](tab[keycode + 20])

        except Exception as e:
            ret = str(e)


async def ImgReceiver(websocket, path):
    global keycode
    global tab
    async for Mes in websocket:
        try:
            if (Mes == "StartImage"):
                while (True):
                    global webcam
                    check, frame = webcam.read()
                    obj = b64E(cv2.imencode('.jpg', frame)[1].tobytes())
                    await websocket.send(str(obj))
                    sleep(1/60)
        except Exception as e:
            ret = str(e)
    
ImgSocket = websockets.serve(ImgReceiver, "0.0.0.0", 443)
CmdSocket = websockets.serve(CmdReceiver, "0.0.0.0", 53)

get_event_loop().run_until_complete(ImgSocket)
get_event_loop().run_until_complete(CmdSocket)
get_event_loop().run_forever()