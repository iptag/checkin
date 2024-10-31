"""
打开小程序或APP-我的-积分, 抓包以下几种url开头的链接（随便一个）,把整个url放到变量对应的cookie里
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/activityRedirect
https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/activityRedirect
"""
import hashlib, json, os, random, time, re, requests
from datetime import datetime, timedelta
from urllib3.exceptions import InsecureRequestWarning

from sendNotify import send
from utils import get_data

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

one_msg = ''

def log(cont=''):
    global one_msg
    print(cont)
    if cont:
        one_msg += f'{cont}\n'

inviteId = [
    '8C3950A023D942FD93BE9218F5BFB34B', 'EF94619ED9C84E968C7A88CFB5E0B5DC',
    '9C92BD3D672D4B6EBB7F4A488D020C79', '803CF9D1E0734327BDF67CDAE1442B0E',
    '00C81F67BE374041A692FA034847F503', '3F7E28CDA0D44D75B74FC5CCD1030FC7',
    'DE79938CF377404981DC744F9D4CBBED'
]

class RUN:
    def __init__(self, info, index):
        global one_msg
        one_msg = ''
        split_info = info.split('@')
        self.url = split_info[0]
        self.send_UID = split_info[-1] if len(split_info) > 1 and "UID_" in split_info[-1] else None
        self.index = index + 1
        log(f"---------开始执行第{self.index}个账号---------")
        self.s = requests.session()
        self.s.verify = False
        self.headers = {
            'Host': 'mcs-mimp-web.sf-express.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555',
            'platform': 'MINI_PROGRAM',
        }
        self.anniversary_black = False
        self.member_day_black = False
        self.member_day_red_packet_drew_today = False
        self.member_day_red_packet_map = {}
        self.login_res = self.login(self.url)
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.answer = False
        self.max_level = 8
        self.packet_threshold = 1 << (self.max_level - 1)

    def get_deviceId(self):
        return ''.join(random.choice('abcdef0123456789') for _ in range(32))

    def login(self, sfurl):
        ress = self.s.get(sfurl, headers=self.headers)
        self.user_id = self.s.cookies.get_dict().get('_login_user_id_', '')
        self.phone = self.s.cookies.get_dict().get('_login_mobile_', '')
        self.mobile = f"{self.phone[:3]}****{self.phone[7:]}"
        if self.phone:
            log(f'用户:【{self.mobile}】登陆成功')
            return True
        else:
            log(f'获取用户信息失败')
            return False

    def getSign(self):
        timestamp = str(int(time.time() * 1000))
        token = 'wwesldfs29aniversaryvdld29'
        sysCode = 'MCS-MIMP-CORE'
        data = f'token={token}&timestamp={timestamp}&sysCode={sysCode}'
        signature = hashlib.md5(data.encode()).hexdigest()
        self.headers.update({
            'sysCode': sysCode,
            'timestamp': timestamp,
            'signature': signature
        })
        return {
            'sysCode': sysCode,
            'timestamp': timestamp,
            'signature': signature
        }

    def do_request(self, url, data={}, req_type='post'):
        self.getSign()
        try:
            if req_type.lower() == 'get':
                response = self.s.get(url, headers=self.headers)
            elif req_type.lower() == 'post':
                response = self.s.post(url, headers=self.headers, json=data)
            else:
                raise ValueError('Invalid req_type: %s' % req_type)
            return response.json()
        except requests.exceptions.RequestException as e:
            print('Request failed:', e)
        except json.JSONDecodeError as e:
            print('JSON decoding failed:', e)
        return None

    def sign(self):
        print(f'---开始执行签到---')
        json_data = {"comeFrom": "vioin", "channelFrom": "WEIXIN"}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~automaticSignFetchPackage'
        response = self.do_request(url, data=json_data)
        if response and response.get('success'):
            count_day = response.get('obj', {}).get('countDay', 0)
            if response.get('obj') and response['obj'].get('integralTaskSignPackageVOList'):
                packet_name = response["obj"]["integralTaskSignPackageVOList"][0]["packetName"]
                log(f'签到成功，获得【{packet_name}】，本周累计签到【{count_day + 1}】天')
            else:
                log(f'今日已签到，本周累计签到【{count_day + 1}】天')
        else:
            print(f'签到失败！原因：{response.get("errorMessage") if response else "无返回"}')

    def superWelfare_receiveRedPacket(self):
        print(f'---超值福利签到---')
        json_data = {'channel': 'czflqdlhbxcx'}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberActLengthy~redPacketActivityService~superWelfare~receiveRedPacket'
        response = self.do_request(url, data=json_data)
        if response and response.get('success'):
            gift_list = response.get('obj', {}).get('giftList', []) or []
            if response.get('obj', {}).get('extraGiftList'):
                gift_list.extend(response['obj']['extraGiftList'])
            gift_names = ', '.join([gift['giftName'] for gift in gift_list]) if gift_list else '无奖励'
            receive_status = response.get('obj', {}).get('receiveStatus')
            status_message = '领取成功' if receive_status == 1 else '已领取过'
            log(f'超值福利签到[{status_message}]: {gift_names}')
        else:
            error_message = response.get('errorMessage') or json.dumps(response) or '无返回'
            print(f'超值福利签到失败: {error_message}')

    def get_SignTaskList(self, END=False):
        if not END: print(f'---开始获取签到任务列表---')
        json_data = {
            'channelType': '3',
            'deviceId': self.get_deviceId(),
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~queryPointTaskAndSignFromES'
        response = self.do_request(url, data=json_data)
        if response and response.get('success') and response.get('obj'):
            totalPoint = response["obj"]["totalPoint"]
            if END:
                log(f'当前积分：【{totalPoint}】')
                return
            log(f'执行前积分：【{totalPoint}】')
            for task in response["obj"]["taskTitleLevels"]:
                self.taskId = task["taskId"]
                self.taskCode = task["taskCode"]
                self.strategyId = task["strategyId"]
                self.title = task["title"]
                status = task["status"]
                skip_title = ['用行业模板寄件下单', '去新增一个收件偏好', '参与积分活动']
                if status == 3:
                    print(f'{self.title}-已完成')
                    continue
                if self.title in skip_title:
                    print(f'{self.title}-跳过')
                    continue
                else:
                    self.doTask()
                    time.sleep(3)
                self.receiveTask()
        else:
            print(f'获取签到任务列表失败: {response.get("errorMessage") if response else "无返回"}')

    def doTask(self):
        print(f'---开始去完成 {self.title} 任务---')
        json_data = {'taskCode': self.taskCode,}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonRoutePost/memberEs/taskRecord/finishTask'
        response = self.do_request(url, data=json_data)
        if response and response.get('success'):
            print(f'{self.title} 已完成')
        else:
            print(f'{self.title} {response.get("errorMessage") if response else "无返回"}')

    def receiveTask(self):
        print(f'---开始领取 {self.title} 任务奖励---')
        json_data = {
            "strategyId": self.strategyId,
            "taskId": self.taskId,
            "taskCode": self.taskCode,
            "deviceId": self.get_deviceId()
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~fetchIntegral'
        response = self.do_request(url, data=json_data)
        if response and response.get('success'):
            print(f'{self.title} 任务奖励领取成功！')
        else:
            print(f'{self.title} {response.get("errorMessage") if response else "无返回"}')

    def do_honeyTask(self):
        json_data = {"taskCode": self.taskCode}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask'
        response = self.do_request(url, data=json_data)
        if response and response.get('success'):
            print(f'{self.taskType} 已完成')
        else:
            print(f'{self.taskType} {response.get("errorMessage") if response else "无返回"}')

    def get_coupom(self):
        print('---执行领取生活权益领券任务---')
        json_data = {
            "from": "Point_Mall",
            "orderSource": "POINT_MALL_EXCHANGE",
            "goodsNo": self.goodsNo,
            "quantity": 1,
            "taskCode": self.taskCode
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~pointMallService~createOrder'
        response = self.do_request(url, data=json_data)
        if response and response.get('success'):
            print(f'领券成功！')
        else:
            print(f'领券失败！原因：{response.get("errorMessage") if response else "无返回"}')

    def get_coupom_list(self):
        print('---获取生活权益券列表---')
        json_data = {
            "memGrade": 1,
            "categoryCode": "SHTQ",
            "showCode": "SHTQWNTJ"
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~mallGoodsLifeService~list'
        response = self.do_request(url, data=json_data)
        if response and response.get('success'):
            goodsList = response["obj"][0]["goodsList"]
            for goods in goodsList:
                exchangeTimesLimit = goods['exchangeTimesLimit']
                if exchangeTimesLimit >= 7:
                    self.goodsNo = goods['goodsNo']
                    print(f'当前选择券号：{self.goodsNo}')
                    self.get_coupom()
                    break
        else:
            print(f'领券失败！原因：{response.get("errorMessage") if response else "无返回"}')

    def addDeliverPrefer(self):
        print(f'开始【{self.title}】任务')
        json_data = {
            "country": "中国",
            "countryCode": "A000086000",
            "province": "北京市",
            "provinceCode": "A110000000",
            "city": "北京市",
            "cityCode": "A111000000",
            "county": "东城区",
            "countyCode": "A110101000",
            "address": "1号楼1单元101",
            "latitude": "",
            "longitude": "",
            "memberId": "",
            "locationCode": "010",
            "zoneCode": "CN",
            "postCode": "",
            "takeWay": "7",
            "callBeforeDelivery": 'false',
            "deliverTag": "2,3,4,1",
            "deliverTagContent": "",
            "startDeliverTime": "",
            "selectCollection": 'false',
            "serviceName": "",
            "serviceCode": "",
            "serviceType": "",
            "serviceAddress": "",
            "serviceDistance": "",
            "serviceTime": "",
            "serviceTelephone": "",
            "channelCode": "RW11111",
            "taskId": self.taskId,
            "extJson": "{\"noDeliverDetail\":[]}"
        }
        url = 'https://ucmp.sf-express.com/cx-wechat-member/member/deliveryPreference/addDeliverPrefer'
        response = self.do_request(url, data=json_data)
        if response and response.get('success'):
            print('新增一个收件偏好，成功')
        else:
            print(f'【{self.title}】{response.get("errorMessage") if response else "无返回"}')

    def member_day_index(self):
        print('---会员日活动---')
        try:
            invite_user_id = random.choice([invite for invite in inviteId if invite != self.user_id])
            payload = {'inviteUserId': invite_user_id}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayIndexService~index'

            response = self.do_request(url, data=payload)
            if response and response.get('success'):
                lottery_num = response.get('obj', {}).get('lotteryNum', 0)
                can_receive_invite_award = response.get('obj', {}).get('canReceiveInviteAward', False)
                if can_receive_invite_award:
                    self.member_day_receive_invite_award(invite_user_id)
                self.member_day_red_packet_status()
                log(f'会员日可以抽奖{lottery_num}次')
                for _ in range(lottery_num):
                    self.member_day_lottery()
                if not self.member_day_black:
                    self.member_day_task_list()
                    self.member_day_red_packet_status()
            else:
                error_message = response.get('errorMessage', '无返回')
                log(f'查询会员日失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    log('会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_receive_invite_award(self, invite_user_id):
        try:
            payload = {'inviteUserId': invite_user_id}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayIndexService~receiveInviteAward'
            response = self.do_request(url, payload)
            if response and response.get('success'):
                product_name = response.get('obj', {}).get('productName', '空气')
                log(f'会员日奖励: {product_name}')
            else:
                error_message = response.get('errorMessage', '无返回')
                log(f'领取会员日奖励失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    log('会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_lottery(self):
        try:
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayLotteryService~lottery'
            response = self.do_request(url)
            if response and response.get('success'):
                product_name = response.get('obj', {}).get('productName', '空气')
                log(f'会员日抽奖: {product_name}')
            else:
                error_message = response.get('errorMessage', '无返回')
                log(f'会员日抽奖失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    log('会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_task_list(self):
        try:
            payload = {'activityCode': 'MEMBER_DAY', 'channelType': 'MINI_PROGRAM'}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList'
            response = self.do_request(url, payload)
            if response and response.get('success'):
                task_list = response.get('obj', [])
                for task in task_list:
                    if task['status'] == 1:
                        if self.member_day_black:
                            return
                        self.member_day_fetch_mix_task_reward(task)
                for task in task_list:
                    if task['status'] == 2:
                        if self.member_day_black:
                            return
                        if task['taskType'] not in ['SEND_SUCCESS', 'INVITEFRIENDS_PARTAKE_ACTIVITY', 'OPEN_SVIP',
                                                    'OPEN_NEW_EXPRESS_CARD', 'OPEN_FAMILY_CARD', 'CHARGE_NEW_EXPRESS_CARD',
                                                    'INTEGRAL_EXCHANGE']:
                            for _ in range(task['restFinishTime']):
                                if self.member_day_black:
                                    return
                                self.member_day_finish_task(task)
            else:
                error_message = response.get('errorMessage', '无返回')
                log('查询会员日任务失败: ' + error_message)
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    log('会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_finish_task(self, task):
        try:
            payload = {'taskCode': task['taskCode']}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask'
            response = self.do_request(url, payload)
            if response and response.get('success'):
                log('完成会员日任务[' + task['taskName'] + ']成功')
                self.member_day_fetch_mix_task_reward(task)
            else:
                error_message = response.get('errorMessage', '无返回')
                log('完成会员日任务[' + task['taskName'] + ']失败: ' + error_message)
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    log('会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_fetch_mix_task_reward(self, task):
        try:
            payload = {'taskType': task['taskType'], 'activityCode': 'MEMBER_DAY', 'channelType': 'MINI_PROGRAM'}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~fetchMixTaskReward'
            response = self.do_request(url, payload)
            if response and response.get('success'):
                log('领取会员日任务[' + task['taskName'] + ']奖励成功')
            else:
                error_message = response.get('errorMessage', '无返回')
                log('领取会员日任务[' + task['taskName'] + ']奖励失败: ' + error_message)
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    log('会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_red_packet_status(self):
        try:
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketStatus'
            response = self.do_request(url)
            if response and response.get('success'):
                packet_list = response.get('obj', {}).get('packetList', [])
                for packet in packet_list:
                    self.member_day_red_packet_map[packet['level']] = packet['count']
                for level in range(1, self.max_level):
                    count = self.member_day_red_packet_map.get(level, 0)
                    while count >= 2:
                        self.member_day_red_packet_merge(level)
                        count -= 2
                packet_summary = []
                remaining_needed = 0
                for level, count in self.member_day_red_packet_map.items():
                    if count == 0:
                        continue
                    packet_summary.append(f"[{level}级]X{count}")
                    int_level = int(level)
                    if int_level < self.max_level:
                        remaining_needed += 1 << (int_level - 1)
                log("会员日合成列表: " + ", ".join(packet_summary))
                if self.member_day_red_packet_map.get(self.max_level):
                    log(f"会员日已拥有[{self.max_level}级]红包X{self.member_day_red_packet_map[self.max_level]}")
                    self.member_day_red_packet_draw(self.max_level)
                else:
                    remaining = self.packet_threshold - remaining_needed
                    log(f"会员日距离[{self.max_level}级]红包还差: [1级]红包X{remaining}")
            else:
                error_message = response.get('errorMessage', '无返回')
                log(f'查询会员日合成失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    log('会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_red_packet_merge(self, level):
        try:
            payload = {'level': level, 'num': 2}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketMerge'
            response = self.do_request(url, payload)
            if response and response.get('success'):
                log(f'会员日合成: [{level}级]红包X2 - [{level + 1}级]红包')
                self.member_day_red_packet_map[level] -= 2
                if not self.member_day_red_packet_map.get(level + 1):
                    self.member_day_red_packet_map[level + 1] = 0
                self.member_day_red_packet_map[level + 1] += 1
            else:
                error_message = response.get('errorMessage', '无返回')
                log(f'会员日合成两个[{level}级]红包失败: {error_message}')
                if '没有资格参与活动' in error_message:
                    self.member_day_black = True
                    log('会员日任务风控')
        except Exception as e:
            print(e)

    def member_day_red_packet_draw(self, level):
        try:
            payload = {'level': str(level)}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketDraw'
            response = self.do_request(url, payload)
            if response and response.get('success'):
                coupon_names = [item['couponName'] for item in response.get('obj', [])] or []
                log(f"会员日提取[{level}级]红包: {', '.join(coupon_names) or '空气'}")
            else:
                error_message = response.get('errorMessage') if response else "无返回"
                log(f"会员日提取[{level}级]红包失败: {error_message}")
                if "没有资格参与活动" in error_message:
                    self.memberDay_black = True
                    print("会员日任务风控")
        except Exception as e:
            print(e)

    def handle_error(self, error_message):
        if '没有资格参与活动' in error_message:
            self.Autumn_2024_black = True
            log('会员日任务风控')
        print(error_message)

    def main(self):
        global one_msg
        wait_time = random.uniform(1, 3)
        time.sleep(wait_time)
        one_msg = ''
        if not self.login_res:
            return False
        self.sign()
        self.superWelfare_receiveRedPacket()
        self.get_SignTaskList()
        self.get_SignTaskList(True)
        current_date = datetime.now().day
        if 26 <= current_date <= 28:
            self.member_day_index()
        else:
            print('未到指定时间不执行会员日任务')
        return one_msg

if __name__ == '__main__':
    data = get_data()
    tokens = data.get("SFEXPRESS", [])
    if not tokens:
        print(f'未检测到顺丰签到的cookie')
    else:
        for index, token in enumerate(tokens):
            res = RUN(token.get("cookie"), index).main()
            time.sleep(random.uniform(5, 8))
            send("顺丰签到", res)      
