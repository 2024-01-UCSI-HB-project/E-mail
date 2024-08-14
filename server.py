from flask import Flask, render_template, redirect, url_for, request, session, flash
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션을 위한 시크릿 키 설정

# 임시 사용자 데이터베이스 (실제 애플리케이션에서는 데이터베이스를 사용하세요)
users = {'admin': 'admin', 'user': 'user'}


# 기본 라우트: 로그인 페이지
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 인증
        if username in users and users[username] == password:
            session['user'] = username
            if username == 'admin':
                return redirect(url_for('admin_page'))
            else:
                return redirect(url_for('user_page'))
        else:
            flash("Invalid credentials")

    return render_template('login.html')


# 가입 라우트
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash("Username already exists")
        else:
            users[username] = password
            flash("Registration successful")
            return redirect(url_for('login'))

    return render_template('register.html')


# 로그아웃 라우트
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# User 페이지 라우트
@app.route('/user', methods=['GET', 'POST'])
def user_page():
    if 'user' in session and session['user'] == 'user':
        if request.method == 'POST':
            toner_type = request.form['toner_type']
            quantity = request.form['quantity']
            # 실제 애플리케이션에서는 데이터베이스에 이 정보를 저장하거나 이메일로 전송하는 등 처리를 해야 합니다.
            flash(f'Toner request submitted: {toner_type}, Quantity: {quantity}')
        return render_template('user.html')
    return redirect(url_for('login'))


# Admin 페이지 라우트
@app.route('/admin')
def admin_page():
    if 'user' in session and session['user'] == 'admin':
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))


@app.route("/admin", methods=['POST'])
def send_mail():
    # status=request.form['select']

    smtp = smtplib.SMTP('smtp.gmail.com', 587)

    smtp.ehlo()

    smtp.starttls()

    # 보낼 계정
    smtp.login('20221110@edu.hanbat.ac.kr', 'dcbv eokd guhw nttn')

    # 메시지 전송
    msg = request.form['select']
    if msg == "승인":
        send_msg = MIMEText("승인")
        send_msg['Subject'] = "승인"
        # msg=MIMEText(f"선택된 상태: {status}") # 내용
        # msg['Subject']=f'제목: {status} 상태 확인' # 제목
        # 보내는 사람 이메일 / 받는 사람 이메일
        smtp.sendmail('20221095@edu.hanbat.ac.kr', 'luonj@naver.com', send_msg.as_string())
    elif msg == "보류":
        send_msg = MIMEText("보류")
        send_msg['Subject'] = "보류"
        smtp.sendmail('20221095@edu.hanbat.ac.kr', 'luonj@naver.com', send_msg.as_string())
    elif msg == "재고":
        send_msg = MIMEText("재고")
        send_msg['Subject'] = "재고"
        smtp.sendmail('20221095@edu.hanbat.ac.kr', 'luonj@naver.com', send_msg.as_string())

    # 종료
    smtp.quit()

    return render_template('approval.html')


# Dashboard 페이지 라우트 (Admin만 접근 가능)
@app.route('/dashboard')
def dashboard():
    if 'user' in session and session['user'] == 'admin':
        return render_template('dashboard.html')
    return redirect(url_for('login'))


# Application Approval 페이지 라우트 (Admin만 접근 가능)
@app.route('/approval')
def approval_page():
    if 'user' in session and session['user'] == 'admin':
        return render_template('approval.html')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)