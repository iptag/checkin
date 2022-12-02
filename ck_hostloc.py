# -*- coding: utf-8 -*-
"""
cron: 48 0-23/12 * * *
new Env('HOSTLOC');
"""

import random
import re
import textwrap
import time

import requests
from pyaes import AESModeOfOperationCBC
from requests import Session as req_Session

from sendNotify import send
from utils import get_data

desp = ""  # 空值


def log(info: str):
    global desp
    desp = desp + info + "\n"


class HOSTLOC:
    def __init__(self, check_items):
        self.check_items = check_items
        self.home_page = "https://hostloc.com/forum.php"

    # 随机生成用户空间链接
    def randomly_gen_uspace_url(self) -> list:
        url_list = []
        # 访问小黑屋用户空间不会获得积分、生成的随机数可能会重复，这里多生成两个链接用作冗余
        for _ in range(12):
            uid = random.randint(10000, 50000)
            url = "https://hostloc.com/space-uid-{}.html".format(str(uid))
            url_list.append(url)
        return url_list

    # 使用Python实现防CC验证页面中JS写的的toNumbers函数
    def toNumbers(self, secret: str) -> list:
        text = []
        for value in textwrap.wrap(secret, 2):
            text.append(int(value, 16))
        return text

    # 不带Cookies访问论坛首页，检查是否开启了防CC机制，将开启状态、AES计算所需的参数全部放在一个字典中返回
    def check_anti_cc(self) -> dict:
        result_dict = {}
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        home_page = self.home_page
        res = requests.get(home_page, headers=headers)
        aes_keys = re.findall(r'toNumbers\("(.*?)"\)', res.text)
        cookie_name = re.findall('cookie="(.*?)="', res.text)

        if len(aes_keys) != 0:  # 开启了防CC机制
            log("检测到防 CC 机制开启！")
            if (
                len(aes_keys) != 3 or len(cookie_name) != 1
            ):  # 正则表达式匹配到了参数，但是参数个数不对（不正常的情况）
                result_dict["ok"] = 0
            else:  # 匹配正常时将参数存到result_dict中
                result_dict["ok"] = 1
                result_dict["cookie_name"] = cookie_name[0]
                result_dict["a"] = aes_keys[0]
                result_dict["b"] = aes_keys[1]
                result_dict["c"] = aes_keys[2]

        return result_dict

    # 在开启了防CC机制时使用获取到的数据进行AES解密计算生成一条Cookie（未开启防CC机制时返回空Cookies）
    def gen_anti_cc_cookies(self) -> dict:
        cookies = {}
        anti_cc_status = self.check_anti_cc()

        if anti_cc_status:  # 不为空，代表开启了防CC机制
            if anti_cc_status["ok"] == 0:
                log("防 CC 验证过程所需参数不符合要求，页面可能存在错误！")
            else:  # 使用获取到的三个值进行AES Cipher-Block Chaining解密计算以生成特定的Cookie值用于通过防CC验证
                log("自动模拟计尝试通过防 CC 验证")
                a = bytes(self.toNumbers(anti_cc_status["a"]))
                b = bytes(self.toNumbers(anti_cc_status["b"]))
                c = bytes(self.toNumbers(anti_cc_status["c"]))
                cbc_mode = AESModeOfOperationCBC(a, b)
                result = cbc_mode.decrypt(c)

                name = anti_cc_status["cookie_name"]
                cookies[name] = result.hex()

        return cookies

    # 登录帐户
    def login(self, username: str, password: str) -> req_Session:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "origin": "https://hostloc.com",
            "referer": self.home_page,
        }
        login_url = "https://hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
        login_data = {
            "fastloginfield": "username",
            "username": username,
            "password": password,
            "quickforward": "yes",
            "handlekey": "ls",
        }

        s = req_Session()
        s.headers.update(headers)
        s.cookies.update(self.gen_anti_cc_cookies())
        res = s.post(url=login_url, data=login_data)
        res.raise_for_status()
        return s

    # 通过抓取用户设置页面的标题检查是否登录成功
    def check_login_status(self, s: req_Session, number_c: int) -> bool:
        test_url = "https://hostloc.com/home.php?mod=spacecp"
        res = s.get(test_url)
        res.raise_for_status()
        res.encoding = "utf-8"
        test_title = re.findall(r"<title>(.*?)<\/title>", res.text)

        if len(test_title) != 0:  # 确保正则匹配到了内容，防止出现数组索引越界的情况
            if test_title[0] != "个人资料 -  全球主机交流论坛 -  Powered by Discuz!":
                log("第 " + str(number_c) + " 个帐户登录失败！")
                return False
            else:
                log("第 " + str(number_c) + " 个帐户登录成功！")
                return True
        else:
            log("无法在用户设置页面找到标题，该页面存在错误或被防 CC 机制拦截！")
            return False

    # 抓取并打印输出帐户当前积分
    def log_current_points(self, s: req_Session):
        test_url = self.home_page
        res = s.get(test_url)
        res.raise_for_status()
        res.encoding = "utf-8"
        points = re.findall(r"积分: (\d+)", res.text)

        if len(points) != 0:  # 确保正则匹配到了内容，防止出现数组索引越界的情况
            log("帐户当前积分：" + points[0])
        else:
            log("无法获取帐户积分，可能页面存在错误或者未登录！")
        time.sleep(12)

    # 依次访问随机生成的用户空间链接获取积分
    def get_points(self, s: req_Session, number_c: int):
        if self.check_login_status(s, number_c):
            self.log_current_points(s)  # 打印帐户当前积分
            url_list = self.randomly_gen_uspace_url()
            # 依次访问用户空间链接获取积分，出现错误时不中断程序继续尝试访问下一个链接
            for i in range(len(url_list)):
                url = url_list[i]
                try:
                    res = s.get(url)
                    res.raise_for_status()
                    log("第 " + str(i + 1) + " 个用户空间链接访问成功")
                    time.sleep(12)  # 每访问一个链接后休眠5秒，以避免触发论坛的防CC机制
                except Exception as e:
                    log("链接访问异常：" + str(e))
            self.log_current_points(s)  # 再次打印帐户当前积分
        else:
            log("请检查你的帐户是否正确！")

    # 打印输出当前ip地址
    def log_my_ip(self):
        api_url = "https://api.ipify.org/"
        try:
            res = requests.get(url=api_url)
            res.raise_for_status()
            res.encoding = "utf-8"
            log("当前使用 ip 地址：" + res.text)
        except Exception as e:
            log("获取当前 ip 地址失败：" + str(e))

    def main(self):
        i = 0
        for check_item in self.check_items:
            username = check_item.get("username")
            password = check_item.get("password")
            self.log_my_ip()
            log("共检测到 " + str(len(self.check_items)) + " 个帐户，开始获取积分")
            log("*" * 12)

            try:
                s = self.login(username, password)
                self.get_points(s, i + 1)
                log("*" * 12)
            except Exception as e:
                log("程序执行异常：" + str(e))
                log("*" * 12)

            i += 1

        log("程序执行完毕，获取积分过程结束")
        return desp


if __name__ == "__main__":
    data = get_data()
    _check_items = data.get("HOSTLOC", [])
    res = HOSTLOC(check_items=_check_items).main()
    send("HOSTLOC", res)
