import io

from flask import Flask, render_template, request, send_file, session

from registrar import factory

app = Flask(__name__)
app.secret_key = 'developer is very cool'


@app.route('/')
def index():
    return render_template('index.html', index='Ya')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 存在验证码使用GET请求获取验证码
    if request.method == 'GET':
        school = request.values.get('school')

        if school == None:
            return render_template('index.html')

        u = factory.Factory().get_object(school)
        ret = u.get_captcha_base64()

        session['state'] = u.get_state()
        session['school'] = school

        if ret == 'TimeOut':
            return render_template('error.html', info='超时,请检查教务系统是否开放')
        elif ret == 'UnknownError':
            return render_template('error.html', info='发生未知错误')
        else:
            return render_template('login.html', captcha_base64=ret, school=school)

    # 不存在验证码直接发送POST请求
    else:
        school = session['school']
        u = factory.Factory().get_object(school)
        u.set_state(session['state'])

        username = request.form.get('username')
        password = request.form.get('password')
        captcha_text = request.form.get('captcha_text')

        date = request.form.get('date')

        u.start_time(date)

        ret = u.get_classtable(username, password, captcha_text)

        if ret == 'TimeOut':
            return render_template('error.html', info='超时,请检查教务系统是否开放')
        elif ret == 'UnknownError':
            return render_template('error.html', info='发生未知错误')
        elif ret == 'CaptchaError':
            return render_template('error.html', info='请输入正确的信息')

        else:
            return render_template('return.html', ret=ret)


if __name__ == '__main__':
    app.run()
