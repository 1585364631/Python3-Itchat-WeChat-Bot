import datetime
import json

import itchat
import requests
from requests.adapters import HTTPAdapter


class Letter:
    # 插件启动状态
    status = True
    # 插件名
    pluginName = "Letter"
    # 执行优先级（越小越快，最低0）
    priority = 100
    # 匹配头
    startSearch = ['舔狗日记', '毒鸡汤', '历史上的今天', '每日一分钟']
    # 异步线程
    asynch = False
    # 请求
    request = None

    def run(self, msg, tag):
        if (tag in ["TEXT", "TEXTGroup"]) and (str(msg.text).lower().strip().startswith(self.startSearch[0].lower())):
            itchat.send(msg=str(self.getDog()), toUserName=str(msg.FromUserName).strip())
            return
        if (tag in ["TEXT", "TEXTGroup"]) and (str(msg.text).lower().strip().startswith(self.startSearch[1].lower())):
            itchat.send(msg=str(self.getChicken()), toUserName=str(msg.FromUserName).strip())
            return
        if (tag in ["TEXT", "TEXTGroup"]) and (str(msg.text).lower().strip().startswith(self.startSearch[2].lower())):
            itchat.send(msg=str(self.getHistoryDay()), toUserName=str(msg.FromUserName).strip())
            return
        if (tag in ["TEXT", "TEXTGroup"]) and (str(msg.text).lower().strip().startswith(self.startSearch[3].lower())):
            itchat.send(msg=str(self.getDayMin()), toUserName=str(msg.FromUserName).strip())
            return

    def getDog(self):
        url = "https://du.liuzhijin.cn/dog.php"
        print(url)
        try:
            response = \
                self.request.get(url=url, timeout=30).text.split(r'style="font-size: 1rem;">')[1].split(r'</span>')[
                    0].strip()
            return response
        except Exception as e:
            print("getDog报错：" + str(e))
            return "getDog报错：" + str(e)

    def getHistoryDay(self):
        day = datetime.datetime.now().strftime("%m%d")
        url = f'https://www.y5000.com/lssdjt/{day}/'
        print(url)
        try:
            response = self.request.get(url=url, timeout=30).text
            date = response.split(r'class="subHead">')[1].split(r'</p>')[0].strip()
            text = response.split(r'class="subP">')[1].split(r'</p>')[0].strip()
            return f'{date}\n{text}'
        except Exception as e:
            print("getHistoryDay报错：" + str(e))
            return "getHistoryDay报错：" + str(e)

    def getDayMin(self):
        url = f'https://api.vvhan.com/api/60s?type=json'
        print(url)
        try:
            data = json.loads(self.request.get(url=url, timeout=30).text)
            date = " ".join(data['time'])
            text = "\n\n".join(data['data'])
            return f"{date}\n{text}"
        except Exception as e:
            print("getDayMin报错：" + str(e))
            return "getDayMin报错：" + str(e)

    def getChicken(self):
        url = "https://du.liuzhijin.cn/"
        print(url)
        try:
            response = \
                self.request.get(url=url, timeout=30).text.split(r'style="font-size: 2rem;">')[1].split(r'</span>')[
                    0].strip()
            return response
        except Exception as e:
            print("getChicken报错：" + str(e))
            return "getChicken报错：" + str(e)

    def __init__(self):
        self.platform = None

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
    return Letter
