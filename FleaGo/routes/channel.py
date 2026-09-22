from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
from db import get_connection
import pymysql

bp = Blueprint('channel', __name__, url_prefix='/channel')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 트레일링 슬래시 없이 정의하거나 strict_slashes=False
@bp.route('', methods=['GET', 'POST'], strict_slashes=False)
def channel_dashboard():
    admin_name = session.get('user_id')
    if not admin_name:
        flash("로그인이 필요합니다.")
        return redirect(url_for('auth.login_page'))

    if request.method == "POST":
        channel_name = request.form.get('channelName')
        file = request.files.get('channelProfile')

        if file is None or not allowed_file(file.filename):
            flash("이미지 파일을 올려주세요.")
            return render_template('channelFail.html') 

        filename = secure_filename(file.filename)
        upload_dir = os.path.join('static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        upload_path = os.path.join(upload_dir, filename)

        try:
            file.save(upload_path)
        except Exception as e:
            flash(f"파일 저장 실패: {e}")
            return render_template('channelFail.html')

        try:
            conn = get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            cursor.execute("SELECT * FROM channel WHERE channel_name=%s", (channel_name,))
            if cursor.fetchone():
                flash("이미 존재하는 채널명입니다.")
                return render_template('channelFail.html')

            cursor.execute(
                "INSERT INTO channel (admin_name, channel_name, profile_image) VALUES (%s, %s, %s)",
                (admin_name, channel_name, filename)
            )
            conn.commit()
            flash("채널 생성 성공!")
            return render_template('channelSuccess.html')

        except pymysql.MySQLError as e:
            flash(f"DB 오류: {e}")
            return render_template('channelFail.html')
        finally:
            cursor.close()
            conn.close()

    return render_template('channelPosting.html')


@bp.route('/event/<int:channel_id>')
def event_info(channel_id):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM channel WHERE channel_id=%s", (channel_id,))
    channel = cursor.fetchone()
    cursor.close()
    conn.close()

    if channel:
        return render_template('eventInfo.html', channel=channel)
    else:
        flash("채널 정보가 없습니다.")
        return redirect(url_for('channel.channel_dashboard'))
