# Flask : python으로 웹 서버 만들기 위함, 
# flask-cors : 프론트와 다른 폴더/ 도메인에서 통신하게 함

from flask import Flask, request, jsonify
from flask_cors import CORS #프론트와 통신 허용을 위해서

app = Flask(__name__) #Flask 앱 객체 생성 -> 서버 실행, 라우팅 처리 등 기능 관리
CORS(app) # 프론트에서 다른 도메인/포트로 요청해도 허용되도록 설정

#루트 페이지 라우트
@app.route("/")
def index():
    return "서버 실행 중. /calulate로 POST 요청을 보내세요."

#favicon.ico 처리
@app.route("/favicon.ico")
def favicon():
    return "",204

@app.route("/calculate", methods = ["POST"]) #/calculate URL로 POST 요청이 들어오면 calculate() 함수 실행
def calculate():
    data = request.get_json() #요청으로 들어온 JSON 데이터를 Python 딕셔너리 형태로 변환
    
    #JSON 에서 받은 num1,num2 값을 문자열에서 숫자로 변환
    n1 = float(data["num1"])
    n2 = float(data["num2"])

    #JSON에서 연산자 값 가져오기
    op = data["operator"]

    #연산자에 따라 실제 계산 수행 -> result에 저장
    if op == "+" : result = n1 + n2
    elif op == "-" : result = n1 - n2
    elif op == "*" : result = n1 * n2
    elif op == "/" : result = n1 / n2
    elif op == "%" : result = n1 % n2

    #연산자가 잘못된 경우 JSON 으로 에러 반환, HTTP 상태 코드 400
    else : return jsonify({"error":"잘못된 연산자"},400)

    #계산 결과를 JSON 형태로 프론트에 반환
    return jsonify({"result" : result})

#이 파일을 직접 실행하면 Flask 서버를 시작
#debug=True -> 코드 수정 시 자동 재시작 + 에러 메시지 상세 출력
if __name__ == "__main__" :
    app.run(debug=True)






