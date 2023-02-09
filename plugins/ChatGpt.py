import itchat
import requests


# 接口失效，弃用
class ChatGpt:
    # 插件启动状态
    status = False
    # 插件名
    pluginName = "ChatGpt"
    # 执行优先级（越小越快，最低0）
    priority = 100
    # 匹配头
    startSearch = 'ai '
    # 异步线程
    asynch = False
    # 步进锁
    lock = True

    def run(self, msg, tag):
        if (tag in ["TEXT", "TEXTGroup"]) and (str(msg.text).lower().strip().startswith(self.startSearch.lower())):
            value = str(msg.text)[2:].strip()
            print(value)
            text = self.getChatGpt(value)
            print(text)
            itchat.send(msg=text, toUserName=str(msg.FromUserName).strip())

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

    def getChatGpt(self, search):
        body = {
            "text": search
        }
        self.lock = not self.lock
        if self.lock:
            response = requests.post(
                "http://47.106.68.150:8888/", json=body)
        else:
            response = requests.post(
                "http://106.55.104.75:8888/", json=body)
        return response.text


def getPluginClass():
    return ChatGpt
