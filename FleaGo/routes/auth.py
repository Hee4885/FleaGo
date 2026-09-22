from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from db import get_connection
import pymysql

bp = Blueprint('auth', __name__)

class UserAuth:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect_db(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def close_db(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()

    def is_duplicate_id(self, user_id):
        self.cursor.execute("SELECT * FROM member WHERE userName=%s", (user_id,))
        return self.cursor.fetchone() is not None

    def create_user(self, user_id, password, email):
        self.cursor.execute(
            "INSERT INTO member (userName, password, email, role) VALUES (%s,%s,%s,'user')",
            (user_id, password, email)
        )
        self.conn.commit()

    def validate_login(self, user_id, password):
        self.cursor.execute("SELECT * FROM member WHERE userName=%s AND password=%s", (user_id, password))
        return self.cursor.fetchone()


@bp.route('/signUp', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        user_id = request.form.get('userId')
        password = request.form.get('password')
        re_password = request.form.get('rePassword')
        email = request.form.get('email')
        if password != re_password:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template('signUp.html')
        auth = UserAuth()
        try:
            auth.connect_db()
            if auth.is_duplicate_id(user_id):
                flash("이미 사용중인 아이디입니다.")
                return render_template('signUp.html')
            auth.create_user(user_id, password, email)
            flash("회원가입 완료!")
            return redirect(url_for('auth.login_page'))
        except pymysql.MySQLError as e:
            flash(f"DB 오류 발생: {e}")
            return render_template('signUp.html')
        finally:
            auth.close_db()
    return render_template('signUp.html')


@bp.route('/login', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        user_id = request.form.get('userId')
        password = request.form.get('password')
        auth = UserAuth()
        try:
            auth.connect_db()
            user = auth.validate_login(user_id, password)
            if user:
                session['user_id'] = user['userName']  # 세션에 저장
                return render_template('role.html', user_id=user['userName'])

            else:
                flash("아이디 또는 비밀번호가 잘못되었습니다.")
                return render_template('login.html')
        except pymysql.MySQLError as e:
            flash(f"DB 오류 발생: {e}")
            return render_template('login.html')
        finally:
            auth.close_db()
    return render_template('login.html')


@bp.route('/role', methods=['GET','POST'])
def role_selection():
    if request.method == 'POST':
        selected_role = request.form.get('role')
        user_id = request.form.get('userId')
        auth = UserAuth()
        try:
            auth.connect_db()
            auth.cursor.execute("UPDATE member SET role=%s WHERE userName=%s", (selected_role, user_id))
            auth.conn.commit()
            flash(f"권한이 '{selected_role}'로 변경되었습니다.")
            if selected_role == 'admin':
                auth.cursor.execute("SELECT * FROM channel WHERE admin_name=%s", (user_id,))
                channel = auth.cursor.fetchone()
                if channel:
                    return render_template('eventInfo.html', channel=channel)
                return redirect(url_for('channel.channel_dashboard'))
            else:
                return redirect(url_for('board.event_board'))
        except pymysql.MySQLError as e:
            flash(f"DB 오류 발생: {e}")
            return render_template('role.html')
        finally:
            auth.close_db()
    return render_template('role.html')
