/*
17 7 * * * ck_wps.js
*/
const utils = require('./utils');
const fetch = require('node-fetch');
const Env = utils.Env;
const $ = new Env('wps');
const getData = utils.getData;
const sleep = utils.sleep;
const notify = require('./sendNotify');
const AsVow = getData().WPS;
var desp = '';
var info = '';

header ={
    'Host': 'vip.wps.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52',
}

wps();

async function wps() {
    if (AsVow) {
        for (i in AsVow) {
            sid = AsVow[i].sid
            header['cookie'] = "wps_sid=" + sid
            usrinfo = await get_Userinfo().then(data => data);
            info +=`=== 正对在第 ${usrinfo.name} 的账号签到===\n`
            if (usrinfo.flag) {
                info += `今日普通签到已完成！！！\n`;
            } else {
                for (var i=0;i<15;i++){
                    await get_Yzm();
                    result = await get_Norsign().then(data => data);
                    if (result == "ok") break;
                    await sleep(Math.floor((Math.random() * 3000) + 5000));
                }
                await get_Norstatus();
            }
            /*
            for (var i=0;i<15;i++){
                await get_Cpatcha(usrinfo.id);
                result = await get_Vipsign().then(data => data);
                await sleep(Math.floor((Math.random() * 3000) + 5000));
                if (result == "ok") {
                     break;
                }
            }
            await get_Vipstatus()
            */
            desp += info
            info = ''
        }
        info = desp
        console.log(info);
        notify.sendNotify('WPS', info);
    } else {
        info = '签到失败：请先获取Cookie⚠️';
        notify.sendNotify('WPS', info);
    }
    $.done()
}

//获取用户信息
function get_Userinfo() {
    url = "https://vip.wps.cn/sign/mobile/v3/get_data"
    user = {}
    return new Promise(resolve => {
       fetch(url, {method: 'GET',headers: header}).then(response => {
          return response.json()
        }).then(body => {
          console.log(body)
          user.id = body.data.userinfo.userid
          user.name = body.data.userinfo.nickname
          user.flag = body.data.is_sign
          resolve(user)
        }).catch(e => {
          const error = '获取userinfo出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        })
    });
}

//普通签到的验证码
function get_Yzm() {
    url = `https://vip.wps.cn/checkcode/signin/captcha.png?platform=8&encode=0&img_witdh=275.164&img_height=69.184`
    return new Promise(resolve => {
       fetch(url, {method: 'GET', headers: header}).then(response => {
          return response.text()
        }).then(body => {
          console.log('验证码已下载')
        }).catch(e => {
          const error = '获取普通签到的验证码出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        }).finally(() => {
          resolve()
        })
    });
}

//普通签到
function get_Norsign() {
    url = `https://vip.wps.cn/sign/v2`
    body = {"platform": "8","captcha_pos": "137, 36","img_witdh": "275.164","img_height": "69.184"}
    return new Promise(resolve => {
       fetch(url, {method: 'POST', headers: header, body: JSON.stringify(body)}).then(response => {
          return response.json()
        }).then(body => {
          console.log(body)
          resolve(body.result)
        }).catch(e => {
          const error = '普通签到出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        })
    });
}

//获取普通签到后信息
function get_Norstatus() {
    url = `https://vip.wps.cn/sign/mobile/v3/get_data`
    return new Promise(resolve => {
       fetch(url, {method: 'GET',headers: header}).then(response => {
          return response.json()
        }).then(body => {
          if (body.data.is_sign) {
               info += `今日顺利普通签到~\n`;
          } else {
               info += `今日普通签到失败！\n`;
          }
        }).catch(e => {
          const error = '获取普通签到信息出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        }).finally(() => {
          resolve()
        })
    });
}


//获取captcha图片
function get_Cpatcha(t) {
    url = `https://vipapi.wps.cn/vas_risk_system/v1/captcha/image?service_id=zt_clock_in&request_id=zt_clock_in_${t}`
    header['Host'] = 'vipapi.wps.cn'
    header['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.30(0x18001e2e) NetType/WIFI Language/zh_CN'
    delete header['Cookie']
    return new Promise(resolve => {
       fetch(url, {method: 'GET',headers: header}).then(response => {
          return response.text()
        }).then(body => {
          console.log('获取到png图片')
        }).catch(e => {
          const error = '获取cpatcha图片出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        }).finally(() => {
          resolve()
        })
    });
}

//会员打卡
function get_Vipsign() {
    time = Date.now()
    header['Host'] = 'zt.wps.cn'
    header['sid'] = sid
    url = `https://zt.wps.cn/2018/clock_in/api/clock_in?award=wps&client=wechat&_t=${time}&client_code=003ZRi200j5E0P13MT200yOdLI1ZRi2g&captcha=40%2C50%7C105%2C50`
    return new Promise(resolve => {
       fetch(url, {method: 'GET',headers: header}).then(response => {
          return response.json()
        }).then(body => {
          console.log(body)
          resolve(body.result)
        }).catch(e => {
          const error = '会员打卡出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        })
    });
}

//获取会员打卡后信息
function get_Vipstatus() {
    time = Date.now()
    url = `https://zt.wps.cn/2018/clock_in/api/get_data?member=wps`
    return new Promise(resolve => {
       fetch(url, {method: 'GET',headers: header}).then(response => {
          return response.json()
        }).then(body => {
          if (body.is_clock_in == 1) {
               info += `今日顺利打卡~\n`;
          } else {
               info += `今日打卡失败！\n`;
          }
        }).catch(e => {
          const error = '打卡出现错误，请检查⚠️';
          console.log(error + '\n' + e);
        }).finally(() => {
          resolve()
        })
    });
}

module.exports = wps;
