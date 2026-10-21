# db.py
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()  # .env 파일의 값을 환경변수로 불러옴

def get_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ["DB_PASSWORD"],   # 비밀번호는 코드에 두지 않음
        database=os.environ.get("DB_NAME", "FleaGo"),
        charset="utf8mb4",  # 한글 및 이모지까지 지원
        cursorclass=pymysql.cursors.DictCursor  # 결과를 딕셔너리 형태로 가져옴
    )
