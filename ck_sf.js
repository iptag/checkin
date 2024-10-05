/*
1 9 * * * ck_sfexpress.js
android/ios用户请下载9.41.0版本或以后版本，header和headers需要抓取自己手机的，特别要注意languageCode，clientVersion和User-Agent，否则运行出错
*/
const utils = require('./utils');
const fetch = require('node-fetch');
const md5 = require('js-md5');
const Env = utils.Env;
const $ = new Env('顺丰速运');
const getData = utils.getData;
const sleep = utils.sleep;
const notify = require('./sendNotify');
const AsVow = getData().SFEXPRESS;
var desp = '';
var info = '';
header ={
    "regionCode": 'CN',
    "languageCode": 'sc',
    "clientVersion": '9.48.0',
    "carrier": "",
    "model": 'iPhone 12',
    "screenSize": '1170x2532',
    "systemVersion": '14.2.1',
    "mediaCode": 'iOSML',
    "Content-Type": "application/json; charset=utf-8",
    "Host": 'ccsp-egmas.sf-express.com',
    "User-Agent": "SFMainland_Store_Pro/9.48.0 (iPhone; iOS 14.2.1; Scale/3.00)",
}
headers = {
    "Host": "mcs-mimp-web.sf-express.com",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 mediaCode=SFEXPRESSAPP-iOS-ML",
}

sfexpress();

async function sfexpress() {
    if (AsVow) {
        for (i in AsVow) {
            jsbundle = AsVow[i].jsbundle;
            deviceId = AsVow[i].deviceId;
            memNo = AsVow[i].memNo;
            info +=`=== 正对在第 ${i+1} 个账号签到===\n`;
            console.log(1)
            usrinfo = await callfunc(getUserInfo,3).then(data => data);
            console.log(2)
            body = {"needReqTime":"1","memNo":memNo,"mobile":usrinfo.phone,"userId":usrinfo.id,"extra":"","name":"mcs-mimp-web.sf-express.com"}
            header['memberId'] = usrinfo.id
            sign = await callfunc(getSign,3,body).then(data => data);
            console.log(3)
            cookies = await callfunc(getCookie,3,sign.sign).then(data => data);
            console.log(4)
            headers['Referer'] = cookies.trueurl
            headers['Content-Type'] = "application/json;charset=utf-8"
            headers['Cookie'] = cookies.cookie
            countday = await callfunc(normsign,3).then(data => data);
            console.log(5)
            await callfunc(surpsign,3);
            console.log(6)
            list = await callfunc(task_list,3).then(data => data);
            list1 = list.list
            console.log(7)
            for (i in list1) {
               taskId = list1[i].taskId;
               strategyId = list1[i].strategyId;
               taskCode = list1[i].taskCode;
               title = list1[i].description;
               taskPeriod = list1[i].taskPeriod;
               if (title.includes('邀请')) {
                   continue;
               } else if (taskPeriod.includes('D')){
                   await callfunc(do_mission,3,title,taskCode);
                   console.log(8)
                   await sleep(Math.floor(Math.random() * 3000));
                   await callfunc(reward_mission,3,title,strategyId,taskId,taskCode);
                   console.log(9)
                } else if (taskPeriod.includes('W') && countday.countday == 7){
                   await callfunc(do_mission,3,title,taskCode);
                   console.log(10)
                   await sleep(Math.floor(Math.random() * 3000));
                   await callfunc(reward_mission,3,title,strategyId,taskId,taskCode);
                   console.log(11)
               }
               desp += info
               info = ''
            }
            headers['Referer'] = "https://mcs-mimp-web.sf-express.com/pointLottery"
            await callfunc(do_lottery,3);
            desp += info
            info = ''
        }
        info = desp
        console.log(info);
        notify.sendNotify('顺丰速运', info);
    } else {
        info = '签到失败：请先获取Cookie⚠️';
        notify.sendNotify('顺丰速运', info);
    }
    $.done()
}

//获取必要信息
function getUserInfo() {
    url = 'https://ccsp-egmas.sf-express.com/cx-app-member/member/app/user/queryUserInfo'
    body = JSON.stringify({"memNo":memNo})
    controller = new AbortController()
    signal = controller.signal
    time = Date.now()
    header['sytToken'] =get_sytToken(time,body)
    header['jsbundle'] =jsbundle
    header['deviceId'] =deviceId
    header['timeInterval'] =time
    data = {}
    return new Promise(resolve => {
      fetch(url, {
        method: 'POST',
        headers: header,
        body: body,
        signal: controller.signal
      }).then(response => {
        return response.json()
      }).then(body => {
        // console.log(body)
        data.id = body.obj.userId
        data.phone = body.obj.mobile
        data.flag = false
        resolve(data)
      }).catch(e => {
        if (e.name === "AbortError") {
          const error = `getUserInfo任务，发生超时\n`
          console.log(error + e);
          info += error
          data.flag = false
          resolve(data)
        } else {
          const error = 'getUserInfo出现错误，请检查⚠️\n';
          console.log(error + e);
          info += error
          data.flag = false
          resolve(data)
        }
      })
      setTimeout(() => controller.abort(), 20000)
    });
}

