"""Trợ lý gợi mở Toán 9 – ứng dụng Streamlit đa phân hệ.
Giai đoạn: bản thử nghiệm sư phạm, không chấm điểm trước–sau tự động.
"""
from __future__ import annotations

import hmac
import html
import json
import re
import uuid
from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from math_tasks import TASKS
from circle_curriculum import TOPIC_NAME, LESSONS, EXERCISES, guess_lesson, lesson_exercises
from circle_tutor import ask_tutor, next_self_practice
from tutor_engine import feedback_on_attempt, generate_hint, secret_value, is_substantive_attempt, chat_response, ai_is_enabled, review_reasoning, gemini_connection_test
from storage import (all_assessments, all_sessions, assessment_summary,
                     save_assessment, to_csv_bytes, upsert_session)

st.set_page_config(
    page_title="Trợ lý gợi mở Toán 9", page_icon="📘", layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');
:root{--ink:#19345c;--muted:#67819c;--blue:#1558c0;--cyan:#12a5b5;--purple:#7561cd;--soft:#f6f9ff}
html,body,[class*="css"],.stApp{font-family:'Be Vietnam Pro',system-ui,-apple-system,sans-serif!important}
.stApp{background:linear-gradient(135deg,#f8fbff 0%,#fff 54%,#f7fcfc 100%);color:#21344e}
.block-container{max-width:1200px;padding-top:1.45rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:linear-gradient(175deg,#e9f3ff 0%,#f1f8ff 70%,#effaf8 100%);border-right:1px solid #dce8f5}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2{color:#11396f}
[data-testid="stSidebar"] label{font-weight:600}
h1,h2,h3{letter-spacing:-.03em;color:#12396b}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:linear-gradient(110deg,#1363d6,#119db4)!important;border:0!important;color:#fff!important;box-shadow:0 8px 18px rgba(20,90,180,.17);border-radius:12px!important;font-weight:700}
.stButton>button,.stDownloadButton>button,.stFormSubmitButton>button{border-radius:12px!important;min-height:2.6rem;transition:transform .15s ease,box-shadow .15s ease}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-1px);box-shadow:0 7px 16px rgba(30,80,145,.10)}
[data-testid="stTextArea"] textarea,[data-testid="stTextInput"] input{border-radius:12px!important;border-color:#cfddec!important}
[data-testid="stVerticalBlockBorderWrapper"]{border-radius:18px!important;background:#fff}
[data-testid="stChatMessage"]{border-radius:15px;padding:10px 14px;margin:8px 0;border:1px solid #e3eaf7}
[data-testid="stProgress"]{margin-top:12px}
.hero{position:relative;overflow:hidden;border-radius:24px;padding:32px 36px;margin:0 0 20px;
background:radial-gradient(circle at 86% 18%,rgba(114,231,224,.24) 0,transparent 30%),linear-gradient(115deg,#113775,#155ec8 63%,#1595ae);color:#fff;box-shadow:0 14px 30px rgba(16,76,153,.16)}
.hero:after{content:'∑  π  √  x²';position:absolute;right:15px;bottom:-30px;color:#d5fbff;opacity:.16;transform:rotate(-13deg);font-size:72px;letter-spacing:12px;white-space:nowrap}
.hero h1{color:white;font-size:clamp(1.65rem,3.6vw,2.5rem);font-weight:800;margin:7px 0 9px;letter-spacing:-.035em}
.hero p{color:#eefaff;font-size:clamp(.85rem,1.2vw,1.02rem);line-height:1.75;margin:0}
.eyebrow{display:inline-block;background:rgba(255,255,255,.18);color:white;border:1px solid rgba(255,255,255,.24);padding:6px 11px;border-radius:100px;font-size:.78rem;font-weight:700}
.phase-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0 28px}
.phase-card{min-width:0;min-height:118px;border-radius:17px;padding:17px 14px;background:white;border:1px solid #e2ebf7;box-shadow:0 5px 16px rgba(49,95,163,.05)}
.phase-card .tag{display:block;font-weight:800;letter-spacing:.05em;font-size:.71rem;color:#506c96;margin-bottom:7px}
.phase-card .title{color:#173963;font-size:1rem;font-weight:800;line-height:1.5}
.phase-card .desc{font-size:.78rem;color:#687f9c;line-height:1.55;margin-top:5px}
.task{background:#fff;border:1px solid #cfdff2;border-left:5px solid #159eb6;border-radius:16px;padding:20px 23px;margin:12px 0 20px;font-size:1.06rem;line-height:1.85;box-shadow:0 4px 14px rgba(35,90,145,.05)}
.notice{padding:14px 17px;background:#f3f8ff;border-radius:14px;border:1px solid #d6e4f6}
.stage-tag{display:inline-block;padding:6px 12px;border-radius:9px;color:#13539c;background:#e5f2ff;font-size:.78rem;font-weight:800;margin-right:8px}
.stage-title{font-size:1.3rem;font-weight:800;color:#163c70;line-height:1.4}
.stage-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0 22px}
.stage-step{padding:10px 6px;text-align:center;border-radius:10px;color:#68819a;background:#edf4fa;font-size:.76rem;font-weight:700;line-height:1.45}
.stage-step.done{background:#e5f8f4;color:#0d8378}
.stage-step.active{background:#155fbe;color:#fff;box-shadow:0 5px 13px rgba(20,83,170,.16)}
.section-kicker{font-size:.85rem;color:#527194;text-transform:uppercase;letter-spacing:.06em;font-weight:800}
.lesson-card{padding:5px 2px 6px}
.lesson-title{font-weight:800;font-size:1.07rem;color:#15396a;min-height:3.1em}
.lesson-meta{color:#7188a0;font-size:.84rem}
.foot{font-size:.8rem;color:#7a8ea3;text-align:center;margin-top:45px;padding:14px;border-top:1px solid #edf1f7}
@media(max-width:740px){.block-container{padding:1.0rem .75rem 2rem}.hero{padding:24px 20px;border-radius:20px}.hero:after{font-size:38px;right:5px;bottom:-10px}.phase-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}.phase-card{padding:12px;min-height:111px}.stage-steps{grid-template-columns:repeat(2,1fr)}.task{padding:14px 17px;font-size:1rem}}
@media(prefers-reduced-motion:reduce){.stButton>button{transition:none!important}}
.topic-intro{margin:20px 0 10px;padding:24px;border:1px solid #d9e7ff;border-radius:18px;background:linear-gradient(125deg,#f2f7ff,#f0fcff)}
.topic-intro h3{margin:8px 0;font-size:1.25rem}.topic-intro p{color:#516c88;margin-bottom:0}
.topic-eyebrow{font-size:.77rem;letter-spacing:.05em;font-weight:800;color:#006b91}
.topic-hero{padding:26px 30px;border-radius:22px;margin-bottom:22px;background:linear-gradient(110deg,#194183,#206dd9 55%,#12a4b9);color:white;box-shadow:0 12px 22px rgba(21,90,156,.15)}
.topic-hero h2{color:white;margin:7px 0;font-size:clamp(1.45rem,3vw,2.15rem)}
.topic-hero p{color:#ebfcff;line-height:1.65}.topic-hero span{font-size:.75rem;font-weight:800;letter-spacing:.06em;color:#d5eafc}
.topic-step-row{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:16px 0}
.topic-step-row span{background:#eef6ff;border:1px solid #dbe9f8;padding:10px 8px;border-radius:12px;text-align:center;color:#254d7d;font-size:.78rem;font-weight:700}
@media(max-width:740px){.topic-hero{padding:20px}.topic-step-row{grid-template-columns:repeat(2,1fr)}}
</style>
""", unsafe_allow_html=True)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def init_state():
    defaults = {
        "screen": "Trang chủ", "student_code": "", "session": None,
        "messages": [], "awaiting_attempt": False, "last_attempt": "",
        "teacher_authorized": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def student_code_valid(code):
    return bool(re.fullmatch(r"HS\d{2,3}", code.upper().strip()))


def save_current():
    if st.session_state.session:
        upsert_session(st.session_state.session)


def make_session(code, task_id, support_mode):
    return {
        "session_id": str(uuid.uuid4()), "student_code": code.upper(),
        "task_id": task_id, "started_at": now(), "s0": "", "s0_type": "A",
        "hints": [], "attempts": [], "s2": "", "s3": "", "highest_hint": 0,
        "status": "S0", "support_mode": support_mode, "ai_enabled": False,
    }


def task_box(task_text):
    st.markdown(f'<div class="task">{html.escape(task_text)}</div>', unsafe_allow_html=True)


def stage_header(stage_id, title, subtitle=""):
    st.markdown(f'<span class="stage-tag">{html.escape(stage_id)}</span><span class="stage-title">{html.escape(title)}</span>', unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)


def stage_navigation(status):
    names = [("S0", "Tự tư duy"), ("S1", "Gợi mở"), ("S2", "Phản biện"), ("S3", "Vận dụng")]
    order = ["S0", "S1", "S2", "S3", "Hoàn tất"]
    index = order.index(status) if status in order else 0
    items = []
    for i, (key, label) in enumerate(names):
        css = "active" if i == index else "done" if i < index else ""
        items.append(f'<div class="stage-step {css}">{key} · {label}</div>')
    st.markdown('<div class="stage-steps">' + ''.join(items) + '</div>', unsafe_allow_html=True)


def home():
    st.markdown("""<div class="hero"><span class="eyebrow">✦ HỌC TOÁN THEO CÁCH CỦA EM</span>
        <h1>📘 TRỢ LÝ GỢI MỞ TOÁN 9</h1>
        <p>Em tự tìm hướng giải · Trợ lý hỏi đúng chỗ vướng · Em kiểm chứng và tự giải bài mới.</p></div>""", unsafe_allow_html=True)
    tiles = [
        ("S0", "🧠 Tự tư duy", "Viết ý tưởng của riêng em"),
        ("S1", "💬 Gợi mở", "Hỗ trợ đúng chỗ vướng"),
        ("S2", "🔎 Phản biện", "Kiểm tra từng lập luận"),
        ("S3", "🚀 Vận dụng", "Tự làm bài toán mới"),
    ]
    st.markdown('<div class="phase-grid">' + ''.join(
        f'<div class="phase-card"><span class="tag">{tag}</span><div class="title">{title}</div><div class="desc">{desc}</div></div>'
        for tag, title, desc in tiles) + '</div>', unsafe_allow_html=True)
    st.markdown('<div class="topic-intro"><div class="topic-eyebrow">🌟 KHÁM PHÁ NGÂN HÀNG HỌC LIỆU CHƯƠNG V</div><h3>Đường tròn · 5 bài học · 40 bài luyện tập tự biên soạn</h3><p>Nhập bài toán em đang vướng; trợ lý sẽ hỏi em từng bước như một gia sư. Có thể chọn một bài trong kho hoặc tự nhập đề.</p></div>', unsafe_allow_html=True)
    if st.button('💬 HỎI GIA SƯ CHỦ ĐỀ ĐƯỜNG TRÒN →', key='goto_circle_tutor', type='primary', use_container_width=True):
        st.session_state.screen = 'Gia sư Đường tròn'
        st.rerun()
    with st.expander('📚 Khám phá 5 bài học trong chủ đề Đường tròn'):
        for lid, lesson in LESSONS.items():
            st.write(f"**{lesson['title']}** · {len(lesson_exercises(lid))} bài luyện — {lesson['summary']}")
    st.markdown('<div class="section-kicker">CHẾ ĐỘ CŨ · LUYỆN THEO BÀI MẪU S0–S3</div>', unsafe_allow_html=True)
    st.subheader('Hôm nay em muốn khám phá chủ đề nào?')
    icons = {"circles":"◉", "radicals":"√", "quadratic":"x²", "system":"∑"}
    cols = st.columns(2)
    for i, (tid, task) in enumerate(TASKS.items()):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f'<div class="lesson-card"><div class="lesson-title">{icons.get(tid,"✦")} {html.escape(task["title"])}</div><div class="lesson-meta">{html.escape(task["topic"])} · {html.escape(task["duration"])}</div></div>',unsafe_allow_html=True)
                if st.button('Bắt đầu học  →', key=f'home_{tid}', type='primary', use_container_width=True):
                    st.session_state['pref_task'] = tid
                    st.session_state.screen = 'Luyện bài mẫu S0–S3'
                    st.rerun()
    st.info('**Phiên bản 3.0 – thử nghiệm (Chương V).** Khi chưa bật Gemini, ứng dụng dùng câu hỏi giáo viên biên soạn. Khi bật Gemini, trợ lý có thể đặt câu hỏi linh hoạt hơn theo bài làm, nhưng có thể sai và phải được giáo viên giám sát. Không nhập dữ liệu cá nhân.')


def start_or_continue():
    s = st.session_state.session
    if s is not None:
        task = TASKS[s["task_id"]]
        head = st.columns([4, 1])
        with head[0]:
            st.title(f"📖 {task['title']}")
            st.caption(f"Mã: {s['student_code']} · ID lượt học: {s['session_id'][:8]} · Phương thức: {s['support_mode']}")
        with head[1]:
            if st.button("↺ Đổi bài", type="secondary", help="Bắt đầu lượt học mới; lượt trước giữ trong cơ sở dữ liệu thử nghiệm"):
                st.session_state.session = None
                st.session_state.messages = []
                st.session_state.awaiting_attempt = False
                st.session_state.pop("s0_data", None)
                st.session_state.pop("s0_try", None)
                st.rerun()
        stages = ["S0", "S1", "S2", "S3", "Hoàn tất"]
        curr = stages.index(s["status"]) if s["status"] in stages else 0
        st.progress(curr / 4, text=f"Tiến trình của em: {s['status']}")
        stage_navigation(s['status'])
        if s["status"] == "S0": stage_s0(s, task)
        elif s["status"] == "S1": stage_s1(s, task)
        elif s["status"] == "S2": stage_s2(s, task)
        elif s["status"] == "S3": stage_s3(s, task)
        else: stage_complete(s, task)
        return
    st.title("📖 Bắt đầu lượt học")
    st.write("Học sinh dùng mã do giáo viên cấp (HS01, HS02, …); không nhập họ tên hoặc dữ liệu cá nhân.")
    with st.form("new_student"):
        code = st.text_input("Mã học sinh", value=st.session_state.student_code or "HS01", max_chars=5)
        labels = {k: v["title"] for k, v in TASKS.items()}
        options = list(TASKS)
        default_id = st.session_state.get("pref_task", "circles")
        idx = options.index(default_id) if default_id in options else 0
        task_id = st.selectbox("Chủ đề", options, index=idx, format_func=lambda k: labels[k])
        support = st.selectbox("Hình thức sử dụng", ["Chatbot cá nhân", "Chatbot nhóm", "Máy chiếu chung", "Thẻ giấy đối chiếu"])
        st.caption("Giáo viên cần thực hiện quy trình xin phép phù hợp trước khi dùng với học sinh. Mã học sinh không thay thế cơ chế xác thực người dùng.")
        can_ai = bool(secret_value("GEMINI_API_KEY")) and secret_value("ENABLE_GEMINI_FOR_STUDENTS").lower() in ("true", "1", "yes")
        choose_ai = st.checkbox("Dùng Gemini để điều chỉnh câu hỏi gợi mở (có gửi nội dung S0/S1 đến nhà cung cấp AI)", disabled=not can_ai)
        if not can_ai:
            st.caption("Chế độ Gemini chưa được giáo viên bật; hiện ứng dụng chỉ dùng bộ gợi ý đã biên soạn.")
        accept = st.checkbox("Tôi đã được giáo viên hướng dẫn và sẽ chỉ nhập nội dung học tập, không nhập thông tin riêng tư")
        go = st.form_submit_button("Bắt đầu S0", type="primary", use_container_width=True)
    if go:
        if not student_code_valid(code):
            st.error("Mã phải theo dạng HS01, HS02,… (2–3 chữ số).")
        elif not accept:
            st.warning("Cần xác nhận đã đọc hướng dẫn sử dụng an toàn.")
        else:
            st.session_state.student_code = ""
            st.session_state.session = make_session(code.upper().strip(), task_id, support)
            st.session_state.session["ai_enabled"] = bool(choose_ai)
            st.session_state.pop("s0_data", None)
            st.session_state.pop("s0_try", None)
            st.session_state.messages = []
            st.session_state.awaiting_attempt = False
            st.session_state.last_attempt = ""
            st.rerun()


def stage_s0(s, task):
    stage_header("S0", "Tự phân tích và đề xuất hướng giải", "Chưa có gợi ý chatbot. Em hãy viết những gì đã thử, kể cả khi chưa giải được.")
    task_box(task["s0"])
    with st.form("s0_form"):
        st.text_area("1. Dữ kiện và yêu cầu bài toán", key="s0_data", height=100,
                     placeholder="Ví dụ: R = ...; r = ...; d = ...; cần xác định ...")
        st.text_area("2. Hướng giải đã thử hoặc điểm em đang vướng", key="s0_try", height=135,
                     placeholder="Em nghĩ... vì... / Em chưa biết dùng điều kiện nào...")
        received_help = st.checkbox("Em đã được giáo viên hỗ trợ đọc hiểu/kiến thức nền trước khi viết S0")
        save = st.form_submit_button("Lưu S0 và sang S1", type="primary")
    if save:
        data = st.session_state.s0_data.strip()
        attempt = st.session_state.s0_try.strip()
        if len(data) < 8 or len(attempt) < 10:
            st.warning("Em hãy ghi đủ dữ kiện, yêu cầu và ít nhất một bước đã thử hoặc một khó khăn cụ thể.")
        else:
            s["s0"] = "Dữ kiện/yêu cầu: " + data + "\nHướng giải/điểm vướng: " + attempt
            s["s0_type"] = "B" if received_help else "A"
            s["status"] = "S1"
            st.session_state.last_attempt = attempt
            save_current()
            st.rerun()


def stage_s1(s, task):
    stage_header("S1", "Trò chuyện cùng trợ lý gợi mở",
                 "Trợ lý không đưa đáp án. Em hãy chia sẻ bước làm, nhận câu hỏi hỗ trợ và thử tự điều chỉnh.")
    with st.expander("📖 Xem lại bài toán và suy nghĩ ban đầu"):
        st.write(task["s0"])
        st.write("**Bài làm S0 của em:**", s["s0"])

    highest = s["highest_hint"]
    ai_on = bool(s.get("ai_enabled")) and ai_is_enabled()
    if not ai_on and ai_is_enabled():
        st.info("Gemini đã được giáo viên cấu hình, nhưng lượt học này chưa chọn dùng AI. Em có thể bật tại đây để trợ lý đọc bước giải vừa viết.")
        consent_ai = st.checkbox("Tôi đồng ý dùng câu trả lời học tập ẩn danh để Gemini đặt câu hỏi (không nhập thông tin cá nhân)", key="consent_ai_mid_session")
        if st.button("🤖 Bật Gemini cho lượt học hiện tại", disabled=not consent_ai):
            s["ai_enabled"] = True
            save_current()
            st.rerun()
    elif not ai_is_enabled():
        st.caption("Hiện Gemini chưa bật trong Settings → Secrets. Bộ câu hỏi thích ứng theo lỗi phổ biến vẫn hoạt động; đây không phải AI ngôn ngữ tự nhiên.")
    status_cols = st.columns([1.2, 2, 1.8])
    with status_cols[0]:
        st.metric("Mức gợi ý", f"{highest}/3")
    with status_cols[1]:
        st.caption("Chế độ hỗ trợ")
        st.markdown("🤖 **AI Gemini + câu hỏi dự phòng**" if ai_on else "📘 **Ngân hàng câu hỏi giáo viên**")
    with status_cols[2]:
        st.caption("Quyền tự lựa chọn")
        st.markdown("**Không cần gợi ý → sang S2**")

    if s["highest_hint"] >= 3:
        st.info("Em đã nhận tối đa ba mức gợi ý. Hãy viết cách làm của mình và chuyển sang S2 khi sẵn sàng.")
    elif st.session_state.awaiting_attempt:
        st.warning("📝 Sau gợi ý vừa nhận, em hãy viết một bước suy nghĩ của riêng mình trong khung hội thoại để mở mức tiếp theo.")
    cols = st.columns([1.2, 1.0])
    with cols[0]:
        next_level = highest + 1
        if st.button(f"✨ Nhận gợi ý mức {next_level}" if highest < 3 else "Đã đủ 3 mức gợi ý",
                     type="primary", use_container_width=True,
                     disabled=(highest >= 3 or st.session_state.awaiting_attempt)):
            task_for_engine = dict(task, id=s["task_id"])
            with st.spinner("Đang tìm câu hỏi đúng chỗ em vướng...") if ai_on else st.empty():
                hint, src, error_type = generate_hint(
                    task_for_engine, next_level,
                    st.session_state.last_attempt or s["s0"], use_ai=ai_on
                )
            s["highest_hint"] = next_level
            s["hints"].append({"level": next_level, "text": hint, "source": src,
                               "error_hint": error_type, "time": now()})
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"**🧭 Gợi ý mức {next_level}:** {hint}\n\n_{src}_"
            })
            st.session_state.awaiting_attempt = True
            save_current()
            st.rerun()
    with cols[1]:
        if st.button("Tiếp tục sang S2 →", use_container_width=True):
            s["status"] = "S2"
            save_current()
            st.rerun()

    st.markdown("### 💬 Cuộc trao đổi")
    if not st.session_state.messages:
        st.info("Em có thể bấm nhận gợi ý hoặc viết một ý tưởng mới để trợ lý hỏi lại theo suy nghĩ của em.")
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍🎓" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])
    st.caption("Ví dụ: ‘Em nghĩ hai đường tròn cắt nhau vì d < R + r’, hoặc ‘Em chưa biết điều kiện nào còn thiếu’. Không cần viết quá dài.")
    prompt = st.chat_input("Nhắn bước em đã thử hoặc điều chưa hiểu...")
    if prompt:
        prompt = prompt.strip()[:1200]
        if prompt:
            s["attempts"].append({"time": now(), "text": prompt})
            st.session_state.messages.append({"role": "user", "content": prompt})
            task_for_engine = dict(task, id=s["task_id"])
            with st.spinner("Trợ lý đang đọc suy nghĩ của em...") if ai_on else st.empty():
                reply, source = chat_response(task_for_engine, prompt, use_ai=ai_on,
                                              level=max(1, s["highest_hint"]))
            st.session_state.messages.append({"role": "assistant", "content": reply + "\n\n_" + source + "_"})
            # Trợ lý đối thoại theo lời học sinh cũng là một hình thức gợi ý.
            # Nếu trước đó chưa mở gợi ý, gán mức 1 để nhật ký không đánh giá thiếu hỗ trợ.
            given_hint = is_substantive_attempt(prompt)
            if given_hint and s["highest_hint"] == 0:
                s["highest_hint"] = 1
                s["hints"].append({"level": 1, "text": reply, "source": source,
                                   "error_hint": "qua_hội_thoại", "time": now()})
                st.session_state.awaiting_attempt = True
            elif given_hint:
                s["hints"].append({"level": s["highest_hint"], "text": reply, "source": source,
                                   "error_hint": "qua_hội_thoại", "time": now()})
                st.session_state.awaiting_attempt = False
            st.session_state.last_attempt = prompt
            save_current()
            st.rerun()


def stage_s2(s, task):
    stage_header("S2", "Kiểm chứng và phản biện cùng trợ lý",
                 "Em viết lập luận của mình, rồi có thể xin một câu hỏi phản biện để tự kiểm tra trước khi nộp. Không chấm điểm tự động.")
    task_box(task["s0"])
    with st.expander("📋 Các câu hỏi tự kiểm tra của giáo viên", expanded=False):
        for c in task["s2_check"]:
            st.write("• " + c)

    ai_on = bool(s.get("ai_enabled")) and ai_is_enabled()
    if ai_on:
        st.caption("🤖 Phản biện bằng Gemini nếu kết nối thành công; nếu không, dùng câu hỏi dự phòng.")
    elif ai_is_enabled():
        st.info("Gemini đã cấu hình nhưng lượt học chưa bật AI. Bạn có thể bật tại S2 mà không cần làm lại S0.")
        agree = st.checkbox("Tôi đồng ý gửi chỉ nội dung bài Toán 9 không có thông tin cá nhân cho Gemini", key="s2_ai_consent")
        if st.button("🤖 Bật Gemini để phản biện S2", disabled=not agree):
            s["ai_enabled"] = True
            save_current()
            st.rerun()
    else:
        st.caption("📘 Phản biện bằng câu hỏi thích ứng dự phòng. Để dùng Gemini, giáo viên cần bật ENABLE_GEMINI_FOR_STUDENTS trong Secrets trước.")
    sid = s["session_id"][:10]
    draft = st.text_area(
        "Lời giải / lập luận em muốn kiểm tra", key=f"s2_draft_{sid}",
        height=210, value=s.get("s2", ""),
        placeholder="Ví dụ: Em kết luận hai đường tròn cắt nhau vì d < R + r..."
    )
    reviews = [item for item in s["hints"] if item.get("phase") == "S2"]
    if reviews:
        st.markdown("**Những câu hỏi phản biện đã nhận:**")
        for i, item in enumerate(reviews, 1):
            st.info(f"**Câu hỏi {i}:** {item['text']}\n\n_{item.get('source', 'Câu hỏi tự kiểm tra')}_")
        st.caption("Hãy bổ sung lập luận của em vào ô bên trên trước khi hoàn tất.")
    a, b = st.columns(2)
    with a:
        ask = st.button(
            f"🔎 Hỏi phản biện ({len(reviews)}/2)",
            disabled=len(reviews) >= 2, use_container_width=True
        )
    with b:
        submitted = st.button("✅ Lưu S2 và sang S3", type="primary", use_container_width=True)
    if ask:
        if len(draft.strip()) < 18:
            st.warning("Em hãy viết một bước suy luận cụ thể trước khi yêu cầu trợ lý phản biện.")
        else:
            task_for_engine = dict(task, id=s["task_id"])
            with st.spinner("Đang lựa chọn câu hỏi phản biện theo lập luận của em...") if ai_on else st.empty():
                q, source, diagnosed = review_reasoning(
                    task_for_engine, draft.strip(), ai_on, review_turn=len(reviews) + 1)
            s["s2"] = draft.strip()
            s["attempts"].append({"phase": "S2", "time": now(), "text": draft.strip()})
            s["hints"].append({"phase": "S2", "level": max(1, s["highest_hint"]),
                               "text": q, "source": source, "error_hint": diagnosed, "time": now()})
            s["highest_hint"] = max(1, s["highest_hint"])
            save_current()
            st.rerun()
    if submitted:
        if len(draft.strip()) < 30:
            st.warning("Em cần trình bày rõ lý do và điều kiện đã kiểm chứng (ít nhất 30 ký tự).")
        else:
            s["s2"] = draft.strip()
            s["status"] = "S3"
            save_current()
            st.rerun()


def stage_s3(s, task):
    stage_header("S3", "Vận dụng độc lập – không gợi ý", "Trong giai đoạn này chatbot KHÔNG phản hồi lời giải, không đưa gợi ý hoặc đáp án.")
    task_box(task["s3"])
    st.warning("Để đánh giá năng lực thực chất, giáo viên cần giám sát bài làm; việc tắt gợi ý trong ứng dụng không ngăn được học sinh mở một công cụ khác.")
    with st.form("s3_form"):
        attempt = st.text_area("Bài làm độc lập S3", height=250,
                               placeholder="Trình bày từng bước em tự thực hiện...", value=s.get("s3", ""))
        done = st.form_submit_button("Nộp bài S3 và hoàn tất", type="primary")
    if done:
        if len(attempt.strip()) < 15:
            st.warning("Em hãy trình bày bài làm trước khi nộp.")
        else:
            s["s3"] = attempt.strip()
            s["status"] = "Hoàn tất"
            save_current()
            st.rerun()


def stage_complete(s, task):
    if st.session_state.get('celebrated_session') != s['session_id']:
        st.session_state['celebrated_session'] = s['session_id']
        st.balloons()
    st.success("🎉 Đã hoàn thành lượt học S0–S3. Bài S3 được lưu để giáo viên xem xét; đây không phải điểm chấm tự động.")
    st.metric("Mức gợi ý cao nhất", s["highest_hint"])
    with st.expander("Xem lại chuỗi minh chứng S0–S3", expanded=True):
        st.write("**S0 – Tự tư duy**")
        st.code(s["s0"], language="text")
        st.write("**S1 – Gợi ý và phản hồi**")
        for x in s["hints"]:
            st.write(f"Mức {x['level']} ({x['source']}): {x['text']}")
        for x in s["attempts"]:
            st.write(f"Học sinh: {x['text']}")
        st.write("**S2 – Kiểm chứng**")
        st.code(s["s2"], language="text")
        st.write("**S3 – Vận dụng độc lập**")
        st.code(s["s3"], language="text")
    payload = json.dumps(s, ensure_ascii=False, indent=2).encode("utf-8")
    st.download_button("⬇️ Tải hồ sơ học tập (JSON)", data=payload,
        file_name=f"{s['student_code']}_{s['task_id']}_{s['session_id'][:8]}.json",
        mime="application/json", use_container_width=True)
    st.caption("Dữ liệu chỉ chứa mã học sinh và nội dung học tập. Giáo viên phải có quy trình lưu giữ, sao lưu và hủy dữ liệu phù hợp.")
    with st.expander("Đáp án để tự đối chiếu SAU KHI NỘP (không dùng để tính điểm)"):
        st.write(task["teacher_key"])
    if st.button("Bắt đầu bài mới"):
        st.session_state.session = None
        st.session_state.messages = []
        st.session_state.awaiting_attempt = False
        st.session_state.pop("s0_data", None)
        st.session_state.pop("s0_try", None)
        st.rerun()


def personal_log():
    st.title("🗂️ Nhật ký lượt học")
    if not st.session_state.session:
        st.info("Hãy chọn 'Gia sư Đường tròn' hoặc 'Luyện bài mẫu S0–S3' để bắt đầu. Nhật ký ở đây thuộc phiên trình duyệt hiện tại.")
        return
    s = st.session_state.session
    st.write(f"**Học sinh:** {s['student_code']}   |   **Chủ đề:** {TASKS[s['task_id']]['title']}")
    a, b, c = st.columns(3)
    a.metric("Giai đoạn", s["status"])
    b.metric("Mức gợi ý", s["highest_hint"])
    c.metric("Lượt phản hồi", len(s["attempts"]))
    st.write("**S0:**", s["s0"] or "Chưa hoàn thành")
    st.write("**S2:**", s["s2"] or "Chưa hoàn thành")
    st.write("**S3:**", s["s3"] or "Chưa hoàn thành")
    st.download_button("Tải nhật ký lượt học hiện tại", json.dumps(s, indent=2, ensure_ascii=False).encode("utf-8"),
                        file_name=f"nhat_ky_{s['student_code']}.json", mime="application/json")


def access_teacher():
    st.title("👩‍🏫 Góc giáo viên")
    expected = secret_value("ADMIN_PASSWORD")
    if not expected or expected == "THAY_BANG_MAT_KHAU_MANH_CUA_GIAO_VIEN":
        st.error("Chưa cài mật khẩu giáo viên. Hãy cấu hình ADMIN_PASSWORD trong Secrets của ứng dụng để mở khu vực quản trị.")
        return False
    if not st.session_state.teacher_authorized:
        with st.form("teacher_signin"):
            password = st.text_input("Mật khẩu giáo viên", type="password")
            ok = st.form_submit_button("Đăng nhập", type="primary")
        if ok:
            if hmac.compare_digest(password, expected):
                st.session_state.teacher_authorized = True
                st.rerun()
            else:
                st.error("Mật khẩu không đúng.")
        return False
    if st.button("Đăng xuất khu vực giáo viên"):
        st.session_state.teacher_authorized = False
        st.rerun()
    st.warning("**Lưu ý lưu trữ:** CSDL SQLite mặc định chỉ phù hợp thử nghiệm. Trên Streamlit Community Cloud, dữ liệu có thể mất khi ứng dụng khởi động lại. Hãy xuất CSV thường xuyên; muốn triển khai chính thức cần chuyển sang kho dữ liệu bền vững, quyền truy cập phù hợp và quy trình đồng ý/bảo vệ dữ liệu học sinh.")
    return True


def show_admin_sessions():
    st.subheader("Nhật ký S0–S3 của học sinh")
    records = all_sessions()
    st.metric("Số lượt học lưu trong bản thử nghiệm", len(records))
    if not records:
        st.info("Chưa có lượt học. Hãy hoàn thành một bài ở trang Học với chatbot để kiểm tra việc ghi nhật ký.")
        return
    grid = pd.DataFrame(records)
    slim = grid[["student_code", "task_id", "started_at", "status", "highest_hint", "s0_type", "support_mode"]].rename(columns={
        "student_code": "Mã HS", "task_id": "Chủ đề", "started_at": "Thời điểm",
        "status": "Tiến trình", "highest_hint": "Mức gợi ý", "s0_type": "Loại S0", "support_mode": "Hình thức"
    })
    st.dataframe(slim, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Xuất toàn bộ nhật ký S0–S3 (CSV)", to_csv_bytes(records),
        "nhat_ky_S0_S3_thu_nghiem.csv", mime="text/csv")
    choices = list(range(len(records)))
    ix = st.selectbox("Xem chi tiết lượt học", choices,
        format_func=lambda i: f"{records[i]['student_code']} | {TASKS.get(records[i]['task_id'], LESSONS.get(records[i]['task_id'], {})).get('title',records[i]['task_id'])} | {records[i]['started_at'][:16]}")
    rec = records[ix]
    with st.expander("Bản ghi chi tiết", expanded=False):
        st.write("**S0**", rec["s0"])
        st.write("**S1 – Gợi ý**", json.loads(rec["hints_json"]))
        st.write("**S1 – Phản hồi**", json.loads(rec["attempts_json"]))
        st.write("**S2**", rec["s2"])
        st.write("**S3**", rec["s3"])


def show_assessment_form():
    st.subheader("Nhập điểm đánh giá trước / sau")
    st.caption("Chỉ nhập điểm thực tế do giáo viên chấm, có bài làm và rubric đối chiếu. Không tự tạo số liệu hoặc suy ra điểm từ số lượt gợi ý.")
    with st.form("assessment_entry"):
        col1, col2, col3 = st.columns(3)
        with col1:
            code = st.text_input("Mã học sinh", value="HS01", max_chars=5)
            phase = st.radio("Thời điểm đánh giá", ["Trước", "Sau"], horizontal=True)
        with col2:
            selfstudy = st.number_input("Năng lực tự học (/12)", min_value=0., max_value=12., value=5., step=0.5)
            problem = st.number_input("Giải quyết vấn đề (/12)", min_value=0., max_value=12., value=5., step=0.5)
            exam = st.number_input("Bài kiểm tra độc lập (/10)", min_value=0., max_value=10., value=5., step=0.5)
        with col3:
            correct = st.selectbox("Tự nêu đúng hướng giải", ["Không", "Có"])
            detect = st.selectbox("Phát hiện đúng sai lầm", ["Không", "Có"])
            level = st.selectbox("Mức gợi ý cá nhân được xác định", ["Không xác định", "0", "1", "2", "3"])
        source = st.text_input("Tham chiếu bài làm / mã phiếu / lưu ý", placeholder="Ví dụ: Phiếu KT-A-21, đã chấm theo rubric")
        confirm = st.checkbox("Tôi xác nhận điểm vừa nhập được lấy từ minh chứng thật, không phải số liệu dựng")
        save = st.form_submit_button("Lưu điểm", type="primary")
    if save:
        if not student_code_valid(code):
            st.error("Mã học sinh phải theo dạng HS01, HS02,…")
        elif not confirm:
            st.warning("Cần xác nhận nguồn điểm trước khi lưu.")
        else:
            save_assessment({"student_code": code.upper().strip(), "phase": phase,
                "selfstudy": float(selfstudy), "problem_solving": float(problem),
                "independent": float(exam), "correct_plan": int(correct == "Có"),
                "detected_error": int(detect == "Có"),
                "highest_hint": None if level == "Không xác định" else int(level),
                "source_note": source.strip()})
            st.success(f"Đã lưu {phase.lower()} can thiệp cho {code.upper().strip()}.")


def show_results():
    st.subheader("Bốn biểu đồ so sánh – chỉ từ dữ liệu có cặp trước/sau")
    records = all_assessments()
    st.write(f"Hiện có **{len(records)} bản ghi đánh giá**. Đối chiếu theo mã học sinh ở hai thời điểm.")
    if records:
        st.download_button("⬇️ Xuất dữ liệu đánh giá (CSV)", to_csv_bytes(records),
                           "diem_danh_gia_THUC_TE.csv", mime="text/csv")
    summary = assessment_summary(records)
    if summary is None:
        st.info("Chưa có mã học sinh nào có đủ cả điểm Trước và Sau. Hãy nhập dữ liệu thực tế để ứng dụng tự vẽ biểu đồ.")
        return
    n = summary["n"]
    st.success(f"Có {n} học sinh có đủ hai lần đo. Tất cả biểu đồ dưới đây chỉ tính trên {n} cặp hợp lệ.")
    avg = summary["averages"]
    st.write("**Biểu đồ 1 – Điểm trung bình ba thước đo**")
    df = pd.DataFrame({"Tự học /12": avg["selfstudy"], "GQVĐ toán học /12": avg["problem_solving"],
                       "Bài độc lập /10": avg["independent"]}).T
    st.bar_chart(df)
    st.write("**Biểu đồ 2 – Phân bố điểm bài kiểm tra độc lập**")
    st.bar_chart(pd.DataFrame(summary["bands"]).T)
    st.write("**Biểu đồ 3 – Số học sinh tự nêu đúng hướng giải / phát hiện đúng sai lầm**")
    df3 = pd.DataFrame({"Nêu hướng giải đúng": avg["correct_plan"],
                        "Phát hiện sai lầm": avg["detected_error"]}).T * n
    st.bar_chart(df3)
    st.write("**Biểu đồ 4 – Phân bố mức gợi ý cao nhất (cá nhân có dữ liệu xác định)**")
    st.bar_chart(pd.DataFrame({f"Mức {k}": v for k, v in summary["hints"].items()}).T)
    st.caption(f"Mẫu hợp lệ mức gợi ý: Trước {summary['valid_hint']['Trước']}, Sau {summary['valid_hint']['Sau']}. Không quy đổi tự động hỗ trợ theo nhóm thành dữ liệu cá nhân.")
    st.info("Tăng điểm là mô tả thay đổi, chưa đủ kết luận quan hệ nhân quả. Cần đối chiếu bài làm, điều kiện tổ chức và thẩm định độ tương đương đề trước/sau.")


def teacher_dashboard():
    if not access_teacher():
        return
    with st.expander("🔌 Kiểm tra kết nối Gemini (chỉ giáo viên)"):
        st.caption("Bấm để kiểm tra API và mô hình bằng câu hỏi thử, không gửi bài học sinh.")
        if st.button("Kiểm tra Gemini ngay", key="probe_gemini"):
            connected, message = gemini_connection_test()
            if connected:
                st.success(message)
            else:
                st.warning(message)

    tabs = st.tabs(["Nhật ký S0–S3", "Nhập kết quả thật", "Biểu đồ trước–sau", "Đáp án GV", "📚 Kho học liệu Đường tròn"])
    with tabs[0]: show_admin_sessions()
    with tabs[1]: show_assessment_form()
    with tabs[2]: show_results()
    with tabs[3]:
        st.subheader("Đáp án gốc để giáo viên duyệt")
        for task in TASKS.values():
            with st.expander(task["title"]):
                st.write("**S0:**", task["s0"])
                st.write("**Sai lầm dự kiến:**", task["misconception"])
                st.write("**Gợi ý:**")
                for i, h in enumerate(task["hints"], 1):
                    st.write(f"Mức {i}. {h}")
                st.write("**S3:**", task["s3"])
                st.write("**Đáp án GV:**", task["teacher_key"])


    with tabs[4]:
        st.subheader("Ngân hàng học liệu Chương V – Đường tròn")
        st.info("Kho do giáo viên biên soạn: 5 bài học, 40 bài luyện; giao diện chỉ hiển thị đáp án trong Góc giáo viên. Lưu ý: nếu GitHub công khai thì mã nguồn có chứa đáp án; không dùng các bài này làm bài kiểm tra kín.")
        st.metric("Số bài luyện tự biên soạn", len(EXERCISES))
        lids = list(LESSONS)
        chosen = st.selectbox("Bài học", lids, format_func=lambda k: LESSONS[k]["title"], key="teacher_lesson")
        for name, value in LESSONS[chosen]["concepts"]:
            st.markdown(f"**{name}:** {value}")
        st.write("**Sai lầm thường gặp:**", "; ".join(LESSONS[chosen]["misconceptions"]))
        for ex in lesson_exercises(chosen):
            with st.expander(f"{ex['id']} · {ex['title']} · Mức {ex['level']}"):
                st.write("**Đề tự biên soạn:**", ex["problem"])
                st.write("**Ba mức gợi ý tham chiếu:**")
                for i, q in enumerate(ex["hints"],1): st.write(f"{i}. {q}")
                st.write("**Đáp án giáo viên:**", ex["teacher_answer"])
        export = {"topic": TOPIC_NAME, "lessons": LESSONS, "exercises": EXERCISES,
                  "note": "Học liệu tự biên soạn để giáo viên thẩm định; không dùng như dữ liệu kết quả thực nghiệm"}
        st.download_button("⬇️ Tải toàn bộ học liệu và đáp án (JSON – chỉ giáo viên)",
                           json.dumps(export, ensure_ascii=False, indent=2).encode("utf-8"),
                           "hoc_lieu_chu_de_duong_tron_Toan9_GV.json", mime="application/json")


def circle_topic_tutor():
    """Gia sư hội thoại tự nhiên; cho nhập đề bất kỳ trong toàn chương, vẫn đo quá trình S0–S3."""
    st.markdown('<div class="topic-hero"><span>TRỢ LÝ GỢI MỞ TOÁN 9</span><h2>💬 Hỏi gia sư chủ đề Đường tròn</h2><p>Em đặt câu hỏi mình chưa biết · Trợ lý tìm kiến thức liên quan · Em từng bước tự giải.</p></div>', unsafe_allow_html=True)
    if "circle_chat" not in st.session_state:
        st.session_state.circle_chat = None
    ss = st.session_state.circle_chat
    if not ss:
        st.write("### Em muốn nhờ trợ lý hướng dẫn bài toán nào?")
        col1, col2 = st.columns([2, 1])
        with col1:
            code = st.text_input("Mã học sinh (không dùng tên thật)", value="HS01", key="topic_code", max_chars=6)
        with col2:
            mode = st.selectbox("Bài học", ["auto"] + list(LESSONS),
                format_func=lambda x: "Tự nhận diện trong Chương V" if x == "auto" else LESSONS[x]["title"],
                key="topic_lesson_choice")
        choose = st.radio("Cách nhập bài", ["Nhập đề bài của em", "Chọn bài trong ngân hàng"], horizontal=True, key="topic_input_mode")
        chosen = None
        if choose == "Chọn bài trong ngân hàng":
            pool = EXERCISES if mode == "auto" else lesson_exercises(mode)
            options = {e["id"]: e for e in pool}
            eid = st.selectbox("Chọn bài để học", list(options), format_func=lambda k: f"{k} · {options[k]['title']}")
            chosen = options[eid]
            problem = chosen["problem"]
            st.info(problem)
        else:
            problem = st.text_area("Nhập nguyên văn đề toán em chưa biết làm", height=145,
                placeholder="Ví dụ: Cho hai đường tròn (O; 5 cm) và (O'; 3 cm), OO' = 2 cm. Hai đường tròn có mấy điểm chung? Vì sao?",
                key="topic_problem")
            st.caption("Bản 3.0 hỗ trợ nhập đề dạng chữ. Hình vẽ/ảnh đề bài sẽ được phát triển và kiểm thử riêng.")
        allow_ai = ai_is_enabled()
        use_ai = st.checkbox("Cho phép sử dụng Gemini để gợi mở trong lượt học thử", value=False, disabled=not allow_ai,
                             help="Nội dung đề và tin nhắn (đã giảm thiểu dữ liệu cá nhân) sẽ gửi tới dịch vụ Gemini khi bật.")
        if not allow_ai:
            st.caption("Gemini chưa sẵn sàng trong cấu hình này; trợ lý vẫn dùng ngân hàng câu hỏi do giáo viên biên soạn.")
        st.warning("Chỉ dùng mã học sinh giả và đề thử ở giai đoạn này; không nhập tên, số điện thoại hoặc dữ liệu riêng tư. Mã HS không phải tài khoản đăng nhập có bảo mật.")
        if st.button("🚀 Bắt đầu trao đổi với gia sư", type="primary", use_container_width=True):
            if not re.fullmatch(r"[A-Za-z0-9_-]{3,10}", code.strip()):
                st.error("Mã học sinh gồm 3–10 ký tự, chỉ chữ, số, dấu gạch dưới hoặc gạch ngang.")
            elif len(problem.strip()) < 15:
                st.warning("Em nhập đề bài đầy đủ hơn một chút nhé.")
            else:
                lid = chosen["lesson"] if chosen else (mode if mode != "auto" else guess_lesson(problem)[0])
                st.session_state.circle_chat = {
                    "id": str(uuid.uuid4()), "student_code": code.strip().upper(), "problem": problem.strip()[:2500],
                    "selected_lesson": lid, "chosen_exercise": chosen,
                    "messages": [{"role":"assistant", "text":"Mình đã nhận đề của em. Trước khi gợi ý, em đã thử cách nào? Em có thể viết một bước, kể cả khi chưa đúng nhé.", "source":"Khởi động S0"}],
                    "phase": "S0", "turns": 0, "highest_hint":None, "s0":"", "s2":"", "s3_problem":"", "s3_answer":"", "use_ai": bool(use_ai and allow_ai),
                    "started_at":now(), "answered_practice_id":None,
                }
                st.rerun()
        with st.expander("📚 Xem kiến thức được chuẩn bị trong Chương V"):
            for lid, content in LESSONS.items():
                st.write(f"**{content['title']}** — {content['summary']}")
        return

    if st.button("↩ Chọn bài toán khác", key="topic_reset"):
        st.session_state.circle_chat = None
        st.rerun()
    lid = ss.get("selected_lesson")
    title = LESSONS[lid]["title"] if lid in LESSONS else "Chưa xác định chính xác mạch kiến thức"
    st.caption(f"Mã học sinh thử: {ss['student_code']} · {title} · Nguồn: {'Gemini + kho giáo viên' if ss['use_ai'] and ai_is_enabled() else 'Kho học liệu giáo viên'}")
    with st.container(border=True):
        st.markdown("**📝 Đề bài em đang cần hướng dẫn**")
        st.write(ss["problem"])
    st.markdown('<div class="topic-step-row"><span>🧠 S0 · Tự thử</span><span>💡 S1 · Gợi mở</span><span>🔍 S2 · Tự kiểm chứng</span><span>🚀 S3 · Tự vận dụng</span></div>', unsafe_allow_html=True)
    st.caption("Trợ lý chỉ hỏi từng bước, không đưa lời giải hoàn chỉnh. Nếu thấy câu hỏi chưa đúng, em hãy nhờ giáo viên kiểm tra.")
    for m in ss["messages"]:
        with st.chat_message("assistant" if m["role"] == "assistant" else "user", avatar="🤖" if m["role"] == "assistant" else "🧑‍🎓"):
            st.write(m["text"])
            if m.get("source") and m["role"] == "assistant":
                st.caption(m["source"])
    if ss["phase"] in ("S0", "S1", "S2"):
        incoming = st.chat_input("Viết bước em đã thử hoặc câu hỏi em đang vướng…", key=f"topic_chat_input_{ss['id']}")
        if incoming:
            if len(incoming.strip()) < 3:
                st.warning("Em viết rõ hơn một chút nhé.")
            else:
                ss["messages"].append({"role":"student", "text":incoming.strip()[:1400]})
                if ss["phase"] == "S0":
                    ss["s0"] = incoming.strip()[:1400]
                    ss["phase"] = "S1"
                ss["turns"] += 1
                # Ghi số lượt hỗ trợ riêng. KHÔNG đồng nhất số tin nhắn AI với MỨC GỢI Ý.
                question, source, meta = ask_tutor(ss["problem"], incoming, lid,
                    ss["messages"], ss["turns"], ss["use_ai"], chosen_exercise=ss.get("chosen_exercise"))
                # Chỉ gán mức 1–3 nếu câu hỏi thực sự là mức trong bộ học liệu cố định.
                if ss.get("chosen_exercise") and not meta.get("ai_used"):
                    level = min(3, ss["turns"])
                    ss["highest_hint"] = max(ss["highest_hint"] or 0, level)
                ss["messages"].append({"role":"assistant", "text":question, "source":source, "meta":meta})
                st.rerun()
    if ss["phase"] in ("S0", "S1", "S2"):
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📝 Em đã có hướng giải – tự kiểm chứng", use_container_width=True, disabled=ss['phase']=="S0"):
                ss["phase"] = "S2"
                st.rerun()
        with c2:
            if st.button("🚀 Chuyển sang bài vận dụng độc lập", use_container_width=True, disabled=ss['phase']=="S0"):
                target = ss.get("selected_lesson")
                skip = set()
                if ss.get("chosen_exercise"):
                    skip.add(ss["chosen_exercise"]["id"])
                nxt = next_self_practice(target, forbidden_ids=skip)
                if nxt:
                    ss["s3_problem"] = nxt["problem"]
                    ss["answered_practice_id"] = nxt["id"]
                    ss["phase"] = "S3"
                    st.rerun()
                else:
                    st.warning("Chưa nhận diện đủ chắc bài học của em để chọn bài vận dụng riêng. Hãy chọn đúng bài học hoặc nhờ giáo viên giao bài độc lập.")
    if ss["phase"] == "S2":
        with st.expander("🔍 Tự đối chiếu lập luận (S2)", expanded=True):
            ss["s2"] = st.text_area("Viết lập luận hoàn chỉnh bằng lời của em", value=ss.get("s2", ""),
                                     key=f"tutor_s2_{ss['id']}", height=125)
            st.caption("Em nên kiểm tra: đã ghi đúng giả thiết; đã giải thích từng phép suy luận; đã xét đủ điều kiện chưa?")
    if ss["phase"] == "S3":
        st.info("**S3 – Tự làm độc lập.** Trong nhiệm vụ này trợ lý không gửi gợi ý, không chấm tự động và không hiển thị đáp án.")
        st.markdown("### Bài vận dụng")
        st.write(ss["s3_problem"])
        answer = st.text_area("Bài giải của em (không hỏi AI trong lúc làm)", value=ss.get("s3_answer", ""),
                              key=f"tutor_s3_{ss['id']}", height=175)
        if st.button("✅ Nộp bài vận dụng", type="primary"):
            if len(answer.strip()) < 15:
                st.warning("Em cần trình bày thêm cách lập luận trước khi nộp.")
            else:
                ss["s3_answer"] = answer
                ss["phase"] = "Done"
                st.rerun()
    if ss["phase"] == "Done":
        st.success("Em đã nộp bài độc lập. Giáo viên sẽ kiểm tra và nhận xét; trợ lý không tự cho điểm.")
    export = {"name":"TRỢ LÝ GỢI MỞ TOÁN 9", "topic":TOPIC_NAME,
              "student_code":ss["student_code"], "session_id":ss["id"], "started_at":ss["started_at"],
              "lesson":title,"problem":ss["problem"],"s0":ss["s0"],"conversation":ss["messages"],
              "s2":ss.get("s2",""),"s3_problem":ss["s3_problem"],"s3_answer":ss["s3_answer"],
              "highest_hint_level":ss["highest_hint"], "number_of_tutor_questions":ss["turns"], "record_status":ss["phase"],
              "notes":"Dữ liệu lượt thử lưu trong phiên trình duyệt; không thay cho minh chứng có xác thực."}
    st.download_button("📥 Tải nhật ký hỏi gia sư (JSON)",
        json.dumps(export,ensure_ascii=False,indent=2).encode("utf-8"),
        f"nhat_ky_{ss['student_code']}_{ss['id'][:8]}.json", mime="application/json")
    with st.expander("Lưu lên nhật ký thử nghiệm của Góc giáo viên (tùy chọn)"):
        st.caption("Lưu vào SQLite trên máy chủ thử nghiệm và CÓ THỂ MẤT khi ứng dụng khởi động lại. Chưa dùng cho hồ sơ chính thức hoặc dữ liệu cá nhân học sinh.")
        consent = st.checkbox("Tôi chỉ dùng mã giả và nội dung thử nghiệm, đồng ý lưu lượt học lên máy chủ thử", key=f"topic_store_ok_{ss['id']}")
        if st.button("Lưu nhật ký thử nghiệm", disabled=not consent, key=f"topic_store_{ss['id']}"):
            saved = {
                "session_id":ss["id"], "student_code":ss["student_code"],
                "task_id":ss.get("selected_lesson") or "b17", "started_at":ss["started_at"],
                "s0":ss.get("s0", ""), "s0_type":"A",
                "hints":[{"text":m["text"],"source":m.get("source", "")}
                         for m in ss["messages"] if m["role"]=="assistant" and m.get("source") != "Khởi động S0"],
                "attempts":[{"text":m["text"],"phase":ss["phase"]}
                            for m in ss["messages"] if m["role"]=="student"],
                "s2":ss.get("s2",""), "s3":ss.get("s3_answer",""),
                "highest_hint":ss["highest_hint"], "status":ss["phase"],
                "support_mode":"Gia sư chủ đề Đường tròn", "ai_enabled":ss["use_ai"],
            }
            try:
                upsert_session(saved)
                st.success("Đã lưu nhật ký thử nghiệm. Giáo viên có thể xem trong Góc giáo viên; nhớ xuất CSV để sao lưu.")
            except Exception:
                st.error("Máy chủ chưa lưu được. Em vẫn có thể tải nhật ký JSON về máy.")


def guide():
    st.title("❓ Hướng dẫn và giới hạn sử dụng")
    st.subheader("Hỏi gia sư cho toàn bộ chủ đề Đường tròn")
    st.write("Chọn **Gia sư Đường tròn**, nhập bài toán em tự chọn hoặc một bài trong kho 40 bài; ghi bước đã thử; trò chuyện để nhận câu hỏi từng bước; sau đó tự kiểm chứng và làm bài mới độc lập. Ứng dụng có học liệu từ cả Bài 13 đến Bài 17, không phải một bài cố định.")
    st.subheader("Dành cho học sinh")
    st.write("1. Chọn 'Gia sư Đường tròn', nhập mã HSxx và bài toán riêng (hoặc bài trong ngân hàng). 2. Ghi bước em đã thử. 3. Trao đổi cùng trợ lý bằng câu hỏi ngắn, tự kiểm chứng. 4. Chọn bài vận dụng mới không có AI. 5. Xuất nhật ký JSON; chỉ lưu lên máy chủ thử nghiệm nếu được phép.")
    st.subheader("Dành cho giáo viên")
    st.write("Cấu hình ADMIN_PASSWORD trong Streamlit Secrets, mở Góc giáo viên để xem nhật ký và nhập dữ liệu đánh giá thực tế. Có thể xuất CSV và bốn biểu đồ khi có cặp điểm trước/sau.")
    st.subheader("Khác biệt giữa chatbot theo kịch bản và chatbot AI")
    st.write("**Mặc định:** Gia sư tham chiếu học liệu được giáo viên biên soạn cho cả Chương V. Khi không có Gemini, mức độ hiểu đề tự nhập còn hạn chế; câu hỏi dự phòng chủ yếu theo mạch kiến thức.")
    st.write("**Tùy chọn:** Khi giáo viên cấu hình GEMINI_API_KEY và bật ENABLE_GEMINI_FOR_STUDENTS=true, học sinh có thể chọn sử dụng Gemini. Nội dung S0/S1 khi đó được gửi tới dịch vụ Gemini; chỉ bật sau khi nhà trường xác nhận điều kiện bảo vệ dữ liệu. AI có thể sai hoặc lộ cách giải.")
    st.subheader("Lưu ý đạo đức và kỹ thuật")
    st.write("- Không nhập họ tên, địa chỉ, số điện thoại, thông tin sức khỏe hoặc dữ liệu riêng tư.\n"
             "- Bản thử nghiệm dùng SQLite trên máy chủ. Khi triển khai trên Streamlit Community Cloud, dữ liệu có thể mất do hệ thống khởi động lại; cần sao lưu CSV và nâng cấp lưu trữ có kiểm soát trước khi triển khai chính thức.\n"
             "- Mã HSxx không phải phương thức xác thực. Chỉ dùng cho thử nghiệm được nhà trường đồng ý; muốn áp dụng quy mô lớp cần xác thực và quy tắc truy cập dữ liệu.\n"
             "- AI không được dùng để chấm điểm chính thức. Điểm trước/sau chỉ lấy từ bài kiểm tra độc lập có giám sát và rubric do giáo viên đánh giá.\n"
             "- S3 không gợi ý trong ứng dụng, nhưng để đảm bảo không AI cần có giám sát lớp học.")


init_state()
with st.sidebar:
    st.markdown("## 📘 TRỢ LÝ GỢI MỞ TOÁN 9")
    st.caption("Ứng dụng thử nghiệm · Chương trình KNTT")
    sections = ["Trang chủ", "Gia sư Đường tròn", "Luyện bài mẫu S0–S3", "Nhật ký cá nhân", "Góc giáo viên", "Hướng dẫn"]
    selected = st.radio("Điều hướng", sections, index=sections.index(st.session_state.screen),
                        label_visibility="collapsed")
    st.session_state.screen = selected
    st.divider()
    s = st.session_state.session
    if s:
        st.write("**Mã HS:**", s["student_code"])
        st.caption("Giai đoạn hiện tại: " + s["status"])
    st.caption("🟢 Chế độ: " + ("Gemini đã cấu hình (cần bật trong lượt học)" if ai_is_enabled() else "Câu hỏi thích ứng dự phòng – chưa bật Gemini"))
    st.caption("Không đăng nhập bằng họ tên thật")
    st.caption("Phiên bản 3.0 · Chương V Đường tròn")

if selected == "Trang chủ": home()
elif selected == "Gia sư Đường tròn": circle_topic_tutor()
elif selected == "Luyện bài mẫu S0–S3": start_or_continue()
elif selected == "Nhật ký cá nhân": personal_log()
elif selected == "Góc giáo viên": teacher_dashboard()
else: guide()

st.markdown('<div class="foot">TRỢ LÝ GỢI MỞ TOÁN 9 • HỌC SINH TỰ TƯ DUY, GIÁO VIÊN GIỮ VAI TRÒ CHỦ ĐẠO<br/>Bản thử nghiệm sư phạm · Nội dung cần được giáo viên kiểm duyệt trước khi sử dụng chính thức.</div>', unsafe_allow_html=True)
