import os
import threading
import itchat
import importlib
from itchat.content import *
from tools import *


class Platform:
    def __init__(self):
        self.plugins = []
        self.threads = []
        self.loadPlugins()
        self.loadThreads()

    @staticmethod
    def pluginStart(from_):
        print("读取插件 %s." % from_)

    @staticmethod
    def pluginStop(from_):
        print("结束插件 %s." % from_)

    @staticmethod
    def pluginNotRun(from_):
        print("插件已禁用 %s." % from_)

    @staticmethod
    def pluginRun(from_):
        print("插件已启用 %s." % from_)

    @staticmethod
    def threadStart(from_):
        print("读取线程 %s." % from_)

    @staticmethod
    def threadStop(from_):
        print("线程停止 %s." % from_)

    @staticmethod
    def threadNotRun(from_):
        print("线程已禁用 %s." % from_)

    @staticmethod
    def threadRun(from_):
        print("线程已启用 %s." % from_)

    # 重新加载插件
    def reload(self):
        self.plugins = []
        self.loadPlugins()

    # 重新加载线程
    def reloadThreads(self):
        self.shutdownThreads()
        self.threads = []
        self.loadThreads()

    # 加载线程文件夹
    def loadThreads(self):
        for filename in os.listdir("threads"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            self.runThead(filename)
        self.threads.sort(key=lambda i: i.priority)

    # 加载插件文件夹
    def loadPlugins(self):
        for filename in os.listdir("plugins"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            self.runPlugin(filename)
        self.plugins.sort(key=lambda i: i.priority)

    # 读取线程数据
    def runThead(self, filename):
        threadName = os.path.splitext(filename)[0]
        _threads = __import__("threads." + threadName, fromlist=[threadName])
        importlib.reload(_threads)
        clazz = _threads.getPluginClass()
        o = clazz()
        o.setPlatform(self)
        o.isStart()
        # 进程启动状态
        if o.status:
            self.threads.append(o)
            o.start()
            o.inRun()
        else:
            o.notRun()
            o.setPlatform(None)

    # 读取插件数据
    def runPlugin(self, filename):
        pluginName = os.path.splitext(filename)[0]
        plugin = __import__("plugins." + pluginName, fromlist=[pluginName])
        importlib.reload(plugin)
        clazz = plugin.getPluginClass()
        o = clazz()
        o.setPlatform(self)
        o.start()
        # 插件启动状态
        if o.status:
            self.plugins.append(o)
            o.inRun()
        else:
            o.notRun()
            o.setPlatform(None)

    # 结束所有线程
    def shutdownThreads(self):
        for i in self.threads:
            i.stop()
            i.setPlatform(None)

    # 结束所有插件
    def shutdown(self):
        data = []
        for o in self.plugins:
            if o.pluginName == "TianDao":
                data.append(o)
                continue
            o.stop()
            o.setPlatform(None)
        self.plugins = data

    # 插件运行
    def botRunPlugin(self, msg, tag):
        for o in self.plugins:
            try:
                if o.asynch:
                    threading.Thread(target=o.run(msg, tag), name=o.pluginName).start()
                else:
                    o.run(msg, tag)
            except:
                print(o.pluginName + "线程错误")


if __name__ == "__main__":
    platform = Platform()


    @itchat.msg_register(itchat.content.PICTURE)
    def image_reply(msg):
        platform.botRunPlugin(msg, "PICTURE")


    @itchat.msg_register(itchat.content.PICTURE, isGroupChat=True)
    def image_reply(msg):
        platform.botRunPlugin(msg, "PICTUREGroup")


    @itchat.msg_register(itchat.content.TEXT)
    def text_reply(msg):
        platform.botRunPlugin(msg, "TEXT")


    @itchat.msg_register(TEXT, isGroupChat=True)
    def text_reply(msg):
        platform.botRunPlugin(msg, "TEXTGroup")


    # 开启微信机器人
    # startBot(False)
    startBot(2)
