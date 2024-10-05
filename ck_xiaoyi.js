/*
11 8 * * * ck_xiaoyi.js
*/
const utils = require('./utils');
const HmacSha1 = require('crypto-js/hmac-sha1');
const Base64 = require('crypto-js/enc-base64');
const fetch = require('node-fetch');
const Qs = require('qs');
const Env = utils.Env;
const getData = utils.getData;
const sleep = utils.sleep;
const $ = new Env('小蚁');
const notify = require('./sendNotify');
const AsVow = getData().XIAOYI;
var info = '';
var desp = '';

const headers = {
      'Host': 'gw.xiaoyi.com',
      'Origin': 'http://app.xiaoyi.com',
      'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 APP/com.360ants.yihome APPV/5.4.4 iosPassportSDK/2.2.2 iOS/14.2.1',
      'Referer': 'http://app.xiaoyi.com/cnApph5/integral/?rewardType=1&taskType=10&subTask=0'
};

xiaoyi();

async function xiaoyi() {
  if (AsVow) {
    for (i in AsVow) {
      ss = {};
      ss.token = AsVow[i].token;
      ss.token_secret = AsVow[i].token_secret;
      userid = AsVow[i].userid;
      if (ss.token) {
        info += `=== 正对在第 ${(+i)+1} 个账号签到===\n`;
        await sign();
        await query_tsknum().then (function(data){
          tsk = data;
        });
        await sleep(Math.floor((Math.random() * 10) + 32));
        if (tsk.video_num>0) {
            info += `获取视频任务数量成功\n还需完成 ${tsk.video_num} 次看视频任务\n`;
            for(var m=1;m<tsk.video_num+1;m++) {
                await videotask();
                await sleep(Math.floor((Math.random() * 10000) + 32000));
            }
        }
        if (tsk.live_num>0) {
            info += `还需完成 ${tsk.live_num} 次看直播任务\n`;
            for(var m=1;m<tsk.live_num+1;m++) {
                await receive_livetask();
                await sleep(Math.floor((Math.random() * 10000) + 32000));
                await livetask();
                await sleep(Math.floor((Math.random() * 10000) + 10000));
            }
        }
        if (tsk.alert_num>0) {
            info += `还需完成 ${tsk.alert_num} 次看报警视频任务\n`;
            for(var m=1;m<tsk.alert_num+1;m++) {
                await receive_alerttask();
                await sleep(Math.floor((Math.random() * 10000) + 10000));
                await alerttask();
                await sleep(Math.floor((Math.random() * 10000) + 10000));
            }
        }
        else {
            info += '今天的视频任务全部完成啦~~\n';
        }
        desp += info;
        info = '';
      }
    }
    info += desp;
    console.log(info);
    notify.sendNotify('小蚁', info);
  } else {
    info = '签到失败：请先获取Cookie⚠️';
    notify.sendNotify('小蚁', info);
  }
  $.done()
}

function sign() {
  url = 'https://gw.xiaoyi.com/urs/v8/task/do';
  headers['Content-Type'] = 'application/x-www-form-urlencoded';
  nonce = Math.random().toString().slice(-6);
  time = new Date().getTime();
  hh = {"appPlatform":"yihome","nonce":nonce,"region":"CN","seq":1,"subTask":0,"taskType":10,"timestamp":time,"userid":userid};
  cc =Qs.stringify(hh);
  hh.hmac = decodeURIComponent(t(cc,ss).replace('&'+cc,'').slice(5));
  return new Promise(resolve => {
    fetch(url, {
        method: 'POST',
        headers: headers,
        body: Qs.stringify(hh),
    }).then(function(response) {
        return response.json()
    }).then(function(body) {
        if (body.code == "20000" && body.msg == "success") {
            info += `完成签到任务：\n获得${body.data.reward}分\n`;
        }
    }).catch(function(e) {
        const error = '签到任务出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    }).finally(() => {
        resolve()
    })
  });
}

