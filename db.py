import datetime
import random
import sqlite3
import string

DB_NAME = "sociolab.db"


def get_conn():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS library_resources ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "title TEXT NOT NULL, "
        "author TEXT NOT NULL, "
        "res_type TEXT NOT NULL, "
        "specialty TEXT NOT NULL, "
        "pub_year TEXT NOT NULL, "
        "apa_citation TEXT, "
        "source_url TEXT)"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS knowledge_articles ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "title TEXT NOT NULL, "
        "category TEXT NOT NULL, "
        "author TEXT NOT NULL, "
        "summary TEXT NOT NULL, "
        "content TEXT NOT NULL, "
        "pub_date TEXT NOT NULL)"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS observatory_data ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "domain TEXT NOT NULL, "
        "title TEXT NOT NULL, "
        "indicator_val TEXT NOT NULL, "
        "data_source TEXT NOT NULL, "
        "data_year TEXT NOT NULL, "
        "methodology TEXT NOT NULL)"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS researchers ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "full_name TEXT NOT NULL, "
        "academic_rank TEXT NOT NULL, "
        "institution TEXT NOT NULL, "
        "specialty TEXT NOT NULL, "
        "interests TEXT NOT NULL, "
        "contact_link TEXT, "
        "approved INTEGER DEFAULT 0)"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS academy_courses ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "title TEXT NOT NULL, "
        "track TEXT NOT NULL, "
        "format TEXT NOT NULL, "
        "schedule_info TEXT NOT NULL, "
        "description TEXT NOT NULL)"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS projects ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "title TEXT NOT NULL, "
        "status TEXT NOT NULL, "
        "partners TEXT NOT NULL, "
        "summary TEXT NOT NULL)"
    )

    cur.execute(
        "CREATE TABLE IF NOT EXISTS office_requests ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "tracking_code TEXT UNIQUE NOT NULL, "
        "client_name TEXT NOT NULL, "
        "client_email TEXT NOT NULL, "
        "client_role TEXT NOT NULL, "
        "req_type TEXT NOT NULL, "
        "details TEXT NOT NULL, "
        "status TEXT DEFAULT 'قيد الدراسة المنهجية', "
        "created_at TEXT NOT NULL)"
    )

    conn.commit()
    conn.close()


def generate_tracking_code():
    chars = string.ascii_uppercase + string.digits
    suffix = "".join(random.choices(chars, k=6))
    return f"SL-{suffix}"


def add_office_request(name, email, role, req_type, details):
    conn = get_conn()
    cur = conn.cursor()
    code = generate_tracking_code()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cur.execute(
        "INSERT INTO office_requests "
        "(tracking_code, client_name, client_email, client_role, req_type, details, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (code, name, email, role, req_type, details, now_str),
    )
    conn.commit()
    conn.close()
    return code


def get_request_by_code(code):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM office_requests WHERE tracking_code = ?",
        (code.strip().upper(),),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def fetch_all(table_name, order_by="id DESC"):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name} ORDER BY {order_by}")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def delete_record(table_name, record_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table_name} WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
