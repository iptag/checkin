# -*- coding: utf-8 -*-
# @url: https://raw.githubusercontent.com/yxnwh/kevinxf/main/xF_DiDi_DZDZ_Sleep.py
# @author: zyf1118
"""
cron: 1 6,22 * * *
new Env('滴滴多走多赚-起床睡觉');
"""
import requests
import json, sys, os, re
import time, datetime,random

from sendNotify import send
from utils import get_data

requests.packages.urllib3.disable_warnings()

today = datetime.datetime.now().strftime('%Y-%m-%d')
mor_time = '07:00:00.00000000'
after_time = '23:00:00.00000000'
moringtime = '{} {}'.format (today, mor_time)
sleeptime = '{} {}'.format (today, after_time)

class DIDIsleep:
    def __init__(self, check_items):
        self.check_items = check_items
        
    #获取xpsid
    def get_xpsid(self):
        try:
            url = f'https://v.didi.cn/p/aXxR1oB'
            heards = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            }
            response = requests.head (url=url, headers=heards, verify=False)  # 获取响应请求头
            res = response.headers['Location']  # 获取响应请求头
            # print(res)
            r = re.compile (r'root_xpsid=(.*?)&channel_id')
            xpsid = r.findall (res)
            xpsid = xpsid[0]
            return xpsid
        except Exception as e:
            print (e)
    
    #睡觉
    @staticmethod
    def sleep(token,xpsid):
        try:
            url = f'https://res.xiaojukeji.com/sigma/api/sleep/sleep/v2?wsgsig=dd03-%2FbmamzeJR3QXGQJTThyOOv18ZuJqDzvOpFvUyJM1ZuJrGv%2BqxrbhQvEIOJQrGJGQPVzxPRAHQ3WnfpjwpEQmzRLaPJyXE%2BcyYhyiy763PujiGJiPSrWnRN28xJQV'
            heards = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://page.udache.com/",
                "Host": "res.xiaojukeji.com",
                "Origin": "https://page.udache.com",
                "ticket":f"{token}",
                "Content-Type":"application/json",
            }
            data = r'{"xbiz":"240300","prod_key":"ut-walk-bonus","xpsid":"1265f6d94e3e48f686f1be0245c27fd2","dchn":"aXxR1oB","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"1265f6d94e3e48f686f1be0245c27fd2","xpsid_from":"","xpsid_share":"","version":1,"source_from":"app","ticket":"Ag8aVeRbZ1yee4AsBI69GkodAzZQRoQqykuols0cKZEkzDluAzEMQNG7_JoYkKJESWzT5w5ZJkujADFcDXx3Y-z-4R0sJfFNN0VYRpqwCmmqqsJy0nqbJbxajDJdWJW0qK16jNaF1UheXhHeSBDeyTKs9jqn1mjRXfgkp7CTB5e_6__HTupN-Dor7xH6qL5JzNvQMaJrIPw8y9-T3wMAAP__","env":{"ticket":"Ag8aVeRbZ1yee4AsBI69GkodAzZQRoQqykuols0cKZEkzDluAzEMQNG7_JoYkKJESWzT5w5ZJkujADFcDXx3Y-z-4R0sJfFNN0VYRpqwCmmqqsJy0nqbJbxajDJdWJW0qK16jNaF1UheXhHeSBDeyTKs9jqn1mjRXfgkp7CTB5e_6__HTupN-Dor7xH6qL5JzNvQMaJrIPw8y9-T3wMAAP__","cityId":"21","longitude":113.81250027126737,"latitude":23.016204427083334,"newAppid":10000,"isHitButton":true,"ddfp":"99d8f16bacaef4eef6c151bcdfa095f0","deviceId":"99d8f16bacaef4eef6c151bcdfa095f0","appVersion":"6.2.4","userAgent":"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0","fromChannel":"1"},"city_id":"21"}'
            response = requests.post (url=url, headers=heards,verify=False,data=data)
            result = response.json()
            print("sleep#睡觉")
            print (result)
            errmsg = result['errmsg']
            if "睡觉状态错误" in errmsg:
                res = "睡觉状态错误"
            elif errmsg == 'success':
               res = "已执行睡觉命令"
            else:
               res = errmsg
            return res
        except Exception as e:
            print (e)
    
    #睡醒
    @staticmethod
    def wakeup(token,xpsid):
        try:
            url = f'https://res.xiaojukeji.com/sigma/api/sleep/wake/v2?wsgsig=dd03-UfTkqudHf%2B4nfF8UZV2awyM6Epv%2Fc9oqvBqBO%2BL3Epvhfd3OPVIdwyFKe84hfVcsxrU1zoBJg%2BKXGAWkvAwBxo2KBQgPfebhZqxdwRMHB%2BcjfF%2BtuFhMxReNd3Ct'
            heards = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://page.udache.com/",
                "Host": "res.xiaojukeji.com",
                "Origin": "https://page.udache.com",
                "ticket":f"{token}",
                "Content-Type":"application/json",
            }
            data = r'{"xbiz":"240300","prod_key":"ut-walk-bonus","xpsid":"46c633fd0c98480e858b4a0a414ef717","dchn":"aXxR1oB","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"46c633fd0c98480e858b4a0a414ef717","xpsid_from":"","xpsid_share":"","version":1,"source_from":"app","ticket":"Ag8aVeRbZ1yee4AsBI69GkodAzZQRoQqykuols0cKZEkzDluAzEMQNG7_JoYkKJESWzT5w5ZJkujADFcDXx3Y-z-4R0sJfFNN0VYRpqwCmmqqsJy0nqbJbxajDJdWJW0qK16jNaF1UheXhHeSBDeyTKs9jqn1mjRXfgkp7CTB5e_6__HTupN-Dor7xH6qL5JzNvQMaJrIPw8y9-T3wMAAP__","env":{"ticket":"Ag8aVeRbZ1yee4AsBI69GkodAzZQRoQqykuols0cKZEkzDluAzEMQNG7_JoYkKJESWzT5w5ZJkujADFcDXx3Y-z-4R0sJfFNN0VYRpqwCmmqqsJy0nqbJbxajDJdWJW0qK16jNaF1UheXhHeSBDeyTKs9jqn1mjRXfgkp7CTB5e_6__HTupN-Dor7xH6qL5JzNvQMaJrIPw8y9-T3wMAAP__","cityId":"21","longitude":113.81259847005208,"latitude":23.01628173828125,"newAppid":10000,"isHitButton":true,"ddfp":"99d8f16bacaef4eef6c151bcdfa095f0","deviceId":"99d8f16bacaef4eef6c151bcdfa095f0","appVersion":"6.2.4","userAgent":"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0","fromChannel":"1"},"city_id":"21"}'
            response = requests.post (url=url, headers=heards,verify=False,data=data)
            result = response.json()
            print("wakeup#睡醒")
            print (result)
            errmsg = result['errmsg']
            if "起床状态错误" in errmsg:
                res = "当前在睡醒状态,无法领取健康豆"
            elif errmsg == 'success':
                message_text = result['data']['message_text']
                if "只有多多休息" in message_text:
                    res = "当前在睡醒状态,无法领取健康豆"
                else:
                    bonus_amount = result['data']['bonus_amount']
                    res = f"已执行睡醒命令,获取{bonus_amount}健康豆"
            else:
                res = errmsg
            return res
        except Exception as e:
            print (e)

    def main(self):
        msg_all = ""
        i = 1
        for check_item in self.check_items:
            msg_tmp = ""
            token = check_item.get("token")
            xpsid = self.get_xpsid()
            nowtime = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
            print(nowtime)
            print(moringtime)
            print(sleeptime)
            if nowtime > moringtime and nowtime < sleeptime:
                msg_tmp = self.sleep (token=token,xpsid=xpsid)
            else:
                msg_tmp = self.wakeup (token=token,xpsid=xpsid)
            print(msg_tmp)
            msg = (
                f"账号 {i}\n------ 滴滴多走多赚-起床睡觉开始------\n"
                + msg_tmp
                + "\n------ 滴滴多走多赚-起床睡觉结束------"
            )
            i += 1
            msg_all += msg + "\n\n"
        return msg_all

if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("DIDI", [])
    res = DIDIsleep(check_items=_check_items).main()
    send("滴滴多走多赚-起床睡觉", res)  
