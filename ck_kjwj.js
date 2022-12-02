/*
31 7 * * * ck_kjwj.js
请提前在依赖管理-nodejs中安装qs
*/
const utils = require('./utils');
const Qs = require('qs');
const Env = utils.Env;
const getData = utils.getData;
const $ = new Env('科技玩家');
const notify = require('./sendNotify');
const AsVow = getData().KJWJ;
var info = '';
var desp = '';
var token = '';

const headers = {
    'Host': 'www.kejiwanjia.com',
    'Referer': 'https://www.kejiwanjia.com/mission/today',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
};

const data = {
    'username': '',
    'password': ''
};

kjwj();

async function kjwj() {
  if (AsVow) {
    for (i in AsVow) {
      username = AsVow[i].username;
      password = AsVow[i].password;
      data['username'] = username;
      data['password'] = password;
      if (username && password) {
        head = `=== 正对在 ${username} 的账号签到===\n`;
        info += `\n${head}`;
        await getauth();
        await pre_sign();
        await sign();
        desp += info;
        info = '';
      } 
    }
    info += desp;
    console.log(info);
    notify.sendNotify('科技玩家', info);
  } else {
    info = '签到失败：请先获取Cookie⚠️';
    console.log(info);
    notify.sendNotify('科技玩家', info);
  }
  $.done()
}

function getauth() {
  url = 'https://www.kejiwanjia.com/wp-json/jwt-auth/v1/token';
  headers['Referer'] = 'https://www.kejiwanjia.com/';
  headers['Content-Type'] = 'application/x-www-form-urlencoded';
  const request = {
      url: url,
      headers: headers,
      body: Qs.stringify(data)
  };
  return new Promise(resolve => {
    $.http.post(request)
      .then(async (resp) => {
        resdata = $.toObj(resp.body);
        info += `账号：${resdata.name}\n`;
        info += `ID：${resdata.id}\n`;
        info += `金币：${resdata.credit}\n`;
        info += `等级：${resdata.lv.lv.name}\n`;
        token = resdata.token;
      })
      .catch((err) => {
        const error = '账号信息获取失败⚠️';
        console.log(error + '\n' + err);
      })
      .finally(() => {
        resolve();
      });
  });
}

function pre_sign() {
  url = 'https://www.kejiwanjia.com/wp-json/b2/v1/getUserMission';
  headers['Content-Type'] = 'application/x-www-form-urlencoded';
  headers['Origin'] = 'https://www.kejiwanjia.com/';
  headers['Authorization'] = `Bearer ${token}`;
  suff = 'count=10&paged=1';
  const request = {
      url: url,
      headers: headers,
      body: suff
  };  
  return new Promise(resolve => {
    $.http.post(request)
      .then(async (resp) => {
        resdata = $.toObj(resp.body);
        if (resdata.mission.credit != "0") {
          info += `今天已签到：获得${resdata.mission.credit}金币\n\n`;
        }
      })
      .catch((err) => {
        const error = '🆕--签到前--状态获取失败⚠️';
        console.log(error + '\n' + err);
      })
      .finally(() => {
        resolve();
      });
  });
}

function sign() {
  url = 'https://www.kejiwanjia.com/wp-json/b2/v1/userMission';
  headers['Origin'] = 'https://www.kejiwanjia.com/';
  headers['Authorization'] = `Bearer ${token}`;
  const request = {
      url: url,
      headers: headers
  };
  return new Promise(resolve => {
    $.http.post(request)
      .then(async (resp) => {
        resdata = $.toObj(resp.body);
        if ((typeof resdata) != 'string') {
          info += `每日首次签到成功：获得${resdata.credit}金币\n\n`;
        }
      })
      .catch((err) => {
        const error = '🆕--签到--状态获取失败⚠️';
        console.log(error + '\n' + err);
      })
      .finally(() => {
        resolve();
      });
  });
}
module.exports = kjwj;
