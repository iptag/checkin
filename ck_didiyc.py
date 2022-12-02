# -*- coding: utf-8 -*-
# @url: https://raw.githubusercontent.com/zyf1118/kevinxf/main/xF_DiDiYC_sign.py
# @author: zyf1118
"""
cron: 53 8 * * *
new Env('滴滴有车');
"""
import requests
import json,sys,os,re
import time,datetime,random

from sendNotify import send
from utils import get_data

requests.packages.urllib3.disable_warnings()

wsgsig=['dd03-vx9tq2onDp0IZqcYVoABxTjsa%2BXNwlstUQ6fOSmVa%2BX%2BZhfRmNkDw6zkAz0%2BZA8rsJ2%2BzMKjCoJLpecxVoEAOMK%2FBzf2SAJmXo6ax6Nre%2BnNYVNkX72aP6KjAJE',
        'dd03-67TGcdCHNXqCW0FVDMhX%2B%2F%2B650AFtbkyCIqj4r3350AEWfAm9TIW%2B9cKMnqEWXIwEPUQLAXc%2BWT0%2FiFqd1%2Fn%2Be36LslfUXIyD61n%2BAgNL096XnZxBMZUNl%2BN%2BXO',
        'dd03-rxqml47pGugrvrGTzy%2FbOp8ud3nWyknnyQTDxoGxd3nXv%2FDzSNEfP8%2BSFQgXvBJlYJP3Q%2BvlFR3UTdGPxKw9RJGuE3%2BtZa8rPod9xp3uF3KrvEbhPolCP3KkEQ9',
        'dd03-%2FbmamzeJR3QXGQJTThyOOv18ZuJqDzvOpFvUyJM1ZuJrGv%2BqxrbhQvEIOJQrGJGQPVzxPRAHQ3WnfpjwpEQmzRLaPJyXE%2BcyYhyiy763PujiGJiPSrWnRN28xJQV',
        'dd03-UfTkqudHf%2B4nfF8UZV2awyM6Epv%2Fc9oqvBqBO%2BL3Epvhfd3OPVIdwyFKe84hfVcsxrU1zoBJg%2BKXGAWkvAwBxo2KBQgPfebhZqxdwRMHB%2BcjfF%2BtuFhMxReNd3Ct',
        'dd03-CugL8XzfY9YxloS582DSCDiDQ%2F1u%2Fv656T3ZgbXEQ%2F1vlzPd%2BIjSDtoevAYvlNq74M7qAjmev9YTVReH6ScSftv0o%2Fqul7%2F6JP4RCcm9uqLZkvw48SGzfjzAZ9YY',
        'dd03-aScF%2FD3Xy4FqxzWqMzcXogciSvVXYQRtNv7%2FYmClSvVWxo8R58nVS0KUxKFWx8frH43PpggVz3HVRJ3x2z8wYgNlxR6yPzfqM%2BNhZg7%2FzKHjx3Nr2z7kTXDVwKE',
        'dd03-CugL8XzfY9YxloS582DSCDiDQ%2F1u%2Fv656T3ZgbXEQ%2F1vlzPd%2BIjSDtoevAYvlNq74M7qAjmev9YTVReH6ScSftv0o%2Fqul7%2F6JP4RCcm9uqLZkvw48SGzfjzAZ9YY',
        'dd03-NEvAAAqxzcF7%2B%2B%2Fqb0pV6dhOTjV2J3xtacmlHlYpTjV1%2B7IRDn8q5EhywDF1%2BpArgjiS8drvwbH42uLxbbRXIkhWyD5M4z1rb0ok6hZWwjl4MpFhcnXVIalvPDH',
        'dd03-DUXVE0SysCEZ%2BS1O7nX62jMR%2FsUyJZPj5jQ9LikS%2FsUz%2Bx6vNgDF1DxxrbEz%2BLdh3coI4cPvqjIw221TJXgA1tVvlnaPM2APJXba1tURrbhPMLBt7ntC1DhYks9',
        'dd03-wDXIwYa7Z54GDovErARRsS5KRwvBGvJAtdQwkMILRwvADzyHh%2FDPqwA6uL4ADNnCVkoVtSd5vMfDe4v7sevTrwh%2Bu5baf4zBrAXPqLEEYICcD7j3kqcRsSA4YL1',
        'dd03-y3uI01tMPCX7nJYRt2No3SQ1vs02i8IprMnw%2BTv8vs01n4xXjP7P45iNQbX1nQkTXTjV1LW%2BRcQ4rzYhq5iP42QgRgRBt8xzsZmQ%2BSj3O0R8t3PzsSs%2F4SWLyCq',
        'dd03-%2Fep12zdOxaJXJ8w9TGpxE42xphQq%2BJMdpCsTaJLuphQrJNZ5xWKYFvFRyBJrJz%2FfPsWkGRapzA0s5QwJTjQSFKAzRhci73VGSjvvFK9zzkgl7%2BYgoDuPaoLzRaL',
        'dd03-z6%2BZsOikr8p3Z5vssNK6z5jrjz%2B6wIJZqJCLQ6QWjz%2B5ZMyhioR2yStns%2Bp5ZwnvWQGexwnmtNs8pPvXsv87yZnnm3n6T2oPtNbMzwtlnJj6vwGPsRbKzwgonJk',
        'dd03-0%2F1PtGPrF8UO5avU3tAazsYkgzEp2EJz1Xe5RjhjgzEo5AynJDwIzCYsG%2BUo5hnx70aFwbSt0NPTJUvr3fHNzgSsb3wpHdop4tF6ybYqcJYp7hGp3GF4ybLvcJw',
        'dd03-rDByxRBD9w%2BsAUn7w966q%2BEfC5pVFhGFydLKl72aC5pUAliMS%2FV7rp9AcS%2BUAEv0YkHbszEBbTCXfan4wVa2ruEA0ZgVdrsex95Jqz9CGPcVCEJewl5LqzU2GPd',
        'dd03-gUaMGbSXHChPMWOhInVo1fTi3saoHj2QHj5YNXkl3sapMnTs3glT3fxUKbhpMGUONc1r2GPqJcwS4cOkKbHv1fMV8sVQLW9Q8nBlNWIUKiYwLWSoIsEz%2BfOhJXq',
        'dd03-ZB27DIBhLttb1gkuUiIX8TLU7DDe6CFyWfdRKw2t7DDd1Ghmkixy8M9i%2Bjtd1nYwqm9i56EmNiogNskqUgESKTBU%2BfiC1glSUnHO8xBr3DbG2ihpUgIW76Um3jq',
        'dd03-20QwPlA2%2FILbbHoaEks8lhBLsPSeg68eG9XIrA1KsPSdb2R6dkN5lha3j2LdbOsgA%2Ft9mrF7i1BgExoK9dzMldHNWIIA9TWN9ao2qkICWL9ebHs%2B0d71khHIiL5',
        'dd03-35eouVsWdxONxlnc0%2BaNWavjG6HIYqGHFK14i9ukG6HHxUiAgphNWrjVgTOHxevJDR5CVhXrfSVKRAnf0QMHUURrg1x6OF%2BcE3H4iaujgYkaOFpcbQA8WrnqgHY',
        'dd03-qRg6qKKGw8DUhpRWx14yy%2BGcozttku3szw3OOycdoztshyoQT1jxw%2B3Fz%2BDsh%2BXqZ57hz8NBzoNrX3RwPYNpxuNERz8tUztXwOsOxQbCzuf%2FV3nWx1sSy%2BJGx%2BE',
        'dd03-zzyKkOo5PQ82t3sQsSuQOLnIvJz7W%2BchqOjyw6mNvJz8tKXZiL3ROSz8Qu88tuojWHnXRwR5QRb5lpspswWSQSJNQJc4tzultPnYx5R3QzKGrzzrswzuw2v8zQd',
        'dd03-XGGZ8J%2FbhAtQdOYFue33BNV0tqDTaxI7YaKLgzOAtqDSdZxfQls2DNrai9tSdHk5yh%2BeA7ldiaopC6YAue4JB7SA%2FAtkf1rLulKLfyqCWVnldOTKul4KgvYC%2F9S',
        'dd03-DOgz5gRWq%2FAYTS%2F26v82Acsji9qzOZBC5z3Jdsjki9qyTxlJN4j8AcuVtqAyTLwA387cDDoXsrMxv2%2F5KKfKAfX%2Fs9HyTIYG8NK0BtnjrV5uZ5LDJvfKAWWUrq5',
        'dd03-kQNDYoKdpT7kl4cdP27UVJJBxMyj%2FNsaRxDm%2F4cGxMyilJf2Z2QtUQ3gSx7ilv8cT60pXuNdSwchtoc%2BPINqUJcETYN%2Fr7DdOSbqU3JgTO%2BqrRJEQP%2B%2FV%2BbfSTd',
        'dd03-RnANOxOD1Z3H9sJdnUHQlIrfJ2u%2Ben09kqMvqH%2FaJ2uN9jj1WEUokZZA4P3N9CubiAIsnPrD4OgMGgmNmd5plZPCN2NIF0zGlUBwqLxCNPNHaitCnE6xlZqa2ZA'
        ]

