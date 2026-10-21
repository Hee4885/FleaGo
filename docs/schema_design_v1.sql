-- =====================================================================
-- FleaGo DB 설계 기록 (v1 설계안)
--
-- 개발 초기에 작성한 테이블 설계 스크립트입니다.
--   * 회원(members) → 채널(channels) → 행사(events) → 부스(booths)를
--     외래키와 ON DELETE CASCADE로 연결해, 상위 데이터를 지우면
--     하위 데이터가 함께 정리되도록 설계했습니다.
--   * 처음에는 삭제 규칙을 몰라 테이블을 지우고 다시 만드는 일을 반복했고,
--     그 과정을 이 스크립트(초기화 절차 포함)로 기록했습니다.
--
-- ※ 현재 앱 코드(FleaGo/routes/*.py)는 이후 수정된 테이블 구조
--   (member, channel, event, event_manager, booth)를 사용합니다.
--   이 파일은 설계 과정을 보여 주는 기록이며, 현재 코드와 테이블/컬럼
--   이름이 다릅니다.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS fleago;
USE fleago;


-- 1) 회원 테이블 (members)
CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------

-- 2) 채널 테이블 (channels)
CREATE TABLE IF NOT EXISTS channels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    channel_name VARCHAR(100) NOT NULL,
    channel_image VARCHAR(400),   -- 업로드된 이미지 경로 (행사 채널 이미지)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_channel_member
        FOREIGN KEY (member_id) REFERENCES members(id)
        ON DELETE CASCADE
);

-- --------------------------------------------------------

-- 3) 행사 테이블 (events)
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    -- 참조할 테이블 튜플 아이디
    channel_id INT NOT NULL,
    event_name VARCHAR(100) NOT NULL,

    event_date_start DATE NOT NULL,        -- 행사 날짜 (시작)
    event_date_end DATE NOT NULL,          -- 행사 날짜 (끝)

    event_start TIME NOT NULL,             -- 행사 시작 시간
    event_end TIME NOT NULL,               -- 행사 종료 시간

    poster_image VARCHAR(400),             -- 업로드된 이미지 경로 (행사 포스터)

    main_event VARCHAR(255),               -- 주요 이벤트
    place VARCHAR(255),                    -- 행사 장소

    manager_name VARCHAR(100) NOT NULL,    -- 관리자 이름
    manager_email VARCHAR(100) NOT NULL,   -- 관리자 이메일
    manager_phone VARCHAR(20),             -- 관리자 연락처

    description TEXT,                      -- 행사 소개글
    notice TEXT,                           -- 안내 및 공지

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_event_channel
        FOREIGN KEY (channel_id) REFERENCES channels(id)
        ON DELETE CASCADE
);

-- --------------------------------------------------------

-- 4) 부스 테이블 (booths)
CREATE TABLE IF NOT EXISTS booths (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,

    booth_name VARCHAR(100) NOT NULL,      -- 부스명
    booth_place VARCHAR(255) NOT NULL,     -- 장소
    booth_start TIME NOT NULL,             -- 운영 시작 시간
    booth_end TIME NOT NULL,               -- 운영 종료 시간

    product_name VARCHAR(255),             -- 대표 상품명
    product_image VARCHAR(400),            -- 업로드된 이미지 경로 (상품 이미지)
    product_use VARCHAR(255),              -- 상품 용도
    product_price INT,

    product_explain TEXT,                  -- 상품 설명글

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_booth_event
        FOREIGN KEY (event_id) REFERENCES events(id)
        ON DELETE CASCADE
);


-- =====================================================================
-- [참고] 개발 중 사용한 확인·초기화 절차
-- 실수로 실행되지 않도록 주석으로 남겨 둡니다.
-- =====================================================================
-- DESC booths;
-- SELECT * FROM booths;
--
-- -- 테이블 초기화: 외래키 검사를 잠시 끄고 비운 뒤 다시 켬
-- SET FOREIGN_KEY_CHECKS = 0;
-- TRUNCATE TABLE booths;
-- SET FOREIGN_KEY_CHECKS = 1;
