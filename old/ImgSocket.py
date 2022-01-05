import cv2
import websockets
from time import sleep
from threading import Thread
from base64 import b64encode as b64E
from asyncio import Future as runForever

async def start(ip, port):

    async with websockets.serve(main, ip, port):
        await runForever()

async def main(self, websocket):
    while (True):
        check, frame = self.webcam.read()
        obj = b64E(cv2.imencode('.jpg', frame)[1].tobytes())
        await websocket.send(str(obj))
        sleep(1/60)