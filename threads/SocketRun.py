import datetime
import os
import re
import threading
import time
import itchat
import websockets
import asyncio


class SockerRun(threading.Thread):
    # 插件启动状态
    status = True
    # 插件名
    theadName = "SockerRun"
    # 执行优先级（越小越快，最低0）
    priority = 100
    # 锁
    lock = False
    # 异步进程
    loop = None

    # websocket连接
    async def webSockets(self, websocket):
        async for message in websocket:
            if self.lock:
                return
            print("got a message:{}".format(message))
            await websocket.send(message)

    def run(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        self.loop = asyncio.get_event_loop()
        while True:
            if self.lock:
                break
            try:
                self.loop.run_until_complete(websockets.serve(self.webSockets, 'localhost', 9999))
                print("websocket服务器启动成功，端口：9999")
                break
            except:
                print("端口被占用，等待端口释放" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            time.sleep(5)
        self.loop.close()

    def __init__(self):
        threading.Thread.__init__(self, name=self.theadName, daemon=True)
        self.platform = None

    def stop(self):
        self.lock = True
        self.loop.stop()
        self.loop.close()
        self.isStop()

    def setPlatform(self, platform):
        self.platform = platform

    def isStart(self):
        self.platform.threadStart(self.theadName)

    def isStop(self):
        self.platform.threadStop(self.theadName)

    def notRun(self):
        self.platform.threadNotRun(self.theadName)

    def inRun(self):
        self.platform.threadRun(self.theadName)


def getPluginClass():
    return SockerRun
