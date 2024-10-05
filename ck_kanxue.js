/*
5 8 * * * ck_kanxue.js
*/
const utils = require('./utils');
const fetch = require('node-fetch');
const qs = require('qs');
const Env = utils.Env;
const $ = new Env('看雪论坛');
const getData = utils.getData;
const sleep = utils.sleep;
const notify = require('./sendNotify');
const AsVow = getData().KANXUE;
var desp = '';
var info = '';
headers = {
    "Host": "bbs.pediy.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
}

kanxue();

async function kanxue() {
    if (AsVow) {
        for (i in AsVow) {
            headers['Cookie'] = AsVow[i].cookie
            info +=`=== 正对在第 ${i+1} 个账号签到===\n`
            sign_str = await get_Signinfo().then(data => data);
            if (sign_str.includes("已签到")){
                info += "今日已签过到！\n"
            } else {
                token = await get_token().then(data => data);
                headers['Content-Type'] = "application/x-www-form-urlencoded; charset=UTF-8"
                await sign(token);
            }
            desp += info;
            info = '';
        }
        info = desp;
        console.log(info);
        notify.sendNotify('看雪论坛', info);
    } else {
        info = '签到失败：请先获取Cookie⚠️';
        notify.sendNotify('看雪论坛', info);
    }
    $.done()
}

//获取csrf-token
function get_token() {
    url = "https://bbs.pediy.com/"
    return new Promise(resolve => {
       fetch(url, {method: 'GET',headers: headers,}).then(response => {
          return response.text()
        }).then(body => {
          regexp = /(?<=content=")([\w]{30,34})(?=")/
          tmp = body.match(regexp)
          console.log(tmp[0])
          resolve(tmp[0])
        }).catch(e => {
          const error = '获取token出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        })
    });
}

//查看是否已签过到
function get_Signinfo() {
    url = "https://bbs.pediy.com/user-is_signin.htm"
    return new Promise(resolve => {
       fetch(url, {method: 'GET',headers: headers,}).then(response => {
          return response.json()
        }).then(body => {
          console.log(body)
          resolve(body.message)
        }).catch(e => {
          const error = '获取Signinfo出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        })
    });
}

//签到
function sign(t) {
    url = "https://bbs.pediy.com/user-signin.htm"
    body = `{"csrf_token":${t}}`
    return new Promise(resolve => {
       fetch(url, {method: 'POST',headers: headers,body: qs.stringify(body)}).then(response => {
          return response.json()
        }).then(body => {
          if (body.code.includes("0")){
              info += `签到成功！获得积分 ${body.message}\n`;
          } else {
              console.log(body)
          }
        }).catch(e => {
          const error = '签到出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        }).finally(() => {
          resolve()
        })
    });
}
module.exports = kanxue;
