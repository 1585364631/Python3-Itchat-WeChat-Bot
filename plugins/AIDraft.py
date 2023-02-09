import time
import requests
import json
import re
import datetime
import itchat
import os
from tools.DownLoad import DownLoadImage


class AIDraft:
    # 插件启动状态
    status = True
    # 插件名
    pluginName = "AIDraft"
    # 执行优先级（越小越快，最低0）
    priority = 99
    # 异步线程
    asynch = False
    # 匹配头
    startSearch = '画画 '
    searchHeader = "Draft"

    def run(self, msg, tag):
        if (tag in ["TEXT", "TEXTGroup"]) and (str(msg.text).lower().strip().startswith(self.startSearch.lower())):
            value = str(msg.text)[2:].strip()
            print(self.pluginName + "-----" + str(value))
            data = self.getDraftImage(value)
            print(data)
            if data["code"] == 200:
                itchat.send_image(fileDir=data['filename'], toUserName=str(msg.FromUserName).strip())
                os.remove(data['filename'])
            else:
                itchat.send(data['msg'], toUserName=str(msg.FromUserName).strip())

        if (tag in ["TEXT", "TEXTGroup"]) and (str(msg.text).lower().strip().startswith(self.searchHeader.lower())):
            value = str(msg.text)[5:].strip()
            if value == "模型列表":
                itchat.send(self.getModList(), toUserName=str(msg.FromUserName).strip())
            elif value == "帮助":
                itchat.send('''依次顺序为文本-图片高-图片宽-词库-模型ID\n例如：\n\nDraft \n太上老君\n512\n512\n1\n1''',
                            toUserName=str(msg.FromUserName).strip())
            else:
                text = value.split('\n')
                datas = [i for i in text if i != ""]
                print(datas)
                if len(datas) == 5:
                    data = self.getDraftImage(datas[0], int(datas[1]), int(datas[2]), int(datas[3]), int(datas[4]))
                    print(data)
                    if data["code"] == 200:
                        itchat.send_image(fileDir=data['filename'], toUserName=str(msg.FromUserName).strip())
                        os.remove(data['filename'])
                    else:
                        itchat.send(data['msg'], toUserName=str(msg.FromUserName).strip())

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
    def getModulList():
        data = "[" + requests.get("https://draft.art/static/js/main.d78907f3.js").text.split("var Ya=[")[1].split("]")[
            0] + "]"
        for i in re.compile('(id:(.*?),)').findall(data):
            data = data.replace(i[0], "")
        data = data.replace('showInOversea', '"showInOversea"').replace('discount', '"discount"').replace('price',
                                                                                                          '"price"').replace(
            'placeholder', '"placeholder"').replace('name', '"name"').replace('!1', '"!1"').replace('!0', '"!0"')
        data = eval(data)
        newdata = []
        ids = 1
        for i in data:
            if "discount" not in i:
                i['discount'] = 1
            try:
                newdata.append({
                    "id": ids,
                    "name": i['name'],
                    "price": i['discount'] * i['price']
                })
            except:
                newdata.append({
                    "id": ids,
                    "name": i['name'],
                    "price": 0
                })
            ids = ids + 1
        return newdata

    @staticmethod
    def writeModulConfig(data):
        try:
            f = open("DraftConfig.json", 'w+', encoding="utf-8")
            newdata = {
                "time": datetime.datetime.now().timestamp(),
                "data": data
            }
            f.write(json.dumps(newdata))
            f.close()
            return "更新文件成功"
        except PermissionError:
            return "文件存在但是无读写权限"

    @staticmethod
    def getModList():
        modelList = AIDraft.getModul()
        text = "模型ID--模型名称--使用价格"
        for i in modelList:
            text = text + '\n' + str(i['id']) + "--" + str(i['name']) + "--" + str(i['price'])
        return text

    @staticmethod
    def getModul():
        try:
            f = open("DraftConfig.json", 'r', encoding="utf-8")
            text = json.loads(f.read())
            f.close()
            if datetime.datetime.now().timestamp() - text["time"] > 900:
                data = AIDraft.getModulList()
                AIDraft.writeModulConfig(data)
                return data
            return text['data']
        except FileNotFoundError:
            AIDraft.writeModulConfig(AIDraft.getModulList())
            return AIDraft.getModul()
        except PermissionError:
            return "文件存在但是无读写权限"

    @staticmethod
    def getDraftImage(text="", height=512, width=512, words=1, modelId=1, initImage="null"):
        modelList = AIDraft.getModul()
        if modelId not in range(1, 7):
            return {"code": 201, "msg": "模型ID不正确"}
        if modelList[modelId - 1]['price'] != 0:
            return {"code": 201, "msg": "这个模型要钱，不给你用"}
        if modelId == 1:
            modelId = 0
        if text == "":
            text = \
            json.loads(requests.get("https://api.draft.art/api/util/aiDraw/fashion/prompt?modelId=0").text)['data'][
                'zh']
        payload = f"------WebKitFormBoundaryXREf9UjHzRdwvygY\r\nContent-Disposition: form-data; name=\"keyword\"\r\n\r\n{text}\r\n------WebKitFormBoundaryXREf9UjHzRdwvygY\r\nContent-Disposition: form-data; name=\"height\"\r\n\r\n{height}\r\n------WebKitFormBoundaryXREf9UjHzRdwvygY\r\nContent-Disposition: form-data; name=\"width\"\r\n\r\n{width}\r\n------WebKitFormBoundaryXREf9UjHzRdwvygY\r\nContent-Disposition: form-data; name=\"incantationId\"\r\n\r\n{words}\r\n------WebKitFormBoundaryXREf9UjHzRdwvygY\r\nContent-Disposition: form-data; name=\"initImage\"\r\n\r\n{initImage}\r\n------WebKitFormBoundaryXREf9UjHzRdwvygY\r\nContent-Disposition: form-data; name=\"modelId\"\r\n\r\n{modelId}\r\n------WebKitFormBoundaryXREf9UjHzRdwvygY\r\nContent-Disposition: form-data; name=\"language\"\r\n\r\nzh\r\n------WebKitFormBoundaryXREf9UjHzRdwvygY--\r\n"

        headers = {
            "GRAPH-ORIGIN-T": "abbdf62edcbe4a108342897af8fb7bc5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryXREf9UjHzRdwvygY"
        }
        datas = json.loads(requests.post("https://api.draft.art/api/util/aiDraw/create", data=payload.encode("utf8"),
                                         headers=headers).text)
        print(datas)
        imgId = datas['data']['id']
        imgUrl = ""
        while True:
            time.sleep(5)
            data = json.loads(requests.post("https://api.draft.art/api/util/aiDraw/get/" + str(imgId)).text)
            if data['data']['status'] == "succeeded":
                imgUrl = data['data']['download']
                break
        return DownLoadImage(imgUrl)


def getPluginClass():
    return AIDraft