function query_tsknum() {
  time = new Date().getTime();
  hh = 'appPlatform=yihome&region=CN&seq=1&timestamp='+time+'&userid='+userid;
  suffix = t(hh,ss);
  url = `https://gw.xiaoyi.com/urs/v8/task/list?${suffix}`;
  return new Promise(resolve => {
    fetch(url, {
        method: 'GET',
        headers: headers
    }).then(function(response) {
        return response.json()
    }).then(function(body) {
        if (body.code == "20000" && body.msg == "success") {
            tsk_num = {};
            tsk_num.video_num = body.data[0].total - body.data[0].currentTotal;
            tsk_num.live_num = body.data[1].total - body.data[1].currentTotal;
            tsk_num.alert_num = body.data[2].total - body.data[2].currentTotal;
            resolve(tsk_num)
        }
    }).catch(function(e) {
        const error = '获取视频任务数量出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    })
  });
}

function videotask() {
  url = 'https://gw.xiaoyi.com/urs/v8/task/do';
  headers['Content-Type'] = 'application/x-www-form-urlencoded';
  nonce = Math.random().toString().slice(-6);
  time = new Date().getTime();
  hh = {"appPlatform":"yihome","nonce":nonce,"region":"CN","seq":1,"subTask":0,"taskType":20,"timestamp":time,"userid":userid};
  cc =Qs.stringify(hh);
  hh.hmac = decodeURIComponent(t(cc,ss).replace('&'+cc,'').slice(5));
  return new Promise(resolve => {
    fetch(url, {
        method: 'POST',
        headers: headers,
        body: Qs.stringify(hh),
    }).then(function(response) {
        return response.json()
    }).then(function(body) {
        if (body.code == "20000" && body.msg == "success") {
            info += `完成看视频任务：\n获得${body.data.reward}分\n`;
        }
    }).catch(function(e) {
        const error = '看视频任务出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    }).finally(() => {
        resolve()
    })
  });
}

function receive_livetask() {
  url = 'https://gw.xiaoyi.com/urs/v8/task/receive';
  headers['Content-Type'] = 'application/x-www-form-urlencoded';
  nonce = Math.random().toString().slice(-6);
  time = new Date().getTime();
  hh = {"appPlatform":"yihome","nonce":nonce,"region":"CN","seq":1,"subTask":0,"taskType":80,"timestamp":time,"userid":userid};
  cc =Qs.stringify(hh);
  hh.hmac = decodeURIComponent(t(cc,ss).replace('&'+cc,'').slice(5));
  return new Promise(resolve => {
    fetch(url, {
        method: 'POST',
        headers: headers,
        body: Qs.stringify(hh),
    }).then(function(response) {
        return response.json()
    }).then(function(body) {
        if (body.code == "20000" && body.msg == "success") {
            info += '接受一次看直播任务：\n';
        }
    }).catch(function(e) {
        const error = '接受看直播任务出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    }).finally(() => {
        resolve()
    })
  });
}

function livetask() {
  url = 'https://gw.xiaoyi.com/urs/v8/task/do';
  headers['Content-Type'] = 'application/x-www-form-urlencoded';
  nonce = Math.random().toString().slice(-6);
  time = new Date().getTime();
  hh = {"appPlatform":"yihome","nonce":nonce,"region":"CN","seq":1,"subTask":0,"taskType":80,"timestamp":time,"userid":userid};
  cc =Qs.stringify(hh);
  hh.hmac = decodeURIComponent(t(cc,ss).replace('&'+cc,'').slice(5));
  return new Promise(resolve => {
    fetch(url, {
        method: 'POST',
        headers: headers,
        body: Qs.stringify(hh),
    }).then(function(response) {
        return response.json()
    }).then(function(body) {
        if (body.code == "20000" && body.msg == "success") {
            info += `完成一次看直播任务：\n获得${body.data.reward}分\n`;
        }
    }).catch(function(e) {
        const error = '看直播任务出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    }).finally(() => {
        resolve()
    })
  });
}

function receive_alerttask() {
  url = 'https://gw.xiaoyi.com/urs/v8/task/receive';
  headers['Content-Type'] = 'application/x-www-form-urlencoded';
  nonce = Math.random().toString().slice(-6);
  time = new Date().getTime();
  hh = {"appPlatform":"yihome","nonce":nonce,"region":"CN","seq":1,"subTask":0,"taskType":70,"timestamp":time,"userid":userid};
  cc =Qs.stringify(hh);
  hh.hmac = decodeURIComponent(t(cc,ss).replace('&'+cc,'').slice(5));
  return new Promise(resolve => {
    fetch(url, {
        method: 'POST',
        headers: headers,
        body: Qs.stringify(hh),
    }).then(function(response) {
        return response.json()
    }).then(function(body) {
        if (body.code == "20000" && body.msg == "success") {
            info += '接受一次看报警视频任务：\n';
        }
    }).catch(function(e) {
        const error = '接受看报警视频任务出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    }).finally(() => {
        resolve()
    })
  });
}

function alerttask() {
  url = 'https://gw.xiaoyi.com/urs/v8/task/do';
  headers['Content-Type'] = 'application/x-www-form-urlencoded';
  nonce = Math.random().toString().slice(-6);
  time = new Date().getTime();
  hh = {"appPlatform":"yihome","nonce":nonce,"region":"CN","seq":1,"subTask":0,"taskType":70,"timestamp":time,"userid":userid};
  cc =Qs.stringify(hh);
  hh.hmac = decodeURIComponent(t(cc,ss).replace('&'+cc,'').slice(5));
  return new Promise(resolve => {
    fetch(url, {
        method: 'POST',
        headers: headers,
        body: Qs.stringify(hh),
    }).then(function(response) {
        return response.json()
    }).then(function(body) {
        if (body.code == "20000" && body.msg == "success") {
            info += `完成一次看报警视频任务：\n获得${body.data.reward}分\n`;
        }
    }).catch(function(e) {
        const error = '看报警视频任务出现错误，请检查⚠️';
        console.log(error + '\n' + e);
    }).finally(() => {
        resolve()
    })
  });
}

function t(a, b) {
    m = b.token,
    n = b.token_secret,
    o = Base64.stringify((HmacSha1(a,m+'&'+n)));
    c = 'hmac=' + encodeURIComponent(o) + '&' + a;
   	return c
}

module.exports = xiaoyi;
