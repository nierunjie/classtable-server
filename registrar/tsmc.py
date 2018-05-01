import base64
import json
import re

import requests
from bs4 import BeautifulSoup

from . import registrar

MAP = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
               "六": 6, "日": 7}


def format_week_num(week_num_str):
    # 单周
    if week_num_str.find('单') != -1:
        week_num_str = re.sub(r'第|周|单', '', week_num_str)
        week_num_str = week_num_str.split('-')
        tmp = list(range(int(week_num_str[0]), int(
            week_num_str[len(week_num_str)-1])+1, 2))
        return tmp

    # 双周
    if week_num_str.find('双') != -1:
        week_num_str = re.sub(r'第|周|双', '', week_num_str)
        week_num_str = week_num_str.split('-')
        tmp = list(range(int(week_num_str[0])+1, int(
            week_num_str[len(week_num_str)-1])+1, 2))
        return tmp

    # 直接获取周
    if week_num_str.find(',') != -1:
        return list(map(eval, week_num_str.split(',')))

    # 常规
    week_num_str = re.sub(r'第|周', '', week_num_str)
    week_num_str = week_num_str.split('-')
    return list(range(int(week_num_str[0]), int(
        week_num_str[len(week_num_str)-1])+1))


def format_day_of_week(day_of_week):
    day_of_week = re.sub(r'星|期', '', day_of_week)
    return MAP.get(day_of_week)


def format_class_of_day(class_of_day):
    class_of_day = re.sub(r'上|下|晚|午|节', '', class_of_day)
    class_of_day = list(map(eval, class_of_day.split('-')))
    duration = max(class_of_day)-min(class_of_day)+1
    return (min(class_of_day), duration)


class TSMC(registrar.Registrar):
    def __init__(self):
        self.session = requests.session()
        self.captcha_url = None
        self.login_url = None
        self.classtable_url = None
        self.html_head = None
        self.headers = None

    def base_url(self):
        return 'http://jwc.tsmc.edu.cn/academic/'

    def generate(self):
        self.captcha_url = self.base_url()+'getCaptcha.do'
        self.login_url = self.base_url()+'j_acegi_security_check'
        self.classtable_url = self.base_url()+'student/currcourse/currcourse.jsdo'

        self.html_head = '<!DOCTYPE html><html><head><meta charset="utf-8"></head>'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }

    def get_state(self):
        return self.session.cookies.get_dict().get('JSESSIONID')

    def set_state(self, state):
        self.session.cookies.set('JSESSIONID', state)

    def get_captcha_base64(self):
        self.generate()
        try:
            captcha_pic = self.session.get(self.captcha_url, timeout=1).content
        except:
            return "TimeOut"

        if str(captcha_pic).find("html") != -1:
            return "UnknownError"

        return str(base64.b64encode(captcha_pic), encoding='utf-8')

    def start_time(self,date):
        date = str(date).split('/')
        self.year = date[2]
        self.month = date[0]
        self.day = date[1]

    def get_classtable(self, username, password, captcha):
        self.generate()
        user_info = {"j_username": username,
                     "j_password": password, "j_captcha": captcha}
        response = self.session.post(
            self.login_url, headers=self.headers, data=user_info)

        if str(response.text).find(u'验证码不正确') >= 0:
            return 'CaptchaError'
        try:
            text = self.html_head + \
                self.session.get(self.classtable_url, timeout=3).text
        except:
            return "Timeout"
        self.session.close()
        soup = BeautifulSoup(text, 'lxml')
        try:
            items = soup.find_all('table')[3]
        except IndexError:
            print("Username:{}\nPassword:{}\n")
            return "UnknownError"

        objs = []
        start = {"year": self.year, "month": self.month, "day": self.day}
        for item in items.find_all('tr', {'class': 'infolist_common'}):
            name = item.find_all('td')[2].get_text().strip()
            t = item.find_all('table')[0]
            for tt in t.find_all('tr'):
                ttt = tt.find_all('td')
                week_num_str = ttt[0].get_text().strip()
                week_num = format_week_num(week_num_str)
                day_of_week = format_day_of_week(ttt[1].get_text().strip())
                class_of_day, duration = format_class_of_day(
                    ttt[2].get_text().strip())
                place = ttt[3].get_text().strip()

                obj = {"name": name, "place": place, "day_of_week": day_of_week,
                       "class_of_day": class_of_day, "duration": duration, "week_num": week_num}
                objs.append(obj)
        ret = {"classtable": objs, "start": start}
        ret = json.dumps(ret, ensure_ascii=False)
        return(ret)

    def test(self):
        print('TSMC')
