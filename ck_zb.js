/*
28 8 * * * ck_zb.js
*/
const utils = require('./utils');
const fetch = require('node-fetch');
const Env = utils.Env;
const $ = new Env('新赚吧');
const getData = utils.getData;
const sleep = utils.sleep;
const notify = require('./sendNotify');
const AsVow = getData().ZHUANBA;
require("https").globalAgent.options.rejectUnauthorized = false
var desp = '';
var info = '';
headers = {
    "Host": "v1.xianbao.net",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
}

zhuanba();

async function zhuanba() {
    if (AsVow) {
        for (i in AsVow) {
            headers['Cookie'] = AsVow[i].cookie
            info +=`=== 正对在第 ${i+1} 个账号签到===\n`
            await get_Sign();
            await get_Signinfo();
            desp += info;
            info = '';
        }
        info = desp;
        console.log(info);
        notify.sendNotify('新赚吧', info);
    } else {
        info = '签到失败：请先获取Cookie⚠️';
        notify.sendNotify('新赚吧', info);
    }
    $.done()
}

//签到
function get_Sign() {
    url = "https://v1.xianbao.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=0&inajax=0"
    return new Promise(resolve => {
       fetch(url, {method: 'GET',headers: headers}).then(response => {
          return response.text()
        }).then(body => {
        //   console.log(body)
          regexp = /([\u4e00-\u9fa5].*?)(?=<a href="plu)/
          tmp = body.match(regexp)
          if (tmp[0].includes('恭喜')){
              info += `${tmp[0]}\n`
          } else {
            info += `今日已签过到！\n`
          }
        }).catch(e => {
          const error = '签到出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        }).finally(() => {
          resolve()
        })
    });
}

//获取签到信息
function get_Signinfo() {
    url = "https://v1.xianbao.net/plugin.php?id=dsu_paulsign:sign"
    return new Promise(resolve => {
       fetch(url, {method: 'GET',headers: headers}).then(response => {
          return response.text()
        }).then(body => {
          tmp= []
          regexp = [/(?<=签到:<b>)(.*?)(?=<)/,/(?<=green><b>)(.*?)(?=<)/,/(?<=FF0000><b>)(.*?)(?=<)/]
          regexp.forEach((s,i)=>{tmp[i]=body.match(s)[0]})
          console.log(tmp)
          info += `本月已累计签到:${tmp[0]}天\n目前的等级:${tmp[1]}\n还需签到${tmp[2]}天才能升到下一级\n`;
        }).catch(e => {
          const error = '获取Signinfo出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        }).finally(() => {
          resolve()
        })
    });
}
module.exports = zhuanba;
