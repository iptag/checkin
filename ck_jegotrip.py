# -*- coding: utf-8 -*-
"""
cron: 31 7 * * *
new Env('无忧行签到');
打开app-我的-任务中心 很多链接都有token 格式应该是32位16进制数
感谢作者limoruirui https://github.com/limoruirui/misaka
"""
from json import loads, dumps
from base64 import b64decode, b64encode
from hashlib import md5 as md5Encode
from random import randint, choice
from time import time
from Crypto.Cipher import AES
from requests import post
from sendNotify import send
from utils import get_data

class AESCipher:
    def __init__(self, secretkey: str):
        self.key = secretkey  # 密钥

    def encrypt(self, text):
        cipher = AES.new(key=self.key.encode(), mode=AES.MODE_ECB)
        bs = AES.block_size
        pad = lambda s: s + (bs - len(s.encode()) % bs) * chr(bs - len(s.encode()) % bs)
        encrypted_text = cipher.encrypt(pad(text).encode())
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(key=self.key.encode(), mode=AES.MODE_ECB)
        decrypted_text = cipher.decrypt(encrypted_text)
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        return unpad(decrypted_text).decode('utf-8')


class jegotrip:
    def __init__(self, check_items):
        self.check_items = check_items
        self.headers = {
            "User-Agent": self.randomUA(),
            "Referer": "https://cdn.jegotrip.com.cn/"
        }
        self.ge = "93EFE107DDE6DE51"
        self.he = "online_jego_h5"
        self.fe = "01"
        self.taskId = ""
        self.msg = ""

    def randomUA(self):
        USER_AGENTS = ['Mozilla/5.0 (Linux; Android 10; ONEPLUS A5010 Build/QKQ1.191014.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045230 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (Linux; Android 9; Mi Note 3 Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045131 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (Linux; Android 10; GM1910 Build/QKQ1.190716.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045230 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (Linux; Android 9; 16T Build/PKQ1.190616.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044942 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044942 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (Linux; Android 11; Redmi K30 5G Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045511 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 source/jegotrip','Mozilla/5.0 (Linux; Android 10; M2006J10C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045230 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (Linux; Android 10; M2006J10C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045230 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (Linux; Android 10; ONEPLUS A6000 Build/QKQ1.190716.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045224 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (Linux; Android 9; MHA-AL00 Build/HUAWEIMHA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044942 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (Linux; Android 8.1.0; 16 X Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044942 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (Linux; Android 8.0.0; HTC U-3w Build/OPR6.170623.013; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044942 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (Linux; Android 10; LYA-AL00 Build/HUAWEILYA-AL00L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045230 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045131 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (Linux; Android 10; Redmi K20 Pro Premium Edition Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045227 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip','Mozilla/5.0 (Linux; Android 11; Redmi K20 Pro Premium Edition Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045513 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (Linux; Android 10; MI 8 Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045227 Mobile Safari/537.36 source/jegotrip','Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 source/jegotrip']
        RANDOM_UA = choice(USER_AGENTS)
        return RANDOM_UA

    def md5(self, text):
        m = md5Encode(text.encode(encoding='utf-8'))
        return m.hexdigest()

    def decrypt_key(self, encrypt_key):
        t = b64decode(encrypt_key).decode()
        a = t.split(";")
        if a and 3 == len(a):
            c = self.ge + a[1]
            n = self.md5(c)[8:24]
            return n

    def gene_encrypt_key(self):
        e = f"{int(time()*1000)}{randint(100, 999)}"
        i = self.ge + e
        a = self.md5(i)[8:24]
        c = f"{self.he};{e};{self.fe}"
        t = b64encode(c.encode("utf-8")).decode()
        return a, t

    def query_total_score(self):
        url = f"https://app.jegotrip.com.cn/api/service/member/v1/expireRewardQuery?token={self.token}&lang=zh_CN"
        encrypt_key = self.gene_encrypt_key()
        key = encrypt_key[0]
        sec = encrypt_key[1]
        body = {
            "sec": sec,
            "body": AESCipher(key).encrypt("{}")
        }
        encrypt_data = post(url, headers=self.headers, json=body).json()
        if encrypt_data["code"] == "0":
            encrypt_body = encrypt_data["body"]
            encrypt_sec = encrypt_data["sec"]
            decrypt_data = AESCipher(self.decrypt_key(encrypt_sec)).decrypt(encrypt_body)
            print(f"query_total_score的返回信息为：\n{decrypt_data}")
            total_score = loads(decrypt_data)["tripcoins"]
            print(f"查询成功, 你共有{total_score}点积分\n")
            self.msg += f", 你共有{total_score}点积分\n"

    def get_checkin_taskid(self):
        url = f"https://app.jegotrip.com.cn/api/service/v1/mission/sign/querySign?token={self.token}&lang=zh_CN"
        encrypt_key = self.gene_encrypt_key()
        key = encrypt_key[0]
        sec = encrypt_key[1]
        body = {
            "sec": sec,
            "body": AESCipher(key).encrypt("{}")
        }
        encrypt_data = post(url, headers=self.headers, json=body).json()
        if encrypt_data["code"] == "0":
            encrypt_body = encrypt_data["body"]
            encrypt_sec = encrypt_data["sec"]
            decrypt_data = AESCipher(self.decrypt_key(encrypt_sec)).decrypt(encrypt_body)
            print(f"get_checkin_taskid的返回信息为：\n{decrypt_data}")
            for checkin_task in eval(decrypt_data)[::-1]:
                task_status = checkin_task["isSign"]
                if task_status == 2:
                    self.taskId = checkin_task["id"]
                    #print(self.taskId)
                    return self.taskId
        if self.taskId == "":
            print("获取任务id失败 退出")
            exit(0)

    def checkin(self):
        url = f"https://app.jegotrip.com.cn/api/service/v1/mission/sign/userSign?token={self.token}&lang=zh_CN"
        encrypt_key = self.gene_encrypt_key()
        key = encrypt_key[0]
        sec = encrypt_key[1]
        body = {
            "sec": sec,
            "body": AESCipher(key).encrypt(f'{{"signConfigId":{self.get_checkin_taskid()}}}')
        }
        data = post(url, headers=self.headers, json=body).json()
        #print(f"checkin的返回信息为：\n{data}")
        if data["code"] == "0":
            self.msg += "签到成功"
            print(self.msg)
        else:
            self.msg += "签到失败"
            print(self.msg)

    def main(self):
        i = 1
        for check_item in self.check_items:
            self.msg += f"账号{i}签到状态\n"
            self.token = check_item.get("token")
            self.checkin()
            self.query_total_score()
            i += 1
        return self.msg


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("JEGOTRIP", [])
    res = jegotrip(check_items=_check_items).main()
    send("JEGOTRIP", res)
