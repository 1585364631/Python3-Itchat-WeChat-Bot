import json
import os
import itchat
import requests
from requests.adapters import HTTPAdapter
from tools.DownLoad import DownLoadImage


class HonorOfKings:
    # 插件启动状态
    status = True
    # 插件名
    pluginName = "HonorOfKings"
    # 执行优先级（越小越快，最低0）
    priority = 100
    # 匹配头
    startSearch = '王者荣耀 '
    # 异步线程
    asynch = False
    # 请求
    request = None
    # 装备类型
    equipType = {
        '1': "攻击装备",
        '2': "法术装备",
        '3': "防御装备",
        '4': "移动装备",
        '5': "打野装备",
        '7': "游走装备"
    }

    def run(self, msg, tag):
        if (tag in ["TEXT", "TEXTGroup"]) and (str(msg.text).lower().strip().startswith(self.startSearch.lower())):
            value = str(msg.text)[5:].strip()
            if value == "装备列表":
                itchat.send(msg=str(self.getEquipList()), toUserName=str(msg.FromUserName).strip())
                return
            if value == "装备类型":
                itchat.send(msg=str(self.getEquipType()), toUserName=str(msg.FromUserName).strip())
                return
            if "周免" in value:
                itchat.send(msg=str(self.getWeeksFrom()), toUserName=str(msg.FromUserName).strip())
                return
            if value.strip().startswith("装备"):
                value = value[2:].strip()
                self.getEquipShow(value, str(msg.FromUserName).strip())
                return
            if value.strip().startswith("英雄"):
                value = value[2:].strip()
                self.getHeroShow(value, str(msg.FromUserName).strip())
                return
            for name, val in self.equipType.items():
                if value == val:
                    itchat.send(msg=str(self.getEquipList(name)), toUserName=str(msg.FromUserName).strip())
                    return

    def getEquip(self):
        url = "http://api.000081.xyz/wzry/zb"
        print(url)
        try:
            response = json.loads(self.request.get(url=url, timeout=30).text)
            return response
        except Exception as e:
            print("getEquip报错：" + str(e))
            return "getEquip报错：" + str(e)

    def getHero(self):
        url = "http://api.000081.xyz/wzry/yx"
        print(url)
        try:
            response = json.loads(self.request.get(url=url, timeout=30).text)
            return response
        except Exception as e:
            print("getHero报错：" + str(e))
            return "getHero报错：" + str(e)

    def getWeeksFrom(self):
        response = self.getHero()
        heroList = [f"{i['title']}--{i['cname']}" for i in response if 'pay_type' in i.keys()]
        return "\n".join(heroList)

    def getHeroShow(self, name, user):
        response = self.getHero()
        data = [i for i in response if i['cname'].strip() == name]
        if len(data) == 0:
            itchat.send(msg="无结果", toUserName=user)
            return
        # img = DownLoadImage(data[0]['img'])
        img1 = DownLoadImage(f"http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{data[0]['ename']}/{data[0]['ename']}-bigskin-1.jpg")
        data = json.dumps(data[0], sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        # if img['code'] == 200:
        #     itchat.send_image(fileDir=img['filename'], toUserName=user)
        if img1['code'] == 200:
            itchat.send_image(fileDir=img1['filename'], toUserName=user)
        # os.remove(img['filename'])
        os.remove(img1['filename'])
        itchat.send(msg=data, toUserName=user)

    def getEquipShow(self, name, user):
        response = self.getEquip()
        for i in response:
            equipList = "装备详细信息\n--------"
            if name in i['item_name']:
                itchat.send(msg=str(json.dumps(response)), toUserName=user)
                equipList = equipList + f"\n名称：{i['item_name']}\n类型：{self.equipType[str(i['item_type'])]}\n购买价：{i['total_price']}\n出售价：{i['price']}"
                if "des1" in i.keys():
                    des1 = i['des1'].strip().replace("<p>", "").replace("</p>", "").replace("<br>", "\n")
                    equipList = equipList + f"\n属性：{des1}"
                if "des2" in i.keys():
                    des2 = i['des2'].strip().replace("<p>", "").replace("</p>", "").replace("<br>", "\n")
                    equipList = equipList + f"\n介绍：{des2}"
                data = DownLoadImage(i['img'])
                if data['code'] == 200:
                    itchat.send_image(fileDir=data['filename'], toUserName=user)
                    os.remove(data['filename'])
                    itchat.send(msg=equipList, toUserName=user)

    def getEquipType(self):
        text = "类型名称"
        for name, value in self.equipType.items():
            text = text + f"\n{value}"
        print(text)
        return text

    def getEquipList(self, index='0'):
        response = self.getEquip()
        text = "装备名称-装备类型-装备价格-出售价格"
        for i in response:
            typeEquip = str(i['item_type'])
            if index == '0':
                text = text + f"\n{i['item_name']}-{self.equipType[typeEquip]}-{i['total_price']}-{i['price']}"
            else:
                if str(index) == typeEquip:
                    text = text + f"\n{i['item_name']}-{self.equipType[typeEquip]}-{i['total_price']}-{i['price']}"
        print(text)
        return text

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
    return HonorOfKings
