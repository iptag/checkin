# -*- coding: utf-8 -*-
"""
cron: 43 7 * * *
new Env('数码之家');
"""

import requests
import time
import json
import re

from sendNotify import send
from utils import get_data


class mydigit:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(cookie):
        result = ""
        headers = {
            "Cookie": cookie,
            "Host": "www.mydigit.cn",
            "Referer": "https://www.mydigit.cn/home.php",
            #User-Agent最好更换为自己的
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        url1 = 'https://www.mydigit.cn/k_misign-sign.html'
        s = requests.session()
        resp = s.get( url1, headers=headers )
        time.sleep(1)
        m = re.findall(r'name="formhash" value="([0-9a-z]+)"',resp.content.decode())
        formhash = m[0]
        url2 = 'https://www.mydigit.cn/plugin.php?id=k_misign:sign&operation=qiandao&format=text&formhash=' + formhash
        headers.update({'Referer': 'https://www.mydigit.cn/k_misign-sign.html'})
        resp2 = s.post( url2, headers=headers )
        time.sleep(1)
        n = re.findall(r'已签',resp2.content.decode())
        if n[0] == "已签":
            resp3 = s.get( url1, headers=headers )
            time.sleep(1)
            nn = re.findall(r'id="lxdays" value="([0-9]+)"|id="lxreward" value="([0-9]+)"|id="lxtdays" value="([0-9]+)"|class="author">([0-9a-zA-Z]+)<',resp3.content.decode())
            account = nn[0][3]
            result += f"账号名 {account} 今天已签到\n已连续签到：{nn[1][0]}天\n获得积分：{nn[2][1]}\n总签到：{nn[3][2]}天"
        else:
            result += f"有错误，请重新调试"
        s.close()
        return result

    def main(self):
        i = 1
        msg_all = ""
        for check_item in self.check_items:
            cookie = check_item.get("cookie")
            sign_msg = self.sign(cookie=cookie)
            msg = f"账号{i}签到状态: {sign_msg}\n"
            msg_all += msg + "\n"
            i += 1
        print(msg_all)
        return msg_all


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("MYDIGIT", [])
    res = mydigit(check_items=_check_items).main()
    send("数码之家", res)