//获取sign
function getSign(t) {
    url = 'https://ccsp-egmas.sf-express.com/cx-app-member/member/app/user/universalSign'
    body = JSON.stringify(t)
    controller = new AbortController()
    signal = controller.signal
    time = Date.now()
    header['sytToken'] =get_sytToken(time,body)
    header['timeInterval'] =time
    data = {}
    return new Promise(resolve => {
      fetch(url, {
        method: 'POST',
        headers: header,
        body: body,
        signal: controller.signal
      }).then(response => {
        return response.json()
      }).then(body => {
        // console.log(body)
        data.sign = body.obj.sign
        data.flag = false
        resolve(data)
      }).catch(e => {
        if (e.name === "AbortError") {
          const error = `getSign任务，发生超时\n`
          console.log(error + e);
          info += error
          data.flag = false
          resolve(data)
        } else {
          const error = 'getSign出现错误，请检查⚠️\n';
          console.log(error + e);
          info += error
          data.flag = false
          resolve(data)
        }
      })
      setTimeout(() => controller.abort(), 20000)
    });
}

//获取cookie
function getCookie(t) {
    url = `https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect?sign=${encodeURIComponent(t)}&source=SFAPP&bizCode=647`
    controller = new AbortController()
    signal = controller.signal
    data = {}
    return new Promise(resolve => {
      fetch(url, {
        method: 'GET',
        headers: headers,
        redirect: 'manual',
        signal: controller.signal
      }).then(response => {
        // console.log(response.headers)
        data.trueurl = response.headers.get('Location')
        tmp = response.headers.get('set-cookie')
        pat = /sessionId=([\w]+);/g
        sessionid = pat.exec(tmp)
        data.cookie = `JSESSIONID=${sessionid[1]}.node0;_login_mobile_=${usrinfo.phone};_login_user_id_=${usrinfo.id};${sessionid[0]}`
        data.flag = false
        resolve(data)
      }).catch(e => {
        if (e.name === "AbortError") {
          const error = `getcookie任务，发生超时\n`
          console.log(error + e);
          info += error
          data.flag = false
          resolve(data)
        } else {
          const error = 'getcookie出现错误，请检查⚠️\n';
          console.log(error + e);
          info += error
          data.flag = false
          resolve(data)
        }
      })
      setTimeout(() => controller.abort(), 20000)
    });
}

//普通签到
function normsign() {
    url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~automaticSignFetchPackage'
    body = {"comeFrom": "vioin", "channelFrom": "SFAPP"}
    controller = new AbortController()
    signal = controller.signal
    return new Promise(resolve => {
      fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body),
        signal: controller.signal
      }).then(response => {
        return response.json()
      }).then(body => {
        if (body.success) {
            if (body.obj.hasFinishSign == 0) {
              info += `---首次签到成功---\n今日获得 ${body.obj.integralTaskSignPackageVOList[0].packetName}\n连续签到 ${body.obj.countDay} 天\n`;
            } else {
              info += `今日已签到过啦~\n`;
            }
            data.countday = body.obj.countDay;
        } else {
             info += "普通签到返回错误，请重新调试\n";
             console.log(info);
             console.log(body);
        }
        data.flag = false
        resolve(data)
      }).catch(e => {
        if (e.name === "AbortError") {
          const error = `普通签到任务，发生超时\n`
          console.log(error + e);
          info += error   
          data.flag = true
          resolve(data)          
        } else {
          const error = '普通签到出现错误，请检查⚠️\n';
          console.log(error + e);
          info += error
          data.flag = false
          resolve(data)
        }
      })
      setTimeout(() => controller.abort(), 20000)
    });
}

//超值福利签到
function surpsign() {
    url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberActLengthy~redPacketActivityService~superWelfare~receiveRedPacket'
    body = {"channel":"czflqdlhbapp"};
    controller = new AbortController()
    signal = controller.signal
    data = {}
    return new Promise(resolve => {
      fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body),
        signal: controller.signal
      }).then(response => {
        return response.json()
      }).then(body => {
        if (body.success) {
            list = body.obj.giftList;
            for (i in list) {
                prize = list[i].giftName;
                info += `---超值福利签到成功---\n获得 ${prize} 奖励\n`;
            }
        } else {
            info += "超值签到返回错误，请重新调试\n";
            console.log(info);
        }
        data.flag = false
        resolve(data)
      }).catch(e => {
          if (e.name === "AbortError") {
            const error = `超值签到任务，发生超时\n`
            console.log(error + e);
            info += error 
            data.flag = true
            resolve(data)            
          } else {
            const error = '超值签到返回错误，请检查⚠️\n';
            console.log(error + e);
            info += error
            data.flag = false
            resolve(data)
          }
      }).finally(() => {
          resolve()
      })
      setTimeout(() => controller.abort(), 20000)
    });
}

