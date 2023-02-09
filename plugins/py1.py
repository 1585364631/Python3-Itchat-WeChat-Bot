class Plugin1:
    # 插件启动状态
    status = False
    # 插件名
    pluginName = "plugin1"
    # 执行优先级（越小越快，最低0）
    priority = 1000

    async def run(self, msg, tag):
        print("类型：" + tag)
        print(msg)

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
    return Plugin1
