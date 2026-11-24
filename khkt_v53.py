"""V5.3 KHKT — Bộ quy tắc gợi mở có thể giải thích, cho Bài 17 Toán 9.

Đây là nguyên mẫu có quy tắc xác định; các nhãn là dấu hiệu cần kiểm tra,
không phải chấm điểm học sinh hay xác nhận kết quả toán học.
Không gọi API và không thu thập tên/thông tin cá nhân.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any

VERSION = "5.3-khkt-prototype"


def _normalize(text: str) -> str:
    """Giảm ảnh hưởng khác biệt dấu tiếng Việt và ký hiệu toán học."""
    text = unicodedata.normalize("NFKD", str(text or "").lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return (text.replace("đ", "d").replace("−", "-").replace("–", "-")
            .replace("—", "-").replace("≤", "<=").replace("≥", ">=")
            .replace("’", "'").replace("′", "'").strip())


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", _normalize(text))


def _previous_help_count(messages: list[dict[str, Any]]) -> int:
    """Đếm các yêu cầu giúp đỡ gần đây, không tự đánh giá năng lực."""
    phrases = ("chua hieu", "khong hieu", "em chiu", "chua biet", "khong biet", "bi tac")
    total = 0
    for msg in (messages or [])[-12:]:
        if msg.get("role") not in ("student", "user"):
            continue
        if any(p in _normalize(msg.get("text", msg.get("content", ""))) for p in phrases):
            total += 1
    return total


def classify_b17(student_step: str) -> dict[str, str]:
    """Phân loại DẤU HIỆU của lời giải học sinh, không kết luận đúng/sai."""
    text = _normalize(student_step)
    compact = _compact(student_step)
    if not text:
        return {
            "code": "U00", "label": "Chưa có bước làm",
            "evidence": "Câu trả lời trống", "next_action": "Mời học sinh nêu một dữ kiện",
        }
    if any(p in text for p in (
        "chua hieu", "khong hieu", "em chiu", "chua biet", "khong biet",
        "bi tac", "khong nho", "hoi de hon", "goi y nhe",
    )):
        return {
            "code": "H01", "label": "Học sinh yêu cầu hỗ trợ",
            "evidence": "Có cụm diễn đạt chưa hiểu/chưa biết",
            "next_action": "Chia nhỏ yêu cầu hoặc đổi cách minh họa",
        }

    # Chỉ đánh dấu khi học sinh gắn điều kiện với kết luận có dấu hiệu nhầm.
    if "tiep xuc trong" in text and ("d=r+r" in compact or "d=r1+r2" in compact):
        return {
            "code": "E02", "label": "Nghi vấn nhầm điều kiện tiếp xúc trong",
            "evidence": "Viết 'tiếp xúc trong' cùng điều kiện d = tổng bán kính",
            "next_action": "Hỏi về sự khác biệt giữa tiếp xúc trong và ngoài",
        }
    if "tiep xuc ngoai" in text and (
        "d=|r-r|" in compact or "d=abs(r-r)" in compact
        or "d=|r1-r2|" in compact
    ):
        return {
            "code": "E03", "label": "Nghi vấn nhầm điều kiện tiếp xúc ngoài",
            "evidence": "Viết 'tiếp xúc ngoài' cùng điều kiện d = hiệu bán kính",
            "next_action": "Hỏi học sinh đối chiếu hình vẽ với hai khoảng cách",
        }
    if ("cat nhau" in text or "2 diem chung" in text) and any(
        frag in compact for frag in ("d<r+r", "d<r1+r2")
    ) and not any(frag in compact for frag in ("|r-r|", "|r1-r2|", "r-r<d", "r2-r1<d")):
        return {
            "code": "E01", "label": "Có thể thiếu điều kiện khi kết luận hai đường tròn cắt nhau",
            "evidence": "Kết luận cắt nhau với điều kiện d < tổng bán kính, chưa thấy xét hiệu",
            "next_action": "Hỏi điều kiện còn thiếu trước khi kết luận",
        }
    if len(text) < 10:
        return {
            "code": "U01", "label": "Bước làm quá ngắn để nhận định",
            "evidence": "Ít thông tin trong câu trả lời",
            "next_action": "Yêu cầu nêu một phép tính hoặc lập luận cụ thể",
        }
    return {
        "code": "W00", "label": "Đang lập luận, chưa phát hiện dấu hiệu đặc thù",
        "evidence": "Chưa khớp quy tắc lỗi đã định nghĩa",
        "next_action": "Hỏi học sinh kiểm tra một điều kiện từ đề",
    }


def apply_v53(
    plan: dict[str, Any],
    *,
    student_step: str,
    lesson_id: str | None,
    messages: list[dict[str, Any]] | None = None,
    phase: str = "S1",
) -> dict[str, Any]:
    """Bổ sung giải trình cho kế hoạch V5.2 mà không đổi chữ ký ask_tutor.

    An toàn với bài khác B17: không sửa mức gợi mở của V5.2.
    Trả về bản sao để tránh tác động ngoài ý muốn lên state cũ.
    """
    result = dict(plan or {})
    if lesson_id != "b17":
        result["khkt_v53"] = {
            "version": VERSION, "rule_id": "OUT_OF_SCOPE",
            "decision": "Giữ nguyên cơ chế V5.2 ở bài ngoài B17",
            "evidence": "Chưa áp dụng bộ quy tắc B17",
            "validation_status": "Chưa được giáo viên xác thực",
        }
        return result

    classification = classify_b17(student_step)
    code = classification["code"]
    previous_level = max(1, min(3, int(result.get("hint_level") or 1)))
    help_repeats = _previous_help_count(messages or [])
    chosen_level = previous_level

    if code == "H01":
        # V5.2 đã có thể tăng mức, chỉ giữ ở tối thiểu 2 khi đã lặp lại khó khăn.
        if help_repeats >= 1:
            chosen_level = max(2, chosen_level)
        strategy = "Đổi cách hỏi, dùng hình dung hoặc ví dụ đơn giản tương tự"
    elif code in {"E01", "E02", "E03"}:
        # Với nghi vấn lỗi toán học, hỏi kiểm chứng trước khi mở gợi ý lớn.
        strategy = "Hỏi kiểm tra điều kiện, tránh khẳng định học sinh sai"
    elif code in {"U00", "U01"}:
        strategy = "Hỏi làm rõ một dữ kiện hoặc bước học sinh đã thử"
    else:
        strategy = "Tiếp tục theo lập luận học sinh và hỏi một bước mới"

    if phase == "S2":
        strategy = "Yêu cầu học sinh nêu căn cứ, đối chiếu điều kiện hoặc phản biện"

    result["hint_level"] = chosen_level
    # Không ghi đè các nhận định có ngữ cảnh do V5.2 đã tạo.
    if code in {"E01", "E02", "E03"}:
        result["needs_work"] = classification["next_action"]
        result["misconception"] = classification["label"]
    elif code == "H01" and not result.get("needs_work"):
        result["needs_work"] = classification["next_action"]

    result["khkt_v53"] = {
        "version": VERSION,
        "rule_id": code,
        "observed_signal": classification["label"],
        "evidence": classification["evidence"],
        "decision": strategy,
        "hint_level": chosen_level,
        "phase": phase,
        "previous_help_turns": help_repeats,
        "validation_status": "Giả thuyết cần giáo viên kiểm chứng; không phải điểm số",
    }
    return result
