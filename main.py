import random
import re
import base64

import random
import time
import json
import cv2
import execjs
import requests

class jd:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.arr = [] 
        self.challenge = ""
        self.r = requests.Session()
    # 获取相应的数据
    def getCaptchaImg(self):
        dataUrl = "https://iv.jd.com/slide/g.html?appId=1604ebb2287&scene=login&product=click-bind-suspend&e=D5FI6BZO2XIN5ZMAFSFGM5OTZWSRUMREDLRVAGFNNWGPVTKZN2TDV53Q32SCAEXXGA5N7N7LEEUYOWE7WJHSZDBXGQ&lang=zh_CN&callback=jsonp_03548545356597772"
        r = self.r.get(dataUrl)
        r = r.text.replace("jsonp_03548545356597772(",'');
        r = json.loads(r.replace(")",''));
        # print('滑块返回的结果',r)
        self.challenge = (r['challenge'])
        bgImgData = base64.b64decode(r["bg"])
        bgFile = open("./img/captcha1.png", "wb")
        bgFile.write(bgImgData)
        bgFile.close()
        self.FindPic("./img/captcha1.png")
    def FindPic(self, target):
        """
        找出图像中最佳匹配位置
        :param target: 目标即背景图
        :param template: 模板即需要找到的图
        :return: 返回最佳匹配及其最差匹配和对应的坐标
        """
        template = cv2.imread('E:/Python_project/JD_slide/img/template.png', 0)
        # //灰度
        ret,template = cv2.threshold(template,20,100,cv2.THRESH_BINARY_INV)
        w, h = template.shape[::-1]
        img = cv2.imread(target, 0)
        ret,img_copy = cv2.threshold(img,137,190,130,cv2.THRESH_BINARY)
        # 应用模板匹配
        res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        top_left = max_loc
        position = round(top_left[0]*0.772+25)
        # print('定位为: ',position) 
        self.js_get_trace(position)
    def js_get_trace(self, distance):
        with open("./slider.js", encoding="utf-8") as f:
            r = f.read()
            f.close()
        content = execjs.compile(r)
        result = content.call("getSlide", distance)
        # print('滑块内容',result)
        self.test(result)
    def encodeGJ(self, arr):
        with open("test.js") as f:
            r = f.read()
            f.close()
        context = execjs.compile(r)
        result = context.call("getCoordinate", arr)
        # print('返回结果',result)
        self.test(result)
    def test(self, encodeGJ):
        dataUrl = "https://iv.jd.com/slide/s.html?d="+encodeGJ+"&c="+self.challenge+"&w=278&appId=1604ebb2287&scene=login&product=click-bind-suspend&e=D5FI6BZO2XIN5ZMAFSFGM5OTZWSRUMREDLRVAGFNNWGPVTKZN2TDV53Q32SCAEXXGA5N7N7LEEUYOWE7WJHSZDBXGQ&s=6991150360936174813&o=wft_fapiaoqwe&o1=0&u=https%3A%2F%2Fpassport.jd.com%2Fnew%2Flogin.aspx%3FReturnUrl%3Dhttps%253A%252F%252Fwww.jd.com%252F&lang=zh_CN&callback=jsonp_0583799690037224"
        # print('结果',dataUrl)
        # 延时成功率较高
        time.sleep(6)
        r = self.r.get(dataUrl)
        r = r.text.replace("jsonp_0583799690037224(",'');
        r = json.loads(r.replace(")",''));
        print('返回结果',r)
        if r["success"] == "0":
            print("验证错误")
        elif r["success"] == "1":
            print("验证成功!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        elif r["u"] == "2":
            print("需要重试")
    def login(self):
        self.getCaptchaImg()
if __name__ == '__main__':
    for index in range(100):
        print('执行第： ',index)
        jd('testuser'+str(index), 'password').login()