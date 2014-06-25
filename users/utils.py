#coding:utf-8
import requests
from sgmllib import SGMLParser

"""
Parser html
handle tag <td> which contains information of user
capture user's information
"""
class UserInfo(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_td = ""
        self.value = []

    def start_td(self, attrs):
        self.is_td = 1

    def end_td(self):
        self.is_td = ""

    def handle_data(self, text):
        if self.is_td == 1:
            self.value.append(text)

"""
Parser html
handle tag <div> which contains the error info
capture error info
"""
class Authentication(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_div = ""
        self.string = "failed"
        self.status = "null"

    def start_div(self, attrs):
        #self.string = [v for k, v in attrs if k == "id"]
        for k, v in attrs:
            if k == 'id':
                self.string = v
        if self.string == "error":
            self.is_div = 1

    def end_div(self):
        self.is_div = ""

    def handle_data(self, text):
        if self.is_div == 1:
            self.status = text

"""
get captcha from school website and save session id
"""
def get_captcha(request):
    CAPTCHA_URL = "http://jw.qdu.edu.cn/academic/getCaptcha.do"
    session = requests.session()
    image = session.get(CAPTCHA_URL)
    request.session['JSESSIONID'] = session.cookies['JSESSIONID']
    return image.content

def get_user_info(request, school_id, jw_password, captcha):
    user_info = []
    param = {'j_username': school_id, 'j_password': jw_password,
            'j_captcha': captcha}
    status = authenticate_user(request, param)
    if status[0] == 200:
        STUDENT_INFO_URL = "http://jw.qdu.edu.cn/academic/showPersonalInfo.do"
        session = requests.session()
        session.cookies['JSESSIONID'] = request.session['JSESSIONID'] 
        response = session.get(STUDENT_INFO_URL)
        html = response.text
        info = UserInfo()
        info.feed(html)
        for i in info.value:
            user_info.append(i)
        user_info.append(status)
    else:
        user_info.append(status)
    return user_info

"""
identify the user that comes from university
"""
def authenticate_user(request, param):
    Authentication_URL = "http://jw.qdu.edu.cn/academic/j_acegi_security_check"
    session = requests.session()
    session.cookies['JSESSIONID'] = request.session['JSESSIONID'] 
    response = session.post(Authentication_URL, params=param)
    login = Authentication()
    login.feed(response.text)
    error = login.status.strip()
    if login.status == 'null':
        return [200, '信息验证成功']
    if u'验证码' in error:
        return [601, '验证码错误']
    if u'用户名' in login.status:
        return [602, '学号错误']
    if u'密码' in login.status:
        return [603, '密码错误']
    else:
        return [600, 'fail']
