import sqlite3
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- 데이터베이스 설정 ---
# 파일 경로를 현재 파일 위치 기준으로 변경하여 OS에 상관없이 동작하게 합니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")
SCHEMA = os.path.join(BASE_DIR, "schema.sql")


def get_db_connection():
    """데이터베이스 연결을 생성하는 함수"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """데이터베이스 테이블을 초기화하는 함수"""
    # 앱 컨텍스트 내에서 실행되도록 보장합니다.
    with app.app_context():
        db = get_db_connection()
        with open(SCHEMA, "r", encoding="utf-8") as f:
            db.executescript(f.read())
        db.commit()
        db.close()


# --- 라우팅 ---
@app.route("/")
def homepage():
    """메인 페이지를 렌더링"""
    return render_template("index.html")


# --- API 엔드포인트 ---
@app.route("/get_events")
def get_events():
    """데이터베이스에서 모든 일정을 가져와 JSON 형태로 반환"""
    conn = get_db_connection()
    events_cursor = conn.execute(
        'SELECT id, title, start, "end", color FROM events'
    ).fetchall()
    conn.close()

    events = [dict(row) for row in events_cursor]
    return jsonify(events)


@app.route("/add_event", methods=["POST"])
def add_event():
    """새로운 일정을 데이터베이스에 추가"""
    event_data = request.get_json()
    if not event_data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # color 필드도 함께 저장하도록 SQL 수정
        cursor.execute(
            'INSERT INTO events (title, start, "end", color) VALUES (?, ?, ?, ?)',
            (
                event_data["title"],
                event_data["start"],
                event_data.get("end"),
                event_data.get("color"),  # color 값 추가
            ),
        )
        conn.commit()
        new_event_id = cursor.lastrowid
        conn.close()
        return jsonify({"status": "success", "id": new_event_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/update_event", methods=["POST"])
def update_event():
    """기존 일정의 날짜를 수정"""
    event_data = request.get_json()
    if not event_data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    try:
        conn = get_db_connection()
        # id, start, end 값을 받아와 업데이트
        conn.execute(
            'UPDATE events SET start = ?, "end" = ? WHERE id = ?',
            (event_data["start"], event_data.get("end"), event_data["id"]),
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/delete_event", methods=["POST"])
def delete_event():
    """일정을 데이터베이스에서 삭제"""
    event_data = request.get_json()
    if not event_data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM events WHERE id = ?", (event_data["id"],))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    # 지정된 폴더가 없으면 생성
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    # 스키마 파일이 없으면 생성
    if not os.path.exists(SCHEMA):
        schema_sql = """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start TEXT NOT NULL,
            "end" TEXT,
            color TEXT
        );
        """
        with open(SCHEMA, "w", encoding="utf-8") as f:
            f.write(schema_sql)

    # 앱 실행 시 데이터베이스 초기화
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
