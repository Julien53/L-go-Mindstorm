import websockets
from time import sleep
from threading import Thread
from asyncio import Future as runForever
from TankAPI import Ev3Controller as Tank

# 0001 =  1 =    0 deg = w
# 0010 =  2 =   90 deg = a
# 0011 =  3 =   45 deg = w + a

# 0100 =  4 =  180 deg = s
# 0110 =  6 =  135 deg = s + a
# 1100 = 12 = -135 deg = s + d

# 1000 =  8 =  -90 deg = d
# 1001 =  9 =  -45 deg = w + d

class CmdThread (Thread):

    def __init__(self, threadID, socketIP, port):
        Thread.__init__(self)
        self.threadID = threadID
        self.ip = socketIP
        self.port = port
        self.tank = Tank()
        self.keycode = 0

        self.tab = {
            0  : sleep(0),
            1  : self.tank.Move(100),
            2  : self.tank.TurnLeftOnHimself(100),
            3  : self.tank.TurnLeft(100),
            4  : self.tank.Move(-100),
            5  : sleep(0),
            6  : self.tank.TurnLeft(-100),
            7  : sleep(0),
            8  : self.tank.TurnRightOnHimself(100),
            9  : self.tank.TurnRight(-100),
            10 : sleep(0),
            11 : sleep(0),
            12 : self.tank.TurnRight(-100),
            13 : sleep(0),
            14 : sleep(0),
            15 : self.tank.StopAll()
        }

    async def run(self):
        async with websockets.serve(self.inMessage, self.ip, self.port):
            await runForever()  # run forever

    async def inMessage(self, websocket):
        for Mes in websocket:
            try:
                if (Mes.startswith("[A]")):
                    n = int(Mes.replace("[A]", ""))
                    self.keycode += n
                    self.start()

                elif (Mes.endswith("[D]")):
                    n = int(Mes.replace("[D]", ""))
                    self.keycode -= n
                    self.stop()

            except Exception as e:
                print(str(e))

            # await websocket.send(ret)

    def start(self):
        self.tab[self.keycode]

    def stop(self):
        self.tab[15]
        self.start()