import urllib.request
import os
import datetime
import random


def DownLoadImage(url):
    print(url)
    try:
        name = str(round(datetime.datetime.now().timestamp() + random.randint(1, 99))) + ".jpg"
        urllib.request.urlretrieve(url, name)
        return {"code": 200, "filename": name}
    except:
        return {"code": 201, "msg": "下载失败"}
