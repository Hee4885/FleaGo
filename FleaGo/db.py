# db.py
import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",       # MySQL 계정
        password="07090613", # MySQL 비밀번호
        database="FleaGo", # DB 이름
        charset="utf8mb4", # 한글 및 이모지까지 지원
        cursorclass=pymysql.cursors.DictCursor # pymysql에서 쿼리 실행 시 어떤 형태로 가져오는지에 대한 옵션
    )

# 기본값(Cursor) : 결과를 튜플(tuple) 형태로 가져옴
# DictCursor : 결과를 딕셔너리(dict) 형태로 가져옴