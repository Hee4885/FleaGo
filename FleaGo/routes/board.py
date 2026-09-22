from flask import Blueprint, render_template
from db import get_connection
import pymysql

bp = Blueprint('board', __name__, url_prefix='/board')

# 이벤트 게시판 (전체 이벤트 목록)
@bp.route('/events')
def event_board():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT e.*, c.channel_name, c.profile_image
        FROM event e
        JOIN channel c ON e.admin_name = c.admin_name
        ORDER BY e.start_date DESC
    """)
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('eventBoard.html', events=events)


# 이벤트 상세보기
@bp.route('/read_event/<int:event_id>')
def read_event(event_id):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 이벤트 정보
    cursor.execute("SELECT * FROM event WHERE event_id=%s", (event_id,))
    event = cursor.fetchone()

    # 담당자 정보
    cursor.execute("SELECT * FROM event_manager WHERE event_id=%s", (event_id,))
    manager = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('readEvent.html', event=event, manager=manager)


# 부스 상세보기
@bp.route('/read_booth/<int:event_id>')
def read_booth(event_id):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 이벤트 정보 (부스 위에 이벤트 제목 보여주기 위함)
    cursor.execute("SELECT * FROM event WHERE event_id=%s", (event_id,))
    event = cursor.fetchone()

    # 해당 이벤트 부스 정보
    cursor.execute("SELECT * FROM booth WHERE event_id=%s ORDER BY booth_id ASC", (event_id,))
    booths = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('readBooth.html', event=event, booths=booths)