class DIDIYC:
    def __init__(self, check_items):
        self.check_items = check_items
    
    #获取xpsid
    def get_xpsid(self):
        imei = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 32))
        url = f'https://v.didi.cn/p/DpzAd35'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        }
        response = requests.head(url=url, headers=heards, verify=False)    #获取响应请求头
        result = response.headers['Location']                                  #获取响应请求头
        r = re.compile (r'root_xpsid=(.*?)&channel_id')
        #xpsid = r.findall (result)[0].split("&")[0]
        xpsid = r.findall (result)[0]
        return xpsid,imei

    #获取dchn
    def get_dchn(self):
        nowtime = int(round(time.time() * 1000))
        url = f'https://conf.diditaxi.com.cn/one/page?_t={nowtime}&access_key_id=1&appVersion=6.2.4&appversion=6.2.4&biz_type=1&card_nav_id=dache_anycar&channel=102&clientType=1&datatype=101&imei=99d8f16bacaef4eef6c151bcdfa095f0&imsi=&lang=zh-CN&lat=23.01638904876869&lng=113.8122117519379&location_lat=23.01638834635417&location_lng=113.8122121853299&maptype=soso&mobileType=iPhone%2011&model=iPhone12%2C1&networkType=WIFI&origin_id=1&os=15.0&osType=1&osVersion=15.0&platform_type=1&sig=7eafa42e548185d7f1cf5e841ceb05b82a671e40&start_utc_offset=480&terminal_id=1&timestamp={nowtime}&token={token}&trip_cityid=-1&uid=281474990465673&userRole=1&utc_offset=480&v6x_version=1'
        heards = {
            "user-agent": r"OneTravel/6.2.4 (iPhone; iOS 15.0; Scale/2.00)",
        }
        response = requests.get(url=url, headers=heards, verify=False)
        result = response.json()
        name_list = result['data']['nav_list']
        for i in range(len(name_list)):
            name = name_list[i]['name']
            if name == '走路赚钱':
                dchn = name_list[i]['link']
                dchn = dchn[20:]
        return dchn

    #领取瓜分奖励
    @staticmethod
    def reward(token,xpsid,imei,id,wsgsig):
        wsgsig1 = wsgsig[random.randint(0, 25)]
        uid = ''.join(random.sample('01234657890123456789', 15))  # 281474990465673
        try:
            url = f'https://ut.xiaojukeji.com/ut/kappa/api/owner/obtain?wsgsig={wsgsig1}'
            headers = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://page.udache.com/",
                "Host": "ut.xiaojukeji.com",
                "Origin": "https://page.udache.com",
                "Content-Type":"application/json",
            }
            data = r'{"xbiz":"","prod_key":"","xpsid":"","dchn":"","xoid":"2dcb602b-c319-44d1-93d3-811faeca4b82","uid":"' + f"{uid}" + '","xenv":"passenger","xspm_from":"ut-carowner-service.index.c757.1","xpsid_root":"' +f"{xpsid}" +'","xpsid_from":"' +f"{xpsid}" +'","xpsid_share":"","platform_type":1,"token":"' + f"{token}" + r'","env":{"newTicket":"' + f"{token}" + r'","isOpenWeb":true,"ticket":"' + f"{token}" + r'","cityId":"21","longitude":"113.812232","latitude":"23.016550","xAxes":"0","yAxes":"0","newAppid":"10000","isHitButton":true,"ddfp":"' + f"{imei}" + r'","deviceId":"' + f"{imei}" + r'","appVersion":"6.2.4","userAgent":"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0","fromChannel":"1"},"aid":"' + f"{id}" + '","source":1}'
            response = requests.post(url=url, headers=headers,verify=False,data=data)
            result = response.json()
            print("reward#领取瓜分奖励")
            print(result)
            errmsg = result['errmsg']
            if errmsg == "success":
                res = f"领取奖励成功"
            else:
                res = errmsg
            return res
        except Exception as e:
            print (e)

    #获取活动id
    @staticmethod
    def get_id(token,xpsid,imei,wsgsig):
        wsgsig1 = wsgsig[random.randint(0, 25)]
        uid = ''.join(random.sample('01234657890123456789', 15))  # 281474990465673
        try:
            url = f'https://ut.xiaojukeji.com/ut/kappa/api/owner/getActivityInfo?wsgsig={wsgsig1}'
            headers = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://page.udache.com/",
                "Host": "ut.xiaojukeji.com",
                "Origin": "https://page.udache.com",
                "Content-Type":"application/json",
            }
            data = r'{"xbiz":"","prod_key":"","xpsid":"","dchn":"","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f"{uid}" + '","xenv":"passenger","xspm_from":"ut-carowner-service.index.c757.1","xpsid_root":"' +f"{xpsid}" +'","xpsid_from":"' +f"{xpsid}" +'","xpsid_share":"","platform_type":1,"token":"' + f"{token}" + r'","env":{"newTicket":"' + f"{token}" + r'","isOpenWeb":true,"ticket":"' + f"{token}" + r'","cityId":"21","longitude":"113.812516","latitude":"23.016350","xAxes":"0","yAxes":"0","newAppid":"10000","isHitButton":true,"ddfp":"' + f"{imei}" + r'","deviceId":"' + f"{imei}" + r'","appVersion":"6.2.4","userAgent":"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0","fromChannel":"1"},"source":1}'
            response = requests.post(url=url, headers=headers,verify=False,data=data)
            result = response.json()
            print("get_id#获取活动id")
            print(result)
            id = result['data']['id']
            return id
        except Exception as e:
            print (e)

    #签到
    @staticmethod
    def sign(token,xpsid,imei,id,wsgsig):
        wsgsig1 = wsgsig[random.randint(0, 25)]
        uid = ''.join(random.sample('01234657890123456789', 15))  # 281474990465673
        try:
            url = f'https://ut.xiaojukeji.com/ut/kappa/api/owner/sign?wsgsig={wsgsig1}'
            heards = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://page.udache.com/",
                "Host": "ut.xiaojukeji.com",
                "Origin": "https://page.udache.com",
                "ticket":f"{token}",
                "Content-Type":"application/json",
            }
            data = r'{"xbiz":"","prod_key":"","xpsid":"","dchn":"","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f"{uid}" + '","xenv":"passenger","xspm_from":"ut-carowner-service.index.c757.1","xpsid_root":"' +f"{xpsid}" +'","xpsid_from":"' +f"{xpsid}" +'","xpsid_share":"","platform_type":1,"token":"' + f"{token}" + r'","env":{"newTicket":"' + f"{token}" + r'","isOpenWeb":true,"ticket":"' + f"{token}" + r'","cityId":"21","longitude":"113.812232","latitude":"23.016550","xAxes":"0","yAxes":"0","newAppid":"10000","isHitButton":true,"ddfp":"' + f"{imei}" + r'","deviceId":"' + f"{imei}" + r'","appVersion":"6.2.4","userAgent":"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0","fromChannel":"1"},"aid":"' + f"{id}" + '"}'
            response = requests.post(url=url, headers=heards,verify=False,data=data)
            result = response.json()
            print("sign#签到")
            print(result)
            errmsg = result['errmsg']
            if "success" in errmsg:
                res = f"今日成功参加瓜分活动"
            else:
                if "重复签到" in errmsg:
                    res = f"今日已参加瓜分，无需重复执行"
                else:
                    res = errmsg
            return res
        except Exception as e:
            print (e)

    def main(self):
        msg_all = ""
        i = 1
        for check_item in self.check_items:
            token = check_item.get("token")
            xpsid,imei = self.get_xpsid()
            id = self.get_id(token=token, xpsid=xpsid, imei=imei, wsgsig=wsgsig)
            reward_msg = self.reward(token=token, xpsid=xpsid, imei=imei, id=id, wsgsig=wsgsig)
            time.sleep (2)
            id = self.get_id(token=token, xpsid=xpsid, imei=imei, wsgsig=wsgsig)
            sign_msg = self.sign(token=token, xpsid=xpsid, imei=imei, id=id, wsgsig=wsgsig)
            msg = (
                f"账号 {i}\n------ 滴滴有车领取奖励结果 ------\n"
                + reward_msg
                + "\n------ 滴滴有车参加瓜分结果 ------\n"
                + sign_msg
            )
            i += 1
            msg_all += msg + "\n\n"        
        return msg_all

if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("DIDI", [])
    res = DIDIYC(check_items=_check_items).main()
    send("滴滴有车签到瓜分", res)
