/*
49 7 * * * ck_mcloud.js
*/
const utils = require('./utils');
const sleep = utils.sleep;
const getData = utils.getData;
const Env = utils.Env;
const $ = new Env('和彩云')
const Qs = require('qs');
const fetch = require('node-fetch');
const JSEncrypt = require('./jsencrypt-2.3-mod.js');
const notify = require('./sendNotify');
const AsVow = getData().MCLOUD;
var info = '';
var desp = '';

headers = {
    "Host": "orches.yun.139.com",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MCloudApp/9.2.1"
}
const pubbkey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEdVKnXpmib/xkN/SYguTHTTd4f1N3K8L/QmcWLKtyrdoFwENaaAZC1v471+ge9y3cAgsSZJNbW9LmPD/7W0KZ3K1HXLS5PBMAGFW/CybJ8nE8+xCH6ypOhFMq504q9mDujhtOI54XvDC1BZnDvA5J1OpxeJuOtRAQar/7BgU1nwIDAQAB";

mcloud();

async function mcloud() {
  if (AsVow) {
    for (i in AsVow) {
      ss = {};
      ss.Authorization = AsVow[i].Authorization;
      ss.phoneNumber = AsVow[i].phoneNumber;
      if (ss.Authorization && ss.phoneNumber) {
        info += `\n\n=== 正对 ${ss.phoneNumber} 的账号签到===\n`;
        headers['Authorization'] = ss.Authorization
        await getSTuid(ss.phoneNumber).then (function(data){stuu = data});
        delete headers['Authorization']
        delete headers['Content-Type']
        headers['Host'] = "caiyun.feixin.10086.cn:7071"
        headers['Referer'] = `https://caiyun.feixin.10086.cn:7071/portal/newsignin/index.html?sourceid=1002&enableShare=1&ssoToken=${stuu}`
        await getCookie(stuu).then (function(data){cookie = data});
        headers['jwtToken'] = cookie.jwtoken
        headers['Cookie'] = cookie.cookie
        await pageinfo();
        await tasklist().then (function(data){task_list = data});
        for (i in task_list.day_task){
             if (task_list.day_task[i].description.includes('+') && task_list.day_task[i].state.includes('WAIT')){
                 await dotask(task_list.day_task[i].id,task_list.day_task[i].name)
             }
        }
        await receivepts();
        desp += info;
        info = '';
      } else {
        info += '请检查Cookie和Referer是否正确填写⚠️';
        console.log(`请检查Cookie和Referer是否正确填写⚠️`);
      }
    }
    info += desp;
    console.log(info);
    notify.sendNotify('和彩云', info);
  } else {
    info = '签到失败：请先获取Cookie⚠️';
    notify.sendNotify('和彩云', info);
  }
  $.done()
}

