"""Ngân hàng nhiệm vụ và gợi ý do GV biên soạn, dùng cho ứng dụng Toán 9.
Các bài S3 là nhiệm vụ học tập mới, không dùng để đánh giá trước/sau chính thức.
"""

TASKS = {
    "circles": {
        "title": "Vị trí tương đối của hai đường tròn",
        "topic": "Hình học – Toán 9 KNTT",
        "duration": "22 phút",
        "s0": "Hai đường tròn (O; 5 cm) và (O′; 3 cm) có khoảng cách hai tâm OO′ = 2 cm. Xác định vị trí tương đối của hai đường tròn và giải thích căn cứ.",
        "misconception": "Chỉ dùng d < R + r đã kết luận hai đường tròn cắt nhau tại hai điểm.",
        "hints": [
            "Từ d < R + r, đã đủ căn cứ kết luận hai đường tròn cắt nhau tại hai điểm chưa? Hãy thử phác một hình khác.",
            "Ngoài tổng hai bán kính, em cần so sánh khoảng cách hai tâm d với đại lượng nào nữa?",
            "Hãy tính |5 − 3|, so sánh với d = 2, rồi quan sát hình vẽ xem hai đường tròn có mấy điểm chung."
        ],
        "focus_hints": {
            "only_sum": "Em đã xét tổng R + r. Có một mốc nữa quyết định việc hai đường tròn cắt nhau hay tiếp xúc; em tìm xem đó là mốc nào?",
            "stuck": "Bước đầu tiên: em hãy viết ba dữ kiện R, r, d và phác hai đường tròn để quan sát.",
            "conclusion": "Nếu em đã kết luận vị trí, hãy tự kiểm tra kết luận đó bằng cả tổng và hiệu hai bán kính."
        },
        "s2_check": ["Có đủ điều kiện liên quan đến R, r và d không?", "Em đã phân biệt trường hợp cắt nhau với tiếp xúc trong chưa?", "Em giải thích được bằng hình vẽ hoặc định lý nào?"],
        "s3": "Hai đường tròn có bán kính R = 6 cm, r = 2 cm. Khoảng cách hai tâm d là số nguyên dương. Tìm mọi giá trị của d để hai đường tròn cắt nhau tại hai điểm và giải thích.",
        "teacher_key": "|R−r| < d < R+r ⇔ 4 < d < 8. Vì d nguyên dương nên d ∈ {5; 6; 7} cm.",
    },
    "radicals": {
        "title": "Biến đổi căn thức bậc hai",
        "topic": "Đại số – Toán 9 KNTT",
        "duration": "18–22 phút",
        "s0": "Một học sinh viết √(9 + 16) = √9 + √16. Em hãy kiểm tra tính đúng sai, chỉ ra lý do và nêu cách xử lý phù hợp.",
        "misconception": "Nhầm √(a+b) = √a + √b.",
        "hints": [
            "Em thử tính riêng giá trị vế trái và vế phải xem có bằng nhau hay không.",
            "Hãy tính √25 và √9 + √16. Hai kết quả khác nhau cho em biết điều gì?",
            "Dùng phản ví dụ 9 và 16 để bác bỏ quy tắc đang được đề xuất. Sau đó thử phát biểu một quy tắc biến đổi căn thức đúng mà em đã học."
        ],
        "focus_hints": {"sqrt_sum": "Em thử dùng một cặp số cụ thể thay cho a và b để kiểm tra quy tắc căn của tổng.", "stuck":"Em hãy thử tính hai vế của đẳng thức trước khi nghĩ tới các công thức."},
        "s2_check": ["Em có phản ví dụ số cụ thể không?", "Em đã chỉ ra chính xác bước biến đổi sai chưa?", "Em có phân biệt được căn của tổng với tổng các căn không?"],
        "s3": "Không dùng chatbot, rút gọn C = √75 − √27 + 2√12. Trình bày đủ các bước biến đổi.",
        "teacher_key": "C = 5√3 − 3√3 + 4√3 = 6√3.",
    },
    "quadratic": {
        "title": "Giải phương trình bậc hai một ẩn",
        "topic": "Đại số – Toán 9 KNTT",
        "duration": "18–22 phút",
        "s0": "Giải phương trình x² − 5x + 6 = 0. Một bạn chỉ tìm được nghiệm x = 2 và dừng lại. Em hãy kiểm tra và hoàn thiện lập luận.",
        "misconception": "Bỏ sót nghiệm khi giải phương trình bậc hai.",
        "hints": [
            "Tìm được một nghiệm đã đủ để kết luận về toàn bộ tập nghiệm của phương trình bậc hai chưa?",
            "Em hãy thử phân tích x² − 5x + 6 thành tích hai nhân tử bậc nhất.",
            "Hãy kiểm tra xem tích (x − 2)(x − 3) có bằng vế trái không; sau đó xét từng thừa số bằng 0."
        ],
        "focus_hints": {"one_root":"Em hãy thử thay thêm một giá trị khác hoặc phân tích thành tích để kiểm tra liệu có nghiệm thứ hai.", "stuck":"Em có thể tìm hai số có tổng bằng 5 và tích bằng 6 không?"},
        "s2_check": ["Em đã xác định đủ các nghiệm chưa?", "Có bước biến đổi tương đương nào cần giải thích không?", "Em có thể thay lại từng nghiệm vào phương trình ban đầu không?"],
        "s3": "Không dùng chatbot, giải phương trình x² − 7x + 12 = 0 và kiểm tra đầy đủ các nghiệm.",
        "teacher_key": "(x − 3)(x − 4) = 0 nên x = 3 hoặc x = 4.",
    },
    "system": {
        "title": "Giải hệ hai phương trình bậc nhất hai ẩn",
        "topic": "Đại số – Toán 9 KNTT",
        "duration": "18–22 phút",
        "s0": "Giải hệ x + y = 7; 2x − y = 5. Trình bày cách chọn phép thế hoặc cộng đại số, đồng thời kiểm tra lại nghiệm.",
        "misconception": "Cộng sai dấu hoặc không thử lại nghiệm của hệ.",
        "hints": [
            "Nếu cộng hai phương trình theo từng vế, biến nào sẽ được triệt tiêu?",
            "Em hãy cộng hai phương trình và kiểm tra dấu của các hạng tử chứa y.",
            "Từ x + y = 7 và 2x − y = 5, hãy tự lập phương trình chỉ còn một ẩn rồi thế ngược vào một phương trình ban đầu."
        ],
        "focus_hints": {"sign_error":"Khi cộng vế theo vế, +y và −y cho kết quả gì?", "stuck":"Em thử chọn phương pháp cộng đại số vì hai hệ số của y đối nhau."},
        "s2_check": ["Phép biến đổi hệ có tương đương không?", "Em có kiểm tra dấu khi cộng hai phương trình?", "Cặp nghiệm có thỏa mãn cả hai phương trình ban đầu?"],
        "s3": "Không dùng chatbot, giải hệ x + y = 9; 2x − y = 6. Kiểm tra kết quả.",
        "teacher_key": "Cộng hai phương trình được 3x = 15, x = 5; suy ra y = 4. Thử lại cả hai phương trình.",
    },
}


def get_task(task_id: str):
    return TASKS[task_id]
