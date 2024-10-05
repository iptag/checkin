/*
31 7 * * * ck_52pj.js
请提前在依赖管理-nodejs中安装request,cheerio,iconv-lite
====================$$$$$$$$$$$$$$======================
感谢原作者Mrzqd(https://github.com/Mrzqd/52pojie_sign)
====================$$$$$$$$$$$$$$======================
*/
const utils = require('./utils');
const request = require('request');
const cheerio = require('cheerio');
var iconv = require('iconv-lite');
const Env = utils.Env;
const getData = utils.getData;
const $ = new Env('52pj');
const notify = require('./sendNotify');
const AsVow = getData().POJIE;
var info = '';
var desp = '';

const headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
};

pojie();

async function pojie() {
  if (AsVow) {
    for (i in AsVow) {
      cookie = AsVow[i].cookie;
      cookie = decodeURIComponent(cookie.replace(/\s*/g,""));
      if (cookie) {
        head = `=== 正对在第 ${i+1} 的账号签到===\n`;
        info += `\n${head}`;
        cookieList = cookie.split(";");
        let filteredCookies = '';
        for (const cookie of cookieList) {
            key = cookie.split("=")[0];
            if (key == "htVC_2132_saltkey") {
                filteredCookies += cookie + "; ";
            }
            if (key == "htVC_2132_auth") {
                filteredCookies += cookie + ";";
            }
        }
        tmp1 = await get_cookie(filteredCookies)
        tmp2 = await get_cookie2(tmp1)
        jx_data = await get_sign(tmp2)
        if (jx_data.includes("您需要先登录才能继续本操作")) {
            console.log(`Cookie 失效`);
            info += `Cookie 失效`;
        } else if (jx_data.includes("恭喜")) {
            console.log(`签到成功`);
            info += `签到成功`;
        } else if (jx_data.includes("不是进行中的任务")) {
            console.log(`今日已签到`);
            info += `今日已签到`;
        } else {
            console.log(`签到失败`);
            info += `签到失败`;
        }
        desp += info;
        info = '';
      }
    }
    info += desp;
    console.log(info);
    notify.sendNotify('52pj', info);
  } else {
    info = '签到失败：请先获取Cookie⚠️';
    console.log(info);
    notify.sendNotify('52pj', info);
  }
  $.done()
}

function get_cookie(cookie) {
    return new Promise((resolve) => {
        headers["Cookie"] = cookie
        const option = {
            url: "https://www.52pojie.cn/CSPDREL2hvbWUucGhwP21vZD10YXNrJmRvPWRyYXcmaWQ9Mg==?wzwscspd=MC4wLjAuMA==",
            method: "get",
            headers: headers,
            followRedirect: false,
        };
        request(option, (error, response, body) => {
            cookie = cookie + response.headers['set-cookie']
            resolve(cookie)
        });
    });
};

function get_cookie2(cookie) {
    return new Promise((resolve) => {
        headers["Cookie"] = cookie
        const option = {
            url: "https://www.52pojie.cn/home.php?mod=task&do=apply&id=2&referer=%2F",
            method: "get",
            headers: headers,
            followRedirect: false,
        };
        request(option, (error, response, body) => {
            cookie = cookie + response.headers['set-cookie']
            resolve(cookie)
        });
    });
};

function get_sign(cookie) {
    return new Promise((resolve) => {
        headers["Cookie"] = cookie
        const option = {
            url: "https://www.52pojie.cn/home.php?mod=task&do=draw&id=2",
            method: "get",
            headers: headers,
            encoding: null,
        };
        request(option, (error, response, body) => {
            if (!error && response.statusCode === 200) {
                var html = iconv.decode(body, 'gbk')
                var $ = cheerio.load(html);
                jx_data = $("#messagetext p").text();
                console.log(jx_data)
                resolve(jx_data)
            }
        });
    });
};
