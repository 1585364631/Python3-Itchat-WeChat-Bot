import base64
import re
import uuid


def decode_image(src):
    print("解码图片")
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")
    else:
        raise Exception("Do not parse!")
    img = base64.urlsafe_b64decode(data)
    filename = "{}.{}".format(uuid.uuid4(), ext)
    with open(filename, "wb") as f:
        f.write(img)
    return filename


def encode_image(filename):
    print("编码图片")
    with open(filename, 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding='utf-8')
        return "data:image/jpeg;base64," + image_base64
