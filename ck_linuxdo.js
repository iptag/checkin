# -*- coding: utf-8 -*-
# 原作者：WowYiJiu@Linux.do-KeepAlive 
# 地址：https://github.com/WowYiJiu/Linux.do-KeepAlive
# 使用claude精简了原作者的代码，并小修改了部门执行逻辑，多账号能完美运行
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import shutil, os, time, logging, random, requests

# 设置日志
logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%H:%M:%S')

# 环境变量，多账号间以英文逗号','分割，环境变量新增一个'LINUXDO'，内容为'账号1@密码1,账号2@密码2,账号3@密码3'
USERNAME, PASSWORD = zip(*(item.split('@') for item in os.getenv("LINUXDO", "").split(',')))
SCROLL_DURATION = 3 #可修改，数值越大，浏览的时间越长，浏览的帖子越多，为3时浏览90个帖子，为5时浏览120个帖子
VIEW_COUNT = 10000 #可修改，帖子浏览量大于该数值时，才点赞
HOME_URL = "https://linux.do/"
CONNECT_URL = "https://connect.linux.do/"

# 验证配置
if not USERNAME or not PASSWORD:
    logging.error("缺少必要配置: USERNAME 或 PASSWORD，请在环境变量中设置。")
    exit(1)
if len(USERNAME) != len(PASSWORD):
    logging.error("用户名和密码的数量不一致，请检查环境变量设置。")
    exit(1)
logging.info(f"共找到 {len(USERNAME)} 个账户")

