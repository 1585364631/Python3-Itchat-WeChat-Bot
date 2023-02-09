import time

import itchat


class TianDao:
    # 插件启动状态
    status = True
    # 插件名
    pluginName = "TianDao"
    # 执行优先级（越小越快，最低0）
    priority = 1
    # 异步线程
    asynch = False
    # 匹配头
    startSearch = '天道 '

    def run(self, msg, tag):
        if (tag in ["TEXT", "TEXTGroup"]) and (str(msg.text).lower().strip().startswith(self.startSearch.lower())):
            value = str(msg.text)[3:].strip()
            if value == "重构":
                itchat.send("正在重构插件", toUserName=str(msg.FromUserName).strip())
                self.platform.reload()
                itchat.send("插件重构完成", toUserName=str(msg.FromUserName).strip())
                time.sleep(1)
                itchat.send("正在重构线程", toUserName=str(msg.FromUserName).strip())
                self.platform.reloadThreads()
                itchat.send("线程重构完成", toUserName=str(msg.FromUserName).strip())
                return
            if value == "摧毁":
                itchat.send("正在摧毁插件", toUserName=str(msg.FromUserName).strip())
                self.platform.shutdown()
                itchat.send("插件摧毁完成", toUserName=str(msg.FromUserName).strip())
                time.sleep(1)
                itchat.send("正在摧毁线程", toUserName=str(msg.FromUserName).strip())
                self.platform.shutdownThreads()
                itchat.send("线程摧毁完成", toUserName=str(msg.FromUserName).strip())
                return
            if value == "升级插件":
                itchat.send("正在升级插件", toUserName=str(msg.FromUserName).strip())
                self.platform.reload()
                itchat.send("插件升级完成", toUserName=str(msg.FromUserName).strip())
                return
            if value == "升级线程":
                itchat.send("正在升级线程", toUserName=str(msg.FromUserName).strip())
                self.platform.reloadThreads()
                itchat.send("线程升级完成", toUserName=str(msg.FromUserName).strip())
                return

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


def getPluginClass():
    return TianDao
