import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template
from routes import auth, event, booth, board, channel # 각 기능 모듈 import

app = Flask(__name__)

# 세션/flash 사용을 위한 secret key 설정
app.secret_key = os.environ["SECRET_KEY"]  # 비밀값은 .env에서 불러옴

# 기본 페이지
@app.route("/")
def index():
    return render_template("index.html")  # 처음 실행 시 기본 페이지만 보여줌

# 각 기능 모듈 블루프린트 등록 (블루프린트 : 기능별로 라우트와 로직을 모듈화)
app.register_blueprint(auth.bp)    # 로그인/회원가입 처리
app.register_blueprint(event.bp)   # 행사 관련 처리
app.register_blueprint(booth.bp)   # 부스 관련 처리
app.register_blueprint(board.bp)   # 게시판 관련 처리
app.register_blueprint(channel.bp)   # 채널 관련 처리


if __name__ == "__main__" :
    app.run(debug=True) #수정할 때 자동 재시작, 에러 표시


    # 행사 안에 부스 정보들도 있어야 하는데 궁금한 거는 부스들은 관리자 모드일 경우 추가하기 버튼 누르면 추가 가능한데 추가해도 추가한 부스들 정보를 나중에 또 수정할 수 있어야 한단 말이야



    #로그인 끝나고 관리자 할지 참가자할지 선택하고 여기서 user 테이블에 정보 저장

    # 관리자일 경우 role.html로 보여주고 그곳에서 행사 게시(채널 개설)을 한다 이것은 추후에 event board에서 보여줄 채널 이미지와 이름, 행사 정보를 입력(행사 카테고리(선택형), 행사 기간 입력) 이후에 행사 개설 완료

    # 관리자 모드이므로 행사 개설이 끝나면 바로 posting event 화면으로 전환
    # 이 화면에서는 행사를 소개하는데 행사 소개는 (행사 홍보 글, 공지/안내 글, 담당자 정보 입력, 행사 정보(처음에 채널 게시할 때 넘은 행사 정보가 임시로 입력되어만 있고 다시 작성 가능, 일시, 행사 시간, 컨셉(카테고리),주요 행사(이벤트같은 큰 특정 시간 이벤트))