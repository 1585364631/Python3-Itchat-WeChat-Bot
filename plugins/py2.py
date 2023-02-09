class Plugin2:
    # 插件启动状态
    status = False
    # 插件名
    pluginName = "plugin2"
    # 执行优先级（越小越快，最低0）
    priority = 500

    async def run(self, msg, tag):
        print(msg)
        print("类型：" + tag)

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
    return Plugin2
