/*
11 8 * * * ck_nga.js
*/
const utils = require('./utils');
const axios = require("axios");
const Env = utils.Env;
const getData = utils.getData;
const $ = new Env('NGA');
const notify = require('./sendNotify');
const AsVow = getData().NGA;
var info = '';
var desp = '';  

nga();

async function nga() {
  if (AsVow) {
    for (i in AsVow) {
      token = AsVow[i].token;
      uid = AsVow[i].uid;
      if (token && uid) {
        info += `===对${i+1} 账号签到===\n`;
        let res1 = await ngaGet("check_in", "check_in")
        if (res1 && res1.data) {
            info += "签到：" + res1.data[0] + "\n";
        } else {
            console.log("res1:" + res1);
            info += "签到：" + (res1.error && res1.error[0]) + "\n";
        }
        if (!info.match(/登录|CLIENT/)) {
            await ngaGet("mission", "checkin_count_add", 11, "mid=2&get_success_repeat=1&no_compatible_fix=1")
            await ngaGet("mission", "checkin_count_add", 11, "mid=131&get_success_repeat=1&no_compatible_fix=1")       
            await ngaGet("mission", "checkin_count_add", 11, "mid=30&get_success_repeat=1&no_compatible_fix=1")
            console.log("看视频免广告\n")
            info += "---看视频免广告---\n"
            await ngaGet("mission", "video_view_task_counter_add_v2_for_adfree_sp1")
            for (c of new Array(4)) await ngaGet("mission", "video_view_task_counter_add_v2_for_adfree")
            console.log("看视频得N币\n")
            info += "---看视频得N币---\n"
            for (c of new Array(5)) await ngaGet("mission", "video_view_task_counter_add_v2")
            //分享帖子
            console.log("分享帖子 5\n")
            info += "---分享帖子 5---\n"
            tid = Math.ceil(Math.random() * 12346567) + 12345678
            for (c of new Array(5)) await ngaGet("data_query", "topic_share_log_v2", 12, "event=4&tid=" + tid)
            console.log("领取分享奖励 1N币\n")
            info += "---领取分享奖励 1N币---\n"
            await ngaGet("mission", "check_mission", 11, "mid=149&get_success_repeat=1&no_compatible_fix=1")
            //查询
            let {
                data: [sign, money, y]
            } = await ngaGet("check_in", "get_stat")
            info += ` 连签 ${sign.continued}天 累签 ${sign.sum}天\n    N币：${money.money_n}\n    铜币：${money.money}\n    啊哈：${y[0]}\n`
        }
        desp += info;
        info = '';
      }
    }
    info += desp;
    console.log(info);
    notify.sendNotify('NGA', info);
  } else {
    info = '签到失败：请先获取Cookie⚠️';
    notify.sendNotify('NGA', info);
  }
  $.done()
}
    
function ngaGet(lib, act, output = 11, other = null) {
    return new Promise(async (resolve) => {
        try {
            let url = "https://ngabbs.com/nuke.php";
            let res = await axios.post(url,`access_uid=${uid}&access_token=${token}&app_id=1010&__act=${act}&__lib=${lib}&__output=${output}&${other}`, {
                    headers: {
                        "User-Agent": "Mozilla/5.0 (Linux; Android 10; NOH-AN00 Build/HUAWEINOH-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 Nga_Official/90021",
                    }
                }
            );            
            console.log("    " + (res.data && res.data.time || res.data.code))
            resolve(res.data)
        } catch (err) {
            console.log(err);
            resolve({
                error: ["签到接口请求出错"]
            })
        }
        resolve();
    });
}

module.exports = nga;
