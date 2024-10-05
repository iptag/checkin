/*
1 8 * * * ck_haier.js
*/
const utils = require('./utils');
const fetch = require('node-fetch');
const Env = utils.Env;
const $ = new Env('海尔');
const getData = utils.getData;
const notify = $.isNode() ? require('./sendNotify') : '';
const AsVow = getData().HAIER;
var desp = '';
var info = '';

const headers = {
    'Host': 'zj.haier.net',
    'Content-Type': 'application/json',
    'User-Agent': 'Uplus/7.8.0 (iPhone; iOS 14.2.1; Scale/3.00)'
};

haier();

async function haier() {
    if (AsVow) {
        for (i in AsVow) {
            token = AsVow[i].token;
            info +=`=== 正对在第 ${i+1} 个账号签到===\n`;
            await sign();
            await getinfo();
        }
        console.log(info);
        notify.sendNotify('海尔', info);
    } else {
        info = '签到失败：请先获取Cookie⚠️';
        notify.sendNotify('海尔', info);
    }
}

function sign() {
    url = 'https://uws.haier.net/zjapi/zjBaseServer/daily/sign';
    headers['accountToken'] = token;
    body = {};
    return new Promise(resolve => {
      fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
      }).then(function(response) {
        return response.json()
      }).then(function(body) {
        if (body.retInfo.includes('成功')) {
            if (body.data.first) {
              info += `${body.data.signDate}首次签到成功\n获得 ${body.data.haibeiCount} 个海贝\n连续签到 ${body.data.signDay} 天\n总计签到 ${body.data.totalSignDay} 天\n`;
            } else {
              info += `${body.data.signDate}已签到过啦~\n获得 ${body.data.haibeiCount} 个海贝\n连续签到 ${body.data.signDay} 天\n总计签到 ${body.data.totalSignDay} 天\n`;
            }
        } else {
             info += "签到返回错误，请重新调试";
             console.log(info);
        }
  
      }).catch(function(e) {
          const error = '签到出现错误，请检查⚠️';
          console.log(error + '\n' + e);
      }).finally(() => {
          resolve()
      })
    });
}

function getinfo() {
    url = 'https://uws.haier.net/zjapi/zjBaseServer/signDetail/getUserPointsAndWallet';
    headers['accountToken'] = token;
    body = {};
    return new Promise(resolve => {
      fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
      })
      .then(function(response) {
        return response.json()
      }).then(function(body) {
        if (body.retInfo.includes('成功')) {
            info += `共计持有海贝 ${body.data.haiBeiTotal} 个\n`;
        }  else {
            info += "查询钱包信息返回错误，请重新调试";
        }
      }).catch(function(e) {
          info += "获取钱包信息失败" + e;
      }).finally(() => {
          resolve()
      })
    });
}

module.exports = haier;
