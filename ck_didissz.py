# -*- coding: utf-8 -*-
# @url: https://raw.githubusercontent.com/yxnwh/kevinxf/main/xF_DiDi_ssz.py
# @author: zyf1118
"""
cron: 23 8,14 * * *
new Env('滴滴刷刷赚签到');
"""
import requests
import json, sys, os, re
import time, datetime,random

from sendNotify import send
from utils import get_data

requests.packages.urllib3.disable_warnings ()

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

class DIDIssz:
    def __init__(self, check_items):
        self.check_items = check_items

    def get_xpsid(self):
        try:
            url = f'https://v.didi.cn/p/7mPlO68'
            heards = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            }
            response = requests.head (url=url, headers=heards, verify=False)  # 获取响应请求头
            res = response.headers['Location']  # 获取响应请求头
            r = re.compile (r'root_xpsid=(.*?)&channel_id')
            xpsid = r.findall (res)[0].split("&")[0]
            return xpsid
        except Exception as e:
            print (e)

    #查看福利金
    @staticmethod
    def get_fulijin(token,wsgsig):
        try:
            wsgsig1 = wsgsig[random.randint (0, 25)]
            nowtime = int (round (time.time () * 1000))
            info_url = f'https://rewards.xiaojukeji.com/loyalty_credit/bonus/getWelfareUsage4Wallet?wsgsig={wsgsig1}&token={token}&city_id=21'
            info_headers = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://page.udache.com/",
                "origin": "https://page.udache.com",
                "content-type": "application/json",
                "host": "rewards.xiaojukeji.com",
            }
            response = requests.get (url=info_url, headers=info_headers, verify=False)
            result = response.json()
            print(result)
            balance = result['data']['balance']
            res = f"现总共有{balance}福利金"
            return res
        except Exception as e:
            print(e)
    
    #执行积分签到
    @staticmethod
    def do_sign(token,xpsid,wsgsig):
        try:
            uid = ''.join (random.sample ('01234657890123456789', 15))     #281474990465673
            imei = ''.join (random.sample ('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 32))
            wsgsig1 = wsgsig[random.randint (0, 25)]
            do_sign_url = f'https://bosp-api.xiaojukeji.com/gulfstream/hubble/open/signin/submit?wsgsig={wsgsig1}'
            data = r'{"xbiz":"240200","prod_key":"ut-discover","xpsid":"' + f"{xpsid}" + r'","dchn":"7mPlO68","xoid":"9921f9b4-e3f1-444f-8409-dec4e9af99e4","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f"{xpsid}" + r'","xpsid_from":"","xpsid_share":"","token":"' + f"{token}" + r'","lat":"23.0164990234375","lng":"113.81229031032986","city_id":21,"env":"{\"newTicket\":\"' + f"{token}" + r'\",\"latitude\":\"23.0164990234375\",\"longitude\":\"113.81229031032986\",\"cityId\":\"21\",\"userAgent\":\"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0\",\"appVersion\":\"6.2.4\",\"wifi\":\"1\",\"model\":\"iPhone 11\",\"ddfp\":\"'+ f'{imei}' + r'\",\"fromChannel\":\"1\",\"newAppid\":\"10000\",\"isHitButton\":false,\"isOpenWeb\":true,\"timeCost\":36}","openid":"","platform":"na","res_params":"{\"resource_names\":\"didipas_find_feed\",\"appversion\":\"6.2.4\",\"channel_id\":\"\",\"platform_type\":1}"}'
            do_sign_heards = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://page.udache.com/",
                "origin": "https://page.udache.com",
                "content-type": "application/json",
                "host":"bosp-api.xiaojukeji.com",
            }
            response = requests.post(url=do_sign_url,data=data,headers=do_sign_heards,verify=False)
            do_sign_ = response.json()
            print("do_sign_#积分签到")
            print(do_sign_)
            code = do_sign_['errno']   #本次签到获得的积分
            if code == 200100:
                res = f"今日刷刷赚已签到，无需重复签到"
            elif code == 0:
                #prize_status = do_sign_['data']['prize_status']   #5天签到周期内签到第几天
                content = do_sign_['data']['content']
                content = content[6:]
                res = f"今日签到成功，获得{content}"
            else:
                res = code
            return res
        except Exception as e:
            print(e)

    def main(self):
        msg_all = ""
        i = 1
        for check_item in self.check_items:
            token = check_item.get("token")
            xpsid = self.get_xpsid()
            msg = (
                f"账号 {i}\n------ 滴滴刷刷赚开始------\n"
                + self.do_sign(token=token,xpsid=xpsid,wsgsig=wsgsig)
                + "\n"
                + self.get_fulijin(token=token,wsgsig=wsgsig)
                + "\n------ 滴滴刷刷赚结束------"
            )
            i += 1
            msg_all += msg + "\n\n"     
        return msg_all

if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("DIDI", [])
    res = DIDIssz(check_items=_check_items).main()
    send("滴滴刷刷赚", res)        
