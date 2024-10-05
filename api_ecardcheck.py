# -*- coding: utf-8 -*-
"""
:author @limoruirui
cron: 18 0-23/6 * * *
new Env('爱企查e卡监控');
"""

from random import choice

import requests

from sendNotify import send
from utils import get_data


class EcardCheck:
    @staticmethod
    def randomstr(numb):
        s = ""
        for _ in range(numb):
            s = s + choice("abcdefghijklmnopqrstuvwxyz0123456789")
        return s

    def main(self):
        url = "https://aiqicha.baidu.com/usercenter/getBenefitStatusAjax"
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1",
            "Referer": f"https://aiqicha.baidu.com/m/usercenter/mall?jf_h5_center1?VNK={self.randomstr(8)}",
        }
        if requests.get(url, headers=headers).json()["data"]["AQ03008"] == "true":
            send("爱企查e卡监控", "爱企查京东e卡有货，请进行兑换")


if __name__ == "__main__":
    data = get_data()
    ecardcheck = data.get("ECARDCHECK")
    if ecardcheck:
        EcardCheck().main()
