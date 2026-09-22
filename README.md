# FleaGo (플리고)

Flask + 정적 HTML/CSS/JS로 구성된 소규모 웹 프로젝트 — 이벤트(부스) 및 공지(게시판)용 프론트엔드 템플릿을 로컬에서 제공하는 연습/포트폴리오용 프로젝트입니다.

Flask의 `send_from_directory`를 사용해 `FleaGo/html`에 있는 정적 파일을 서빙합니다.

---

## 한 줄 요약

Flask로 정적 웹 페이지(HTML/CSS/JS)를 서빙하는 이벤트·부스 정보 사이트 템플릿 — 메인 페이지, 로그인/회원가입, 게시판 및 부스 페이지 포함.

---

## 프로젝트 소개

이 저장소는 플리마켓/행사 홍보용 웹 페이지를 구성하는 연습 프로젝트입니다. 실제 서비스처럼 회원가입, 로그인, 역할 선택, 채널 생성, 행사 게시판, 부스 정보 등록 등의 흐름을 구현해 보았고, 프론트엔드는 정적 HTML/CSS/JS 기반으로 구성되어 있습니다.

특히 현재 구조는 Flask 앱이 `routes`를 통해 기능별로 분리되어 있고, 각 화면을 템플릿으로 렌더링하는 방식입니다. 파일 업로드 기능과 MySQL 연결도 포함되어 있어, 백엔드와 프론트엔드가 함께 구성된 소형 웹 애플리케이션 형태를 띱니다.

---

## 주요 기능

- 정적 페이지 서빙 (메인, 로그인, 회원가입, 이벤트/부스 상세 및 목록)
- Flask 엔트리포인트 (`send_from_directory` 및 템플릿 렌더링)로 HTML 제공
- HTML / CSS / JavaScript 기반 프론트엔드 템플릿
- 이미지, 폰트, 스크립트, 업로드 파일 등 정적 자산 관리
- MySQL 연동 기반 회원/채널/행사/부스 데이터 처리
- 로그인 후 관리자/사용자 역할 선택 기능
- 쇼핑몰형 행사 채널 생성 및 행사 게시판 기능
- 연습용 Frontend / Backend 디렉터리 포함
- 로컬 개발용 `.venv` 포함 (권장: `.gitignore`로 제외)

---

## 사용된 기술

- 언어 : Python 3.x
- 프레임워크 : Flask
- 템플릿 엔진 : Jinja2
- 데이터베이스 : MySQL
- DB 드라이버 : PyMySQL
- 프론트엔드 : HTML, CSS, JavaScript
- 정적 자산 : Image, Font, Uploads
- 개발 도구 : Git / GitHub

---

## 저장소 구조 (요약)

```text
.
├─ .venv/                       # (커밋된 가상환경 - 일반적으로는 제외)
├─ FleaGo/
│  ├─ app.py                    # Flask 앱 생성 및 라우트 등록
│  ├─ db.py                     # MySQL 연결 설정
│  ├─ routes/
│  │  ├─ auth.py                # 회원가입 / 로그인 / 역할 선택
│  │  ├─ event.py               # 행사 정보 관리
│  │  ├─ booth.py               # 부스 정보 추가 및 목록
│  │  ├─ board.py               # 이벤트 게시판 및 상세
│  │  └─ channel.py             # 채널 생성 및 업로드
│  ├─ templates/
│  │  ├─ index.html
│  │  ├─ login.html
│  │  ├─ signUp.html
│  │  ├─ role.html
│  │  ├─ eventBoard.html
│  │  ├─ readEvent.html
│  │  ├─ boothInfo.html
│  │  ├─ readBooth.html
│  │  ├─ channelPosting.html
│  │  ├─ channelSuccess.html
│  │  └─ channelFail.html
│  ├─ static/
│  │  ├─ css/
│  │  ├─ js/
│  │  ├─ img/
│  │  ├─ font/
│  │  └─ uploads/
│  ├─ html/
│  │  └─ (정적 HTML/에셋 보관용 디렉터리)
│  ├─ Lib/
│  ├─ Scripts/
│  ├─ venv/
│  ├─ pyvenv.cfg
│  ├─ pip-selfcheck.json
│  └─ __pycache__/
├─ venv/
├─ 연습/
│  ├─ backend/
│  └─ frontend/
└─ README.md
```

---

## 실행 방법

Python 3.x 설치

가상환경 권장

```bash
python -m venv .venv
```

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Flask 및 PyMySQL 설치

```bash
pip install flask pymysql
```

애플리케이션 실행

```bash
cd FleaGo
python app.py
```

기본 실행 주소

```text
http://127.0.0.1:5000
```

---

## 주요 동작 흐름

1. 사용자가 메인 페이지에서 로그인 또는 회원가입 진입
2. `auth.py`에서 회원 정보 확인 및 세션 저장
3. 사용자가 관리자/일반 사용자 역할 선택
4. 관리자는 채널 생성 및 행사 정보 등록
5. 행사 등록 후 부스 정보 추가 및 게시판에 노출
6. 사용자 입장에서 행사 리스트와 상세 페이지 조회 가능

---

## 주의 사항

- Python 3.x 및 Flask, PyMySQL 설치가 필요합니다.
- 프로젝트 루트에서 실행하는 것을 권장합니다.
- `.venv` 또는 `venv`는 보통 저장소에 포함하지 않고 `.gitignore`로 관리하는 것이 좋습니다.
- MySQL 연결 정보는 `FleaGo/db.py`에 하드코딩되어 있으므로 보안상 별도 환경 변수 관리가 필요합니다.
- `secret_key`도 코드에 직접 넣어져 있으므로 실제 서비스에서는 환경 변수로 분리하는 것이 좋습니다.
- 현재 앱은 개발용 `debug=True` 상태이므로 운영 환경에서 바로 사용하지 않는 것이 좋습니다.

---

## 개발 메모

- Flask 앱은 `routes` 디렉터리의 기능별 Blueprint로 구성되어 있습니다.
- 정적 파일은 `FleaGo/templates`와 `FleaGo/static`을 중심으로 제공됩니다.
- `FleaGo/html` 폴더가 별도로 남아 있으나 현재 앱의 실제 실행 구조는 `templates`와 `static` 기반으로 동작합니다.
- 대체로 학습/포트폴리오용 프로젝트로서 프론트엔드 템플릿과 백엔드 연결 흐름을 익히기 좋은 구조입니다.
- 추후에는 사용자 권한 검증, 비밀번호 해시 처리, 에러 처리, 테스트 코드, 배포 설정 등으로 발전시킬 수 있습니다.
