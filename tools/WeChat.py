import itchat


# 微信机器人登入重写
def wechatLogin(enableCmdQR):
    print("扫描二维码登入")
    loginid = itchat.get_QRuuid()
    itchat.get_QR(uuid=loginid, enableCmdQR=enableCmdQR)
    waitForConfirm = True
    waitForConfirm1 = True
    while True:
        status = itchat.check_login(loginid)
        if status == '200':
            print("登入成功!")
            itchat.web_init()
            itchat.show_mobile_login()
            break
        elif status == '400':
            if waitForConfirm1:
                print("登入状态码400")
                waitForConfirm1 = False
        elif status == '201':
            if waitForConfirm:
                print('请确认登入')
                waitForConfirm = False


# 启动机器人
def startBot(enableCmdQR):
    wechatLogin(enableCmdQR)
    itchat.get_contact()
    itchat.start_receiving()
    itchat.run()
