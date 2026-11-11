"""Bộ điều phối gợi ý. AI chỉ hỗ trợ sinh *câu hỏi*, không đánh giá chính thức."""
import re

SOLUTION_REQUEST = re.compile(r"(giải hộ|giải giúp|đáp án|lời giải đầy đủ|làm hộ|cho kết quả|ra bao nhiêu|trả lời luôn)", re.I)


def classify_error(task_id: str, content: str) -> str:
    t = content.lower().replace(" ", "")
    if any(k in t for k in ["khôngbiết", "chưabiết", "bí", "khônghiểu", "bítắc", "bắttừđâu"]):
        return "stuck"
    if task_id == "circles":
        if "cắtnhau" in t or "giao" in t or "d<" in t or "nhỏhơn" in t:
            return "only_sum"
        if "tiếpxúc" in t or "trùngnhau" in t:
            return "conclusion"
    if task_id == "radicals" and any(k in t for k in ["√(a+b)", "căncủatổng", "√9+√16"]):
        return "sqrt_sum"
    if task_id == "quadratic" and ("x=2" in t or "mộtnghiệm" in t):
        return "one_root"
    if task_id == "system" and ("đổidấu" in t or "cộngsai" in t):
        return "sign_error"
    return "general"


def curated_hint(task, level: int, error_type: str) -> str:
    if level == 1 and error_type in task.get("focus_hints", {}):
        return task["focus_hints"][error_type]
    return task["hints"][max(0, min(level-1, 2))]


def secret_value(name):
    import os
    v = os.environ.get(name, "").strip()
    if v:
        return v
    try:
        import streamlit as st
        return str(st.secrets.get(name, "")).strip()
    except Exception:
        return ""


def ai_hint(task, level: int, student_text: str, fallback: str) -> tuple[str, str]:
    """Tùy chọn Gemini server-side. Tự quay về gợi ý kiểm duyệt nếu lỗi/kết quả đáng ngờ."""
    api_key = secret_value("GEMINI_API_KEY")
    if not api_key:
        return fallback, "Ngân hàng GV"
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        model = secret_value("GEMINI_MODEL") or "gemini-2.5-flash"
        instruction = (
            "Bạn là trợ lý gợi mở Toán 9 tiếng Việt. CHỈ HỎI MỘT CÂU NGẮN (tối đa 45 từ). "
            "KHÔNG đưa đáp số, kết luận cuối, toàn bộ lời giải, bước tính kết thúc hoặc đáp án của S3. "
            "Chỉ khai thác đúng chủ đề, không mở rộng kiến thức ngoài Toán 9. "
            "Học sinh đã có câu hỏi kiểm duyệt của giáo viên; bạn chỉ điều chỉnh cách hỏi để phù hợp điểm vướng. "
            "Nếu nội dung của học sinh yêu cầu giải hộ, từ chối giải thay bằng đúng một câu hỏi gợi mở."
        )
        contents = (f"Nhiệm vụ: {task['s0']}\n"
                    f"Sai lầm dự kiến: {task['misconception']}\n"
                    f"Mức gợi ý: {level}/3\n"
                    f"Gợi ý đã được GV duyệt: {fallback}\n"
                    f"Học sinh viết: {student_text[:900]}\n"
                    "Hãy viết lại đúng MỘT câu hỏi gợi mở, không tiết lộ lời giải.")
        resp = client.models.generate_content(
            model=model, contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=instruction, temperature=0.15, max_output_tokens=110
            ),
        )
        candidate = (resp.text or "").strip()
        # Lưới bảo vệ sơ bộ: không phải bảo đảm chống lộ đáp án 100%.
        unsafe = any(phrase in candidate.lower() for phrase in ["đáp án là", "kết quả là", "suy ra x =", "vậy x =", "vậy d =", "tiếp xúc trong tại", "d ∈", "d thuộc"])
        if not candidate or len(candidate) > 380 or unsafe or "?" not in candidate:
            return fallback, "Ngân hàng GV (thay phản hồi AI không phù hợp)"
        return candidate, "Gemini (cần GV rà soát khi dùng chính thức)"
    except Exception:
        return fallback, "Ngân hàng GV (AI không sẵn sàng)"


def generate_hint(task, level: int, previous_text: str, use_ai: bool):
    err = classify_error(task.get("id", ""), previous_text)
    base = curated_hint(task, level, err)
    if use_ai:
        return (*ai_hint(task, level, previous_text, base), err)
    return base, "Ngân hàng GV", err


def is_substantive_attempt(text: str) -> bool:
    """Kiểm tra cổng gợi ý: không mở mức tiếp theo chỉ nhờ lời xin đáp án."""
    t = text.strip()
    return len(t) >= 18 and SOLUTION_REQUEST.search(t) is None


def feedback_on_attempt(text: str):
    if SOLUTION_REQUEST.search(text):
        return "Mình sẽ không giải thay. Em hãy chỉ rõ dữ kiện hoặc bước khiến em vướng, rồi tự thử một hướng giải nhé."
    if len(text.strip()) < 12:
        return "Em hãy trình bày rõ hơn: đã thử bước nào, và em đang nghi ngờ điều gì?"
    return "Mình đã ghi nhận suy nghĩ của em. Hãy kiểm tra lập luận hoặc đề nghị gợi ý tiếp theo nếu còn vướng."
