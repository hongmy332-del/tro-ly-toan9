"""SQLite phục vụ thử nghiệm nội bộ. KHÔNG là kho lưu trữ bền vững trên Streamlit Cloud."""
import csv
import io
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY, student_code TEXT NOT NULL, task_id TEXT NOT NULL,
    started_at TEXT NOT NULL, updated_at TEXT NOT NULL, s0 TEXT DEFAULT '', s0_type TEXT DEFAULT 'A',
    hints_json TEXT DEFAULT '[]', attempts_json TEXT DEFAULT '[]', s2 TEXT DEFAULT '',
    s3 TEXT DEFAULT '', highest_hint INTEGER DEFAULT 0, status TEXT DEFAULT 'S0',
    support_mode TEXT DEFAULT 'Cá nhân', ai_enabled INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS assessments (
    student_code TEXT NOT NULL, phase TEXT NOT NULL,
    selfstudy REAL NOT NULL, problem_solving REAL NOT NULL, independent REAL NOT NULL,
    correct_plan INTEGER NOT NULL, detected_error INTEGER NOT NULL,
    highest_hint INTEGER, source_note TEXT DEFAULT '', updated_at TEXT NOT NULL,
    PRIMARY KEY(student_code, phase)
);
"""


def db_path() -> str:
    p = os.environ.get("DATABASE_PATH", "").strip()
    if not p:
        p = str(Path(__file__).resolve().parent / "data" / "pilot.db")
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    return p


def connect():
    db = sqlite3.connect(db_path(), timeout=15)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA busy_timeout=15000")
    db.executescript(SCHEMA)
    return db


def utcnow():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def upsert_session(obj):
    now = utcnow()
    with connect() as db:
        db.execute("""INSERT INTO sessions
            (session_id, student_code, task_id, started_at, updated_at, s0, s0_type,
              hints_json, attempts_json, s2, s3, highest_hint, status, support_mode, ai_enabled)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(session_id) DO UPDATE SET
              updated_at=excluded.updated_at, s0=excluded.s0, s0_type=excluded.s0_type,
              hints_json=excluded.hints_json, attempts_json=excluded.attempts_json,
              s2=excluded.s2, s3=excluded.s3, highest_hint=excluded.highest_hint,
              status=excluded.status, support_mode=excluded.support_mode,
              ai_enabled=excluded.ai_enabled
        """, (
            obj["session_id"], obj["student_code"], obj["task_id"],
            obj["started_at"], now, obj.get("s0", ""), obj.get("s0_type", "A"),
            json.dumps(obj.get("hints", []), ensure_ascii=False),
            json.dumps(obj.get("attempts", []), ensure_ascii=False),
            obj.get("s2", ""), obj.get("s3", ""), obj.get("highest_hint", 0),
            obj.get("status", "S0"), obj.get("support_mode", "Cá nhân"), int(bool(obj.get("ai_enabled", False))),
        ))


def all_sessions():
    with connect() as db:
        return [dict(r) for r in db.execute("SELECT * FROM sessions ORDER BY updated_at DESC").fetchall()]


def save_assessment(row):
    with connect() as db:
        db.execute("""INSERT INTO assessments
            (student_code, phase, selfstudy, problem_solving, independent,
             correct_plan, detected_error, highest_hint, source_note, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(student_code, phase) DO UPDATE SET
            selfstudy=excluded.selfstudy, problem_solving=excluded.problem_solving,
            independent=excluded.independent, correct_plan=excluded.correct_plan,
            detected_error=excluded.detected_error, highest_hint=excluded.highest_hint,
            source_note=excluded.source_note, updated_at=excluded.updated_at
        """, (
            row["student_code"], row["phase"], row["selfstudy"], row["problem_solving"],
            row["independent"], row["correct_plan"], row["detected_error"],
            row.get("highest_hint"), row.get("source_note", ""), utcnow(),
        ))


def all_assessments():
    with connect() as db:
        return [dict(r) for r in db.execute("SELECT * FROM assessments ORDER BY student_code, phase").fetchall()]


def to_csv_bytes(rows):
    if not rows:
        return "".encode("utf-8-sig")
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=list(rows[0].keys()), extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode("utf-8-sig")


def assessment_summary(rows):
    """Chỉ so sánh mã HS có cả bản ghi TRƯỚC và SAU. Không dựng số liệu."""
    items = {}
    for r in rows:
        items.setdefault(r["student_code"], {})[r["phase"]] = r
    matched = [(d["Trước"], d["Sau"]) for d in items.values() if "Trước" in d and "Sau" in d]
    if not matched:
        return None
    metrics = ["selfstudy", "problem_solving", "independent", "correct_plan", "detected_error"]
    n = len(matched)
    averages = {k: {"Trước": round(sum(a[k] for a, b in matched) / n, 3),
                     "Sau": round(sum(b[k] for a, b in matched) / n, 3)} for k in metrics}
    def band(x):
        if x < 5: return "Dưới 5"
        if x < 7: return "Từ 5 đến <7"
        return "Từ 7 trở lên"
    counts = {name: {"Trước": 0, "Sau": 0} for name in ["Dưới 5", "Từ 5 đến <7", "Từ 7 trở lên"]}
    hints = {h: {"Trước": 0, "Sau": 0} for h in range(4)}
    for before, after in matched:
        counts[band(before["independent"])]["Trước"] += 1
        counts[band(after["independent"])]["Sau"] += 1
        for phase, r in [("Trước", before), ("Sau", after)]:
            h = r.get("highest_hint")
            if h in hints:
                hints[h][phase] += 1
    valid_hint = {phase: sum(hints[h][phase] for h in hints) for phase in ["Trước", "Sau"]}
    return {"n": n, "averages": averages, "bands": counts, "hints": hints, "valid_hint": valid_hint,
            "matched_codes": [a["student_code"] for a, _ in matched]}
