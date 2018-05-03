from abc import abstractclassmethod

import requests


class Registrar:
    def __init__(self):
        self.session = requests.session()

    def get_state(self):
        return self.session.cookies.get_dict().get('JSESSIONID')

    def set_state(self, state):
        self.session.cookies.set('JSESSIONID', state)

    def start_time(self, date):
        date = str(date).split('/')
        self.year = date[2]
        self.month = date[0]
        self.day = date[1]

    @abstractclassmethod
    def get_captcha_base64(self):
        pass

    @abstractclassmethod
    def get_classtable(self, username, password, captcha):
        pass