//获取任务列表
function task_list() {
    url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~queryPointTaskAndSignFromES'
    body = {"channelType":"1"};
    controller = new AbortController()
    signal = controller.signal
    data = {}
    return new Promise(resolve => {
      fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body),
        signal: controller.signal
      }).then(response => {
        return response.json()
      }).then(body => {
        data.list = body.obj.taskTitleLevels;
        data.flag = false
        resolve(data)
      }).catch(e => {
        if (e.name === "AbortError") {
          const error = `获取任务列表，发生超时\n`
          console.log(error + e);
          info += error   
          data.flag = true
          resolve(data)          
        } else {
          const error = '获取任务列表返回错误，请检查⚠️\n';
          console.log(error + e);
          info += error
          data.flag = false
          resolve(data)
        }
      })
      setTimeout(() => controller.abort(), 20000)
    });
}

//做任务
function do_mission(title, taskCode) {
    url = `https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask`
    body = {"taskCode":taskCode}
    controller = new AbortController()
    signal = controller.signal
    data = {}
    return new Promise(resolve => {
      fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body),
        signal: controller.signal
      }).then(response => {
        return response.json()
      }).then(body => {
        if (body.success) {
             sleep(Math.floor(Math.random() * 5000));
        } else {
             info += `执行 ${title} 任务出现错误，请重新调试\n`;
             console.log(info);
        }
        data.flag = false
        resolve(data)
      }).catch(e => {
        if (e.name === "AbortError") {
          const error = `执行 ${title} 任务，发生超时\n`
          console.log(error + e);
          info += error
          data.flag = true
          resolve(data)          
        } else {
          const error = `执行 ${title} 任务返回错误，请检查⚠️\n`;
          console.log(error + e);
          info += error
          data.flag = false
          resolve(data)
        }
      })
      setTimeout(() => controller.abort(), 20000)
    });
}

//领取奖励
function reward_mission (title, strategyId, taskId, taskCode) {
    url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~fetchIntegral'
    body = {"strategyId":strategyId,"taskId":taskId,"taskCode":taskCode};
    controller = new AbortController()
    signal = controller.signal
    data = {}
    return new Promise(resolve => {
      fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body),
        signal: controller.signal
      }).then(response => {
        return response.json()
      }).then(body => {
        if (body.success) {
            info += `执行 ${title} 任务成功，领取 ${body.obj.point} 积分\n`;
        } else if (body.errorMessage.includes('已领取')){
            info += `${title} 任务已完成\n\n`;
        } else {
            info += `任务异常，显示${body.errorMessage}\n`;
        }
        data.flag = false
        resolve(data)
      }).catch(e => {
         if (e.name === "AbortError") {
           const error = `领取 ${title} 任务积分，发生超时\n`
           console.log(error + e);
           info += error
           data.flag = true
           resolve(data)
         } else {
           const error = `领取 ${title} 任务积分返回错误，请检查⚠️\n`;
           console.log(error + e);
           info += error
           data.flag = false
           resolve(data)
         }
      })
      setTimeout(() => controller.abort(), 20000)
    });
}

//抽奖任务
function do_lottery() {
    url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~multiIntegralLotteryService~lottery'
    body = {"lotteryType":"NINE_POINT","continuityLotteryFlag":0};
    controller = new AbortController()
    signal = controller.signal
    data = {}
    return new Promise(resolve => {
      fetch(url, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body),
        signal: controller.signal
      }).then(response => {
        return response.json()
      }).then(body => {
        if (body.success) {
             info += `执行抽奖任务，获得 ${body.obj[0].commodityName} 奖励\n`;
        }
        data.flag = false
        resolve(data)
      }).catch(e => {
          if (e.name === "AbortError") {
            const error = "执行抽奖任务，发生超时\n"
            console.log(error + e);
            info += error
            data.flag = true
            resolve(data)
          } else {
            const error = `执行抽奖任务返回错误，请检查⚠️\n`;
            console.log(error + e);
            info += error
            data.flag = false
            resolve(data)
          }
      })
      setTimeout(() => controller.abort(), 20000)
    });
}

//请求超时则重试count次
async function callfunc(task,count,a,b,c,d) {
  while (count--) {
    data = await task(a,b,c,d).then(data => data)
    if (!data.flag) {
        count = 0
    }
    console.log(`执行了${3-count}次`)
  }
  return data
}

function get_sytToken(t,b) {
    p0=b+"&"+"080R3MAC57J2{A19!$3:WO{I<1N$31BI"
    tmp=md5(deviceId+t+header['clientVersion']+"2NBF+BE4{@P:@X${Q9BAE>{PAK!D:N*^"+"CN"+header['languageCode']+md5(p0)+jsbundle+"&"+"2NBF+BE4{@P:@X${Q9BAE>{PAK!D:N*^")
    sytToken = md5(tmp+"&"+"0HQ%H91K&AA{DH$*XV>XR)VKL:QFE{&%")
    return sytToken
}
module.exports = sfexpress;