function getSTuid(t) {
    url = 'https://orches.yun.139.com/orchestration/auth/token/v1.0/querySpecToken';
    body = {account:t,toSourceId:"001005"}
    return new Promise(resolve => {
       fetch(url, {
          method: 'POST',
          headers: headers,
          body: JSON.stringify(body)
        }).then(function(response) {
          return response.json()
        }).then(function(body){
          if (body.success) {
            resolve(body.data.token)
          }
        }).catch(function(e) {
          const error = '获取stuid出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        })
    });
}

function getCookie(t) {
    url = `https://caiyun.feixin.10086.cn:7071/portal/auth/tyrzLogin.action?ssoToken=${t}`;
    return new Promise(resolve => {
       fetch(url, {
          method: 'GET',
          headers: headers,
        }).then(function(response) {
          cookie = response.headers.get('set-cookie')
          pat = /SESSION=([\w]+);/g
          session = pat.exec(cookie)
          pat1 = /jwtToken=(.*?);/g
          jwtoken = pat1.exec(cookie)
          pat2 = /bc_mo=([\w=]+);/g
          bc_mo1 = pat2.exec(cookie)
          pat3 = /bc_mo=\"([\w=]+)\";/g
          bc_mo2 = pat3.exec(cookie)
          pat4 = /bc_to=\"([\w]+)\";/g
          bc_to = pat4.exec(cookie)
          cookies = {}
          cookies.jwtoken = jwtoken[1]
          cookies.cookie = session[0] + bc_to[0] + bc_mo1[0] + bc_mo2[0] + 'bc_ps="";' + jwtoken[0]
          resolve(cookies)
        }).catch(function(e) {
          const error = '获取cookie出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        })
    });
}

function pageinfo() {
  url = 'https://caiyun.feixin.10086.cn:7071/market/signin/page/info';
  headers['token'] = getoken();
  return new Promise(resolve => {
    fetch(url, {
      method: 'GET',
      headers: headers,
    }).then(function(response) {
      return response.json()
    }).then(function(body) {
      if (body.msg.includes('success')) {
          if (body.result.todaySignIn) {
              info += `今日已签到，积分总计：${body.result.total}💰\n`;
              console.log(body)
          } else {
              info += `首次签到成功，积分总计：${body.result.total}💰，本次签到积分到：${body.result.signInPoints}分，本月已签到${body.result.monthDays}天\n`;
          }
      } else {
          info += "获取信息页面返回错误，请重新调试";
          console.log(info);
      }
    }).catch(function(e) {
        const error = '获取信息页面出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    }).finally(() => {
        resolve()
    })
  });
}

function tasklist() {
  url = 'https://caiyun.feixin.10086.cn:7071/market/signin/task/taskList?marketname=sign_in_3';
  headers['token'] = getoken();
  return new Promise(resolve => {
    fetch(url, {
      method: 'GET',
      headers: headers,
    }).then(function(response) {
      return response.json()
    }).then(function(body) {
      if (body.msg.includes('success')) {
          task_list = {}
          task_list.day_task = body.result.day
		  task_list.month_task = body.result.month
		  resolve(task_list)
      } else {
          info += "获取任务页面返回错误";
          console.log(info);
      }
    }).catch(function(e) {
        const error = '获取任务页面出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    })
  });
}

function dotask(id,title) {
  url = `https://caiyun.feixin.10086.cn:7071/market/signin/task/click?key=task&id=${id}`;
  headers['token'] = getoken();
  return new Promise(resolve => {
    fetch(url, {
      method: 'GET',
      headers: headers,
    }).then(function(response) {
      return response.json()
    }).then(function(body) {
      if (body.msg.includes('success')) {
          info += `已完成 ${title} +2云朵\n`;
      }
    }).catch(function(e) {
        const error = '做任务页面出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    }).finally(() => {
        resolve()
    })
  });
}

function receivepts() {
  url = 'https://caiyun.feixin.10086.cn:7071/market/signin/page/receive';
  headers['token'] = getoken();
  return new Promise(resolve => {
    fetch(url, {
      method: 'GET',
      headers: headers,
    }).then(function(response) {
      return response.json()
    }).then(function(body) {
      if (body.msg.includes('success')) {
          info += `收取${body.result.receive}积分成功，积分总计：${body.result.total}💰\n`;
      } else {
          info += "收取页面返回错误，请重新调试";
          console.log(info);
      }
    }).catch(function(e) {
        const error = '收取页面出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    }).finally(() => {
        resolve()
    })
  });
}

function getoken(){
  var headtoken = endata(parseInt(ss.phoneNumber) + '-' + new Date().getTime());
  return headtoken
}

function endata(t){
  var encrypt = new JSEncrypt();
  encrypt.setPublicKey(pubbkey);
  encrypted = encrypt.encrypt(JSON.stringify(t));
  return encrypted
}

/* 无用函数，暂存
function enlogin() {
  url = 'https://caiyun.feixin.10086.cn:7071/portal/auth/encryptDataLogin.action';
  data = {account:ss.account,encryptTime:uxtime};
  formdata = {data:endata(data),token:ss.token,op:"tokenLogin"};
  return new Promise(resolve => {
    fetch(url, {
      method: 'POST',
      headers: headers,
      body: Qs.stringify(formdata)
    }).then(function(response) {
      return response.json()
    }).then(function(body) {
      if (body.code == 10000) {
          info += `加密登录成功\n`;
          console.log(body);
      } else {
          info += `加密登录返回错误调⚠️，信息如下：\n${JSON.stringify(body)}`;
          console.log(info);
      }
    }).catch(function(e) {
        const error = '加密登录出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    }).finally(() => {
        resolve()
    })
  });
}
*/
module.exports = mcloud;
