import itchat
import requests
from requests.adapters import HTTPAdapter


class Courier:
    # 插件启动状态
    status = False
    # 插件名
    pluginName = "Courier"
    # 执行优先级（越小越快，最低0）
    priority = 100
    # 匹配头
    startSearch = ['快递查询 ']
    # 异步线程
    asynch = False
    # 请求
    request = None

    def run(self, msg, tag):
        if (tag in ["TEXT", "TEXTGroup"]) and (str(msg.text).lower().strip().startswith(self.startSearch[0].lower())):
            value = str(msg.text)[5:].strip()
            self.getCourier(value)
            # itchat.send(msg=str(self.getDog()), toUserName=str(msg.FromUserName).strip())
            return

    def __init__(self):
        self.platform = None

    def getCourier(self, number):
        pass

    def setPlatform(self, platform):
        self.request = requests.session()
        self.request.mount('https://', HTTPAdapter(max_retries=2))
        self.request.mount('http://', HTTPAdapter(max_retries=2))
        self.platform = platform

    def start(self):
        self.platform.pluginStart(self.pluginName)

    def stop(self):
        self.platform.pluginStop(self.pluginName)

    def notRun(self):
        self.platform.pluginNotRun(self.pluginName)

    def inRun(self):
        self.platform.pluginRun(self.pluginName)


def getPluginClass():
    return Courier
