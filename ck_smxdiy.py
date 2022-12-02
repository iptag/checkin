# -*- coding: utf-8 -*-
"""
cron: 53 7 * * *
new Env('smxdiy');
"""

import requests
import time
import json
import re
from urllib.parse import urlencode

from sendNotify import send
from utils import get_data


class smxdiy:
    def __init__(self, check_items):
        self.check_items = check_items

    @staticmethod
    def sign(cookie):
        result = ""
        headers = {
            "Cookie": cookie,
            "Host": "www.smxdiy.com",
            #User-Agent最好更换为自己的
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        }
        url1 = 'http://www.smxdiy.com/plugin.php?id=dc_signin:sign&infloat=yes&handlekey=sign&inajax=1&ajaxtarget=fwin_content_sign'
        s = requests.session()
        resp = s.get( url1, headers=headers )
        time.sleep(1)
        n = re.findall(r'签过到',resp.content.decode())
        print(n)
        if not n:
            m = re.findall(r'name="formhash" value="([0-9a-z]+)"',resp.content.decode())
            print(m[0])
            url2 = 'http://www.smxdiy.com/plugin.php?id=dc_signin:sign&inajax=1'
            headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
            payload = {'formhash':m[0], 'signsubmit':'yes', 'handlekey':'signin', 'emotid':'1', 'referer':'http://www.smxdiy.com/home.php?mod=space&uid=15743&content=开心每一天'}
            payloads = json.dumps(payload)
            body = urlencode(json.loads(payloads))
            resp2 = s.post( url2, headers=headers, data=body )
            #print(resp2.content.decode())
            result += f"首次签到成功~\n\n"
            del headers['Content-Type']
            time.sleep(1)
        else:
            result += f"今天已经签过到啦~无需重复签到~\n\n"
        url3 = 'http://www.smxdiy.com/plugin.php?id=dc_signin'
        resp3 = s.get( url3, headers=headers )
        time.sleep(1)
        htmldata = resp3.content.decode()
        #print(htmldata)
        account = re.findall(r'尊敬的<b>([a-z]+)',htmldata)
        totalday = re.findall(r'累计已签到：([0-9]+)天',htmldata)
        signday = re.findall(r'本月已签到：([0-9]+)天',htmldata)
        award = re.findall(r'已获得分享指数：([0-9]+)个',htmldata)
        result += f"账号名 {account[0]} 今天已签到\n本月已签到：{signday[0]}天\n累计已签到：{totalday[0]}天\n累计获得积分：{award[0]}分\n"
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
        return msg_all
        print(msg_all)


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("SMXDIY", [])
    res = smxdiy(check_items=_check_items).main()
    send("smxdiy", res)
