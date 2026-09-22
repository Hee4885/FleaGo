from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_connection
import pymysql

bp = Blueprint('booth', __name__, url_prefix='/booth')

# 부스 입력 + 기존 부스 목록 페이지
@bp.route('/info/<int:event_id>', methods=['GET'])
def booth_info(event_id):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM booth WHERE event_id=%s ORDER BY booth_id ASC", (event_id,))
        booths = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return render_template('boothInfo.html', event_id=event_id, booths=booths)


# 부스 추가 POST (URL과 템플릿의 action이 일치하도록 '/post/<event_id>'로 정의)
@bp.route('/post/<int:event_id>', methods=['POST'])
def post_booth(event_id):
    # 폼 필드 수집 (필요한 항목들을 모두 받음)
    booth_name = request.form.get('boothName', '').strip()
    location = request.form.get('location', '').strip()
    open_time = request.form.get('openTime') or None
    close_time = request.form.get('closeTime') or None
    product_name = request.form.get('productName', '').strip()
    use_type = request.form.get('useType', '').strip()
    price = request.form.get('price')

    # 간단한 유효성 검사
    if not booth_name:
        flash("부스명을 입력하세요.")
        return redirect(url_for('booth.booth_info', event_id=event_id))

    # price는 비어있으면 NULL, 있으면 정수로 변환 시도
    if price == '' or price is None:
        price_val = None
    else:
        try:
            price_val = int(price)
        except ValueError:
            flash("가격은 숫자만 입력하세요.")
            return redirect(url_for('booth.booth_info', event_id=event_id))

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO booth (event_id, name, location, open_time, close_time, product_name, use_type, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (event_id, booth_name, location, open_time, close_time, product_name, use_type, price_val))
        conn.commit()
        flash("부스 정보가 추가되었습니다.")
        # 추가 후 같은 이벤트의 부스 목록 페이지로 리다이렉트
        return redirect(url_for('booth.booth_info', event_id=event_id))
    except pymysql.MySQLError as e:
        conn.rollback()
        flash(f"DB 오류 발생: {e}")
        return redirect(url_for('booth.booth_info', event_id=event_id))
    finally:
        cursor.close()
        conn.close()


# 개별 부스 상세보기 (선택 사항)
@bp.route('/detail/<int:booth_id>', methods=['GET'])
def booth_detail_page(booth_id):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM booth WHERE booth_id=%s", (booth_id,))
        booth = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if not booth:
        flash("해당 부스가 존재하지 않습니다.")
        # 존재하지 않으면 홈(혹은 보드)로 이동
        return redirect(url_for('board.event_board'))
    return render_template('boothDetail.html', booth=booth)
