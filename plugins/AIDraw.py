import asyncio
import threading
import time

import itchat
import os
import websockets
import json
import random
from tools.ImageTools import decode_image
from tools.ImageTools import encode_image


class AIDraw:
    # 插件启动状态
    status = True
    # 插件名
    pluginName = "AIDraw"
    # 执行优先级（越小越快，最低0）
    priority = 100
    # 异步线程
    asynch = False
    # 匹配头
    startSearch = ['画画 ', ['转动画', '图片转动画', '转动漫', '图片转动漫']]

    # 列表
    cartoonUser = []
    cartoonGroup = []

    def run(self, msg, tag):
        title = str(msg.text).lower().strip()
        if (tag in ["TEXT", "TEXTGroup"]) and (title.startswith(self.startSearch[0].lower())):
            value = str(msg.text)[2:].strip()
            print(self.pluginName + "-----" + str(value))
            fileName = AIDraw.getImage(value)
            itchat.send_image(fileDir=fileName, toUserName=str(msg.FromUserName).strip())
            os.remove(path=fileName)
            return
        if (tag in ["TEXT", "TEXTGroup"]) and (title in self.startSearch[1]):
            itchat.send("图片转动画风格开启，请发送一张图片", toUserName=str(msg.FromUserName).strip())
            if tag == "TEXT":
                self.cartoonUser.append(str(msg.FromUserName))
            if tag == "TEXTGroup":
                self.cartoonGroup.append(str(msg.ActualUserName))
            return
        if tag == "PICTUREGroup":
            if str(msg.ActualUserName) in self.cartoonGroup:
                self.cartoonGroup.remove(str(msg.ActualUserName))
                self.toCartoon(msg)
                return
        if tag == "PICTURE":
            if str(msg.FromUserName) in self.cartoonUser:
                self.cartoonUser.remove(str(msg.FromUserName))
                self.toCartoon(msg)
                return

    def toCartoon(self, msg):
        i = 0
        while i < 5:
            time.sleep(3)
            itchat.send(str(i), toUserName=str(msg.FromUserName).strip())
            i = i + 1

    def __init__(self):
        self.platform = None

    def setPlatform(self, platform):
        self.platform = platform

    def start(self):
        self.platform.pluginStart(self.pluginName)

    def stop(self):
        self.platform.pluginStop(self.pluginName)

    def notRun(self):
        self.platform.pluginNotRun(self.pluginName)

    def inRun(self):
        self.platform.pluginRun(self.pluginName)

    @staticmethod
    def getHash(i):
        return str("%032x" % random.getrandbits(128))[0:(0 + i)]

    @staticmethod
    def getImage(text):
        return decode_image(asyncio.run(AIDraw.socketAI(text)))

    @staticmethod
    async def socketAI(text):
        print("sorket")
        async with websockets.connect(
                "wss://idea-ccnl-taiyi-stable-diffusion-chinese.hf.space/queue/join") as websocket:
            data = await websocket.recv()
            newHash = AIDraw.getHash(11)
            if json.loads(data)['msg'] == "send_hash":
                print("send_hash")
                await websocket.send(json.dumps({"session_hash": newHash, "fn_index": 1}))
                while True:
                    data = await websocket.recv()
                    if json.loads(data)['msg'] == "send_data":
                        print("send_data")
                        await websocket.send(json.dumps({"fn_index": 1,
                                                         "data": [str(text), 7, 20, 512,
                                                                  512, None, 0.8], "session_hash": newHash}
                                                        ))

                        break
                while True:
                    data = await websocket.recv()
                    datas = json.loads(data)
                    if datas['msg'] == "process_starts":
                        print("等待处理")
                    if datas['msg'] == "process_completed":
                        print("process_completed")
                        return datas['output']['data'][0]


def getPluginClass():
    return AIDraw
