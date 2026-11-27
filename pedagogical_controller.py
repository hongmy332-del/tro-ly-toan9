"""Pedagogical phase classifier for Trợ lý gợi mở Toán 9 (V5.3 extension).

Independent of Gemini, Streamlit and the existing S0-S3 interface progression.
Stages are tutoring intentions, not assessments of mathematical correctness.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any, Mapping, Sequence

STAGE_EXPLORING = "exploring"   # T1: seeking a solution approach
STAGE_CONCLUDED = "concluded"   # T2: claimed a conclusion, needs reasoning/checking
STAGE_WRITING = "writing"       # T3: drafting or improving the presentation
STAGES = (STAGE_EXPLORING, STAGE_CONCLUDED, STAGE_WRITING)


def _norm(text: Any) -> str:
    """Fold Vietnamese accents and normalize spaces for lightweight matching."""
    text = unicodedata.normalize("NFD", str(text or "").lower().replace("đ", "d"))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text).strip()


def _has(text: str, patterns: Sequence[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


_WRITING = (
    r"\btrinh bay\b", r"\bviet loi giai\b", r"\btrinh bay bai giai\b",
    r"\bsua loi giai\b", r"\bgop y loi giai\b", r"\bviet bai giai\b",
    r"\bviet tung cau\b", r"\bviet cau\b", r"\bviet cho chat che\b",
    r"\bcach viet\b", r"\bcach dien dat\b", r"\bsap xep lap luan\b",
    r"\bsua cach viet\b", r"\bbo cuc\b",
)
_CONCLUSION = (
    r"\bem (?:da |nghi |cho rang )?ket luan\b",
    r"\bem (?:da |nghi )?xac dinh duoc\b",
    r"\bsuy ra\b", r"\bdo do\b", r"\bvi vay\b",
    r"\btiep xuc ngoai\b", r"\btiep xuc trong\b",
    r"\bco (?:mot|1|hai|2|khong|0) diem chung\b",
    r"\bnghiem (?:la|bang)\b", r"\bket qua (?:la|bang)\b",
)
_UNCERTAIN = (
    r"\bchua biet (?:ket luan|giai|bat dau|lam the nao)\b",
    r"\bkhong biet (?:ket luan|giai|bat dau|lam the nao)\b",
    r"\bchua the ket luan\b", r"\bkhong chac\b",
    r"\bchua hieu\b",
)
_RESTART = (
    r"\bquay lai (?:tu )?dau\b", r"\bgiai lai tu dau\b",
    r"\bdoi bai\b", r"\blam bai khac\b",
)


def _student_turns(messages: Sequence[Mapping[str, Any]] | None) -> list[str]:
    turns: list[str] = []
    for m in messages or []:
        if isinstance(m, Mapping) and m.get("role") in ("student", "user"):
            txt = m.get("text", m.get("content", ""))
            if isinstance(txt, str) and txt.strip():
                turns.append(txt)
    return turns


def analyze_pedagogical_state(
    student_step: str,
    messages: Sequence[Mapping[str, Any]] | None = None,
    previous_state: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Determine tutoring phase, using only student evidence.

    `previous_state` is optional: passing it allows phase T3 to survive follow-up
    turns. A new exercise/session should pass None to reset the phase.

    Does NOT certify the student's mathematical conclusion as correct.
    """
    current = _norm(student_step)
    history = [_norm(x) for x in _student_turns(messages)]
    if current and (not history or history[-1] != current):
        history.append(current)

    previous_state = previous_state or {}
    previous_stage = previous_state.get("stage", STAGE_EXPLORING)
    if previous_stage not in STAGES:
        previous_stage = STAGE_EXPLORING

    writing_now = _has(current, _WRITING)
    claimed_now = _has(current, _CONCLUSION)
    # A claim is an assertion, not merely a quoted possibility or a question.
    uncertain_now = _has(current, _UNCERTAIN)
    claimed_any = any(_has(t, _CONCLUSION) and not _has(t, _UNCERTAIN) for t in history)
    started_draft = bool(re.search(r"\b(ta co|theo de bai|vi |suy ra|vay )\b", current))
    restarted = _has(current, _RESTART)

    if restarted:
        stage = STAGE_EXPLORING
    elif writing_now or previous_stage == STAGE_WRITING:
        stage = STAGE_WRITING
    elif (claimed_now and not uncertain_now) or previous_stage == STAGE_CONCLUDED or claimed_any:
        stage = STAGE_CONCLUDED
    else:
        stage = STAGE_EXPLORING

    # Do not infer from statement alone whether a mathematical claim is true.
    return {
        "stage": stage,
        "stage_label": {STAGE_EXPLORING: "T1 – Tìm hướng giải",
                        STAGE_CONCLUDED: "T2 – Kiểm chứng kết luận",
                        STAGE_WRITING: "T3 – Hỗ trợ trình bày"}[stage],
        "writing_requested": bool(writing_now),
        "student_claims_conclusion": bool(claimed_any or (claimed_now and not uncertain_now)),
        "student_draft_detected": bool(started_draft),
        "conclusion_verified": False,
        "reason": ("Yêu cầu hỗ trợ diễn đạt/trình bày hoặc đang ở T3" if stage == STAGE_WRITING
                   else "Đã xuất hiện kết luận cần kiểm chứng" if stage == STAGE_CONCLUDED
                   else "Đang tìm hiểu hướng giải"),
    }


def pedagogy_instruction(state: Mapping[str, Any]) -> str:
    """Short instruction for the existing Gemini system prompt.

    Treat this as advisory: existing math validation, content safety,
    and non-leaking Socratic safeguards must remain effective.
    """
    stage = state.get("stage", STAGE_EXPLORING)
    common = (
        "Chỉ dùng dữ kiện học sinh thực sự đã viết; không tự nhận là đã kiểm chứng "
        "một kết luận nếu chưa có bằng chứng toán học. Đừng hỏi lại dữ kiện hay "
        "phép tính mà học sinh vừa nêu rõ. Mỗi lượt chỉ yêu cầu MỘT thao tác mới. "
        "Không tự giải toàn bài. "
    )
    if stage == STAGE_WRITING:
        return (common +
                "TRẠNG THÁI T3 — HỖ TRỢ TRÌNH BÀY: Học sinh cần học cách diễn đạt lời giải, "
                "không cần giải lại. Ghi nhận những ý đã có, chỉ ra bố cục ngắn gọn, "
                "yêu cầu học sinh tự viết CÂU TIẾP THEO (ví dụ bắt đầu 'Ta có ...'). "
                "Nếu học sinh đã gửi một câu dự thảo, góp ý câu đó rồi yêu cầu câu kế tiếp. "
                "Không quay lại hỏi công thức/số liệu đã nêu, trừ khi học sinh làm sai. ")
    if stage == STAGE_CONCLUDED:
        return (common +
                "TRẠNG THÁI T2 — KIỂM CHỨNG: Học sinh đã NÊU một kết luận (chưa đồng nghĩa đúng). "
                "Kiểm tra cơ sở của kết luận, yêu cầu học sinh nói rõ định lý hoặc "
                "mối quan hệ quyết định; không yêu cầu tính lại dữ kiện đã đúng. "
                "Khi em yêu cầu giúp trình bày, lập tức chuyển sang T3. ")
    return (common +
            "TRẠNG THÁI T1 — TÌM HƯỚNG: Hỏi một câu ngắn giúp học sinh xác định "
            "dữ kiện hoặc kiến thức cần dùng; chỉ thêm gợi ý nhỏ nếu em mắc kẹt. ")
