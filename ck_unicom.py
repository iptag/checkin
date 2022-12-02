# -- coding: utf-8 --
"""
cron: 31 9 * * *
const $ = new Env('联通阅读');
联通app抽奖 入口:联通app 搜索 阅读专区 进入话费派送中
感谢作者 limoruirui https://github.com/limoruirui
"""
from requests import post
from time import sleep, time
from datetime import datetime
from hashlib import md5 as md5Encode
from random import randint, uniform
from sys import exit
from Crypto.Cipher import AES
from base64 import b64encode
from binascii import b2a_hex
from json import dumps
from sendNotify import send
from utils import get_data

class Unicom:
    def __init__(self, check_items):
        self.check_items = check_items
        self.headers = {
            "Host": "10010.woread.com.cn",
            "Content-Type": "application/json;charset=utf-8",
            "Origin": "https://10010.woread.com.cn",
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{randint(89, 103)}.0.{randint(100, 999)}.{randint(100, 999)} Safari/537.36",
            "Referer": "https://10010.woread.com.cn/ng_woread/",
        }
        self.fail_num = 0
        self.msg = ''

    def AES_Encrypt(self, key, data, iv=None, mode="ECB"):
        block_size = AES.block_size
        if len(key) <= 16:
            key_size = AES.key_size[0]
        elif len(key) > 24:
            key_size = AES.key_size[2]
        else:
            key_size = AES.key_size[1]
        if len(key) > key_size:
            key = key[:key_size]
        else:
            if len(key) % key_size != 0:
                key = key + (key_size - len(key) % key_size) * chr(0)
        key = key.encode("utf-8")
        if mode == "ECB":
            mode = AES.MODE_ECB
        else:
            mode = AES.MODE_CBC
        if iv is None:
            cipher = AES.new(key, mode)
        elif isinstance(iv, str):
            iv = iv[:block_size]
            cipher = AES.new(key, mode, iv.encode("utf-8"))
        else:
            iv = iv[:block_size]
            cipher = AES.new(key, mode, iv)
        pad = lambda s: s + (block_size - len(s.encode()) % block_size) * chr(block_size - len(s.encode()) % block_size)
        encrypt_data = b2a_hex(cipher.encrypt(pad(data).encode("utf8")))
        return encrypt_data.decode('utf8')
    
    def md5(self, str):
        m = md5Encode(str.encode(encoding='utf-8'))
        return m.hexdigest()

    def req(self, url, crypt_text):
        body = {
            "sign": b64encode(self.AES_Encrypt(self.headers["accesstoken"][-16:], crypt_text, iv="16-Bytes--String", mode="CBC").encode()).decode()
        }
        self.headers["Content-Length"] = str(len(dumps(body).replace(" ", "")))
        data = post(url, headers=self.headers, json=body).json()
        return data

    def referer_login(self):
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        url = f"https://10010.woread.com.cn/ng_woread_service/rest/app/auth/10000002/{round(time() * 1000)}/{self.md5(f'100000027k1HcDL8RKvc{round(time() * 1000)}')}"
        crypt_text = f'{{"timestamp":"{date}"}}'
        body = {
            "sign": b64encode(self.AES_Encrypt("1234567890abcdef", crypt_text).encode()).decode()
        }
        self.headers["Content-Length"] = str(len(str(body)) - 1)
        data = post(url, headers=self.headers, json=body).json()
        if data["code"] == "0000":
            self.headers["accesstoken"] = data["data"]["accesstoken"]
        else:
            print(f"设备登录失败,日志为{data}")
            exit(0)

    def get_userinfo(self):
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        url = "https://10010.woread.com.cn/ng_woread_service/rest/account/login"
        crypt_text = f'{{"phone":"{self.phone_num}","timestamp":"{date}"}}'
        data = self.req(url, crypt_text)
        if data["code"] == "0000":
            self.userinfo = data["data"]
        else:
            print(f"手机号登录失败, 日志为{data}")
            exit(0)

    def watch_video(self):
        print("看广告获取积分任务: ")
        url = "https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/obtainScoreByAd"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"value":"947728124","timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        for i in range(3):
            data = self.req(url, crypt_text)
            print(data)
            if self.fail_num == 3:
                print("当前任务出现异常 且错误次数达到3次 请手动检查")
                self.msg +=  "当前任务出现异常 且错误次数达到3次 请手动检查"
                exit(0)
            if data["code"] == "9999":
                print("当前任务出现异常 正在重新执行")
                self.fail_num += 1
                self.main()
            sleep(uniform(2, 8))

    def read_novel(self):
        print("正在执行观看150次小说, 此过程较久, 最大时长为150 * 8s = 20min")
        for i in range(150):
            date = datetime.today().__format__("%Y%m%d%H%M%S")
            chapterAllIndex = randint(100000000, 999999999)
            cntIndex = randint(1000000, 9999999)
            url = f"https://10010.woread.com.cn/ng_woread_service/rest/cnt/wordsDetail?catid={randint(100000, 999999)}&pageIndex={randint(10000, 99999)}&cardid={randint(10000, 99999)}&cntindex={cntIndex}&chapterallindex={chapterAllIndex}&chapterseno=3"
            crypt_text = f'{{"chapterAllIndex":{chapterAllIndex},"cntIndex":{cntIndex},"cntTypeFlag":"1","timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
            self.req(url, crypt_text)
            sleep(uniform(2, 8))

    def query_score(self):
        url = "https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/queryUserScore"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"activeIndex":{self.activeIndex},"timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        total_score = data["data"]["validScore"]
        self.lotter_num = int(total_score / 50)
        print(f"你的账号当前有积分{total_score}, 可以抽奖{self.lotter_num}次")

    def get_activetion_id(self):
        url = "https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/queryActiveInfo"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        if data["code"] == "0000":
            self.activeIndex = data["data"]["activeindex"]
        else:
            print(f"活动id获取失败 将影响抽奖和查询积分")

    def lotter(self):
        url = "https://10010.woread.com.cn/ng_woread_service/rest/activity/yearEnd/handleDrawLottery"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"activeIndex":{self.activeIndex},"timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        if data["code"] == "0000":
            print(f"抽奖成功, 获得{data['data']['prizename']}")
        else:
            print(f"抽奖失败, 日志为{data}")

    def watch_ad(self):
        print("观看广告得话费红包: ")
        url = "https://10010.woread.com.cn/ng_woread_service/rest/activity/userTakeActive"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"activeIndex":6880,"timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        print(data)

    def exchange(self):
        # ticketValue activeid来自于https://10010.woread.com.cn/ng_woread_service/rest/phone/vouchers/getSysConfig get请求
        # {"ticketValue":"300","activeid":"61yd210901","timestamp":"20220816213709","token":"","userId":"","userIndex":,"userAccount":"","verifyCode":""}
        url = "https://10010.woread.com.cn/ng_woread_service/rest/phone/vouchers/exchange"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"ticketValue":"300","activeid":"61yd210901","timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        print(data)

    def query_red(self):
        url = "https://10010.woread.com.cn/ng_woread_service/rest/phone/vouchers/queryTicketAccount"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        if data["code"] == "0000":
            can_use_red = data["data"]["usableNum"] / 100
            if can_use_red >= 3:
                print(f"查询成功 你当前有话费红包{can_use_red} 可以去兑换了")
                self.msg += f"查询成功 你当前有话费红包{can_use_red} 可以去兑换了"
            else:
                print(f"查询成功 你当前有话费红包{can_use_red} 不足兑换的最低额度")
                self.msg += f"查询成功 你当前有话费红包{can_use_red} 不足兑换的最低额度"

    def main(self):
        i = 1
        for check_item in self.check_items:
            self.phone_num = check_item.get("phone")
            self.referer_login()
            self.get_userinfo()
            self.watch_video()
            self.get_activetion_id()
            self.read_novel()
            self.query_score()
            self.watch_ad()
            for i in range(self.lotter_num):
                self.lotter()
                sleep(2)
            self.query_score()
            self.query_red()
            i += 1
        return self.msg


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("UNICOM", [])
    res = Unicom(check_items=_check_items).main()
    send("联通", res)