class LinuxDoBrowser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None

    def setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chromedriver_path = shutil.which("chromedriver")
        if not chromedriver_path:
            logging.error("chromedriver 未找到，请确保已安装并配置正确的路径。")
            exit(1)
        self.driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)

    def simulate_typing(self, element, text, typing_speed=0.1):
        for char in text:
            element.send_keys(char)
            time.sleep(typing_speed + random.uniform(0, 0.1))

    def login(self):
        try:
            logging.info(f"--- 开始尝试登录：{self.username}---")
            self.driver.get(HOME_URL)
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-button .d-button-label"))
            )
            login_button.click()
            username_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#login-account-name"))
            )
            self.simulate_typing(username_field, self.username)
            password_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#login-account-password"))
            )
            self.simulate_typing(password_field, self.password)
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-button"))
            )
            submit_button.click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#current-user"))
            )
            logging.info("登录成功")
            return True
        except Exception as e:
            error_message = self.driver.find_elements(By.CSS_SELECTOR, "#modal-alert.alert-error")
            if error_message:
                logging.error("登录失败：用户名、电子邮件或密码不正确")
            else:
                logging.error(f"登录失败：{e}")
            return False

    def load_all_topics(self):
        end_time = time.time() + SCROLL_DURATION
        actions = ActionChains(self.driver)
        while time.time() < end_time:
            actions.scroll_by_amount(0, 500).perform()
            time.sleep(0.1)
        logging.info("页面滚动完成，已停止加载更多帖子")

    def click_topic(self):
        self.load_all_topics()
        topics = self.driver.find_elements(By.CSS_SELECTOR, "#list-area .title")
        logging.info(f"共找到 {len(topics)} 个帖子")
        for idx, topic in enumerate(topics):
            parent_element = topic.find_element(By.XPATH, "./ancestor::tr")
            if parent_element.find_elements(By.CSS_SELECTOR, ".topic-statuses .pinned"):
                logging.info(f"跳过置顶的帖子：{topic.text.strip()}")
                continue
            views_element = parent_element.find_element(By.CSS_SELECTOR, ".num.views .number")
            views_count = int(views_element.get_attribute("title").split("此话题已被浏览 ")[1].split(" 次")[0].replace(",", ""))
            article_title = topic.text.strip()
            logging.info(f"打开第 {idx + 1}/{len(topics)} 个帖子 ：{article_title}")
            article_url = topic.get_attribute("href")
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            try:
                self.driver.get(article_url)
                time.sleep(3)
                if views_count > VIEW_COUNT:
                    logging.info(f"📈 当前帖子浏览量为{views_count}")
                    logging.info(f"🥳 当前帖子浏览量大于设定值{VIEW_COUNT}，开始进行点赞操作")
                    self.click_like()
                self.scroll_article()
            except Exception as e:
                logging.warning(f"处理帖子时发生错误: {e}")
            finally:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                logging.info(f"已关闭第 {idx + 1}/{len(topics)} 个帖子")

    def scroll_article(self):
        start_time = time.time()
        scroll_duration = random.uniform(5, 10)
        try:
            while time.time() - start_time < scroll_duration:
                self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(0.5)
        except Exception as e:
            logging.warning(f"在滚动过程中发生错误: {e}")

    def click_like(self):
        try:
            like_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-toggle-reaction-like"))
            )
            if "移除此赞" not in like_button.get_attribute("title"):
                self.driver.execute_script("arguments[0].click();", like_button)
                logging.info("点赞帖子成功")
            else:
                logging.info("该帖子已点赞，跳过点赞操作。")
        except Exception as e:
            logging.error(f"点赞操作失败: {e}")

    def fetch_user_data(self, username):
        try:
            response = requests.get(f"https://linux.do/u/{username}/summary.json")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as error:
            logging.error(f"获取用户数据失败：{error}")
            return None

    def update_popup_content(self, user_summary, user):
        TRANSLATIONS = {
            "days_visited": "访问天数", "likes_given": "给出的赞", "likes_received": "收到的赞",
            "post_count": "帖子数量", "posts_read_count": "阅读的帖子数", "topics_entered": "进入的主题数",
            "time_read": "阅读时间"
        }
        LEVEL_DESCRIPTIONS = {0: "游客", 1: "基本用户", 2: "成员", 3: "活跃用户", 4: "领导者"}
        LEVEL_REQUIREMENTS = {
            0: {"topics_entered": 5, "posts_read_count": 30, "time_read": 600},
            1: {"days_visited": 15, "likes_given": 1, "likes_received": 1, "post_count": 3,
                "topics_entered": 20, "posts_read_count": 100, "time_read": 3600},
            2: {"days_visited": 50, "likes_given": 30, "likes_received": 20, "post_count": 10,
                "topics_entered": 500, "posts_read_count": 20000}
        }
        trust_level = user['trust_level']
        content = f"信任等级：{LEVEL_DESCRIPTIONS[trust_level]}\n升级进度：\n"
        if trust_level == 3:
            return content + "联系管理员以升级到领导者"
        elif trust_level == 4:
            return content + "您已是最高信任等级"
        requirements = LEVEL_REQUIREMENTS[trust_level]
        return content + '\n'.join(f"{TRANSLATIONS[key]}: {user_summary.get(key, 0)} / {val}" for key, val in requirements.items())

    def print_connect_info(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(CONNECT_URL)
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table tr")
        info = [
            [cells[0].text.strip(), cells[1].text.strip(), cells[2].text.strip()]
            for row in rows[1:]  # Skip header row
            if (cells := row.find_elements(By.TAG_NAME, "td")) and len(cells) >= 3
        ]
        print("在过去 💯 天内：")
        for row in info:
            print(f"{row[0]}（{row[2]}）：{row[1]}")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def logout(self):
        try:
            self.driver.find_element(By.ID, "toggle-current-user").click()
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.ID, "user-menu-button-profile"))
            ).click()
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.logout button.profile-tab-btn"))
            ).click()
            self.driver.refresh()
            if self.driver.find_elements(By.CSS_SELECTOR, ".header-buttons .login-button"):
                logging.info(f"{self.username}登出成功")
            else:
                logging.info(f"{self.username}登出失败")
        except Exception as e:
            logging.error(f"登出过程中发生错误: {e}")

    def run(self):
        self.setup_driver()
        start_time = time.time()
        logging.info(f"▶️▶️▶️  开始执行账号: {self.username}")
        if self.login():
            self.click_topic()
            logging.info(f"🎉恭喜：{self.username}，帖子浏览全部完成")
            # self.print_connect_info()
            if user_data := self.fetch_user_data(self.username):
                print(self.update_popup_content(user_data['user_summary'], user_data['users'][0]))
            self.logout()
        spend_time = int((time.time() - start_time) // 60)
        logging.info(f"账号 {self.username} 处理完毕，共用时 {spend_time} 分钟")
        self.driver.quit()

def main():
    for username, password in zip(USERNAME, PASSWORD):
        browser = LinuxDoBrowser(username, password)
        browser.run()
        time.sleep(2)
    logging.info("所有账户处理完毕")

if __name__ == "__main__":
    main()
