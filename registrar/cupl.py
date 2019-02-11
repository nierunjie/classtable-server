from . import urp


class CUPL(urp.URP):
    def base_url(self):
        return 'http://urp.cupl.edu.cn/'

    def get_captcha_base64(self):
        pass
