from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from db import get_connection
import pymysql

bp = Blueprint('event', __name__, url_prefix='/event')

@bp.route('/eventInfo', methods=['GET'])
def event_info_page():
    user_id = session.get('user_id')
    if not user_id:
        flash("로그인이 필요합니다.")
        return redirect(url_for('auth.login_page'))

    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM event WHERE admin_name=%s ORDER BY event_id DESC LIMIT 1", (user_id,))
    event = cursor.fetchone()
    manager = None
    if event:
        cursor.execute("SELECT * FROM event_manager WHERE event_id=%s LIMIT 1", (event['event_id'],))
        manager = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('eventInfo.html', event=event, manager=manager)

# @bp.route('/posting', methods=['POST'])
# def post_event():
#     user_id = session.get('user_id')
#     if not user_id:
#         flash("로그인이 필요합니다.")
#         return redirect(url_for('auth.login_page'))

#     title = request.form.get('eventTitle')
#     intro = request.form.get('eventDesc')
#     notice = request.form.get('notice')
#     main_event = request.form.get('mainEvent')
#     start_date = request.form.get('startDate')
#     start_time = request.form.get('startTime')
#     end_date = request.form.get('endDate')
#     end_time = request.form.get('endTime')
#     manager_name = request.form.get('managerName')
#     manager_email = request.form.get('managerEmail')
#     manager_phone = request.form.get('managerPhone')

#     conn = get_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute("""
#             INSERT INTO event (title, admin_name, intro, notice, start_date, end_date, start_time, end_time, main_event)
#             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
#         """, (title, user_id, intro, notice, start_date, end_date, start_time, end_time, main_event))
#         conn.commit()
#         event_id = cursor.lastrowid

#         cursor.execute("""
#             INSERT INTO event_manager (event_id, name, email, phone)
#             VALUES (%s,%s,%s,%s)
#         """, (event_id, manager_name, manager_email, manager_phone))
#         conn.commit()

#         flash("행사 정보와 담당자 정보가 저장되었습니다.")
#         return redirect(url_for('board.event_board'))

#     except pymysql.MySQLError as e:
#         flash(f"DB 오류 발생: {e}")
#         return render_template('eventInfo.html', event=None, manager=None)
#     finally:
#         cursor.close()
#         conn.close()

@bp.route('/post_event', methods=['POST'])
def post_event():
    user_id = session.get('user_id')
    if not user_id:
        flash("로그인이 필요합니다.")
        return redirect(url_for('auth.login_page'))

    eventTitle = request.form['eventTitle']
    eventDesc = request.form['eventDesc']
    # ... 나머지 이벤트 정보 저장 코드

    # DB에 이벤트 저장 후 이벤트 ID 가져오기
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
    "INSERT INTO event (title, admin_name, intro, notice, start_date, start_time, end_date, end_time, main_event) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (eventTitle, user_id, eventDesc, request.form['notice'],
     request.form['startDate'], request.form['startTime'],
     request.form['endDate'], request.form['endTime'],
     request.form['mainEvent'])
    )

    conn.commit()
    event_id = cursor.lastrowid
    cursor.close()
    conn.close()

    # 부스 입력 페이지로 이동
    return redirect(url_for('booth.booth_info', event_id=event_id))

