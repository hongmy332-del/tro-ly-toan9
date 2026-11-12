"""Học liệu tự biên soạn cho TOÀN BỘ CHƯƠNG V – ĐƯỜNG TRÒN, Toán 9 KNTT.

Không sao chép đề bài/lời giải SGK. Khung nội dung: Bài 13–17 và luyện tập
liên bài. Đáp án ở kho giáo viên, không gửi trực tiếp vào câu hỏi của học sinh.
"""
from __future__ import annotations
import re
import unicodedata

TOPIC_NAME = "Chương V – Đường tròn (Toán 9 Kết nối tri thức)"
LESSONS = {
    "b13": {
        "title": "Bài 13 · Mở đầu về đường tròn", "short": "Đường tròn và đối xứng", "icon": "◎",
        "summary": "Đường tròn (O; R), vị trí điểm so với đường tròn, bán kính – đường kính và tính đối xứng.",
        "concepts": [
            ("Nhận diện", "Đường tròn (O; R) gồm các điểm M sao cho OM = R. Phân biệt đường tròn (đường biên) với hình tròn (cả phần trong)."),
            ("Vị trí điểm", "Với R > 0: OM < R thì M trong đường tròn; OM = R thì M thuộc đường tròn; OM > R thì M ở ngoài."),
            ("Bán kính / đường kính", "Đường kính đi qua tâm và có hai đầu thuộc đường tròn; độ dài D = 2R. Mọi bán kính cùng một đường tròn bằng nhau."),
            ("Đối xứng", "O là tâm đối xứng của đường tròn. Mọi đường thẳng đi qua O đều là trục đối xứng của đường tròn."),
        ],
        "misconceptions": ["Nhầm hình tròn với đường tròn", "Cho rằng điểm nằm trong là điểm thuộc đường tròn", "Nhầm bán kính với đường kính", "Nhầm chỉ một đường kính là trục đối xứng"],
        "keywords": ["đường tròn", "hình tròn", "tâm đối xứng", "trục đối xứng", "bán kính", "đường kính", "điểm thuộc", "trong ngoài đường tròn"],
        "foundational_question": "Em có thể xác định tâm O, bán kính R và xem điểm đang xét cách O bao nhiêu không?",
    },
    "b14": {
        "title": "Bài 14 · Cung và dây của một đường tròn", "short": "Cung, dây và góc ở tâm", "icon": "⌒",
        "summary": "Phân biệt cung – dây, số đo cung, góc ở tâm, và các tính chất cơ bản của dây.",
        "concepts": [
            ("Cung / dây", "Dây AB là đoạn thẳng nối hai điểm A, B của đường tròn; cung AB là một phần đường tròn giữa A và B."),
            ("Cung – góc ở tâm", "Số đo cung nhỏ AB bằng số đo góc ở tâm AOB chắn cung đó. Hai cung cùng đầu mút có thể là cung nhỏ và cung lớn."),
            ("Dây và khoảng cách tâm", "Đường vuông góc từ tâm tới dây (không phải đường kính) đi qua trung điểm dây; có thể áp dụng Pythagore trong tam giác vuông."),
            ("So sánh dây", "Trong cùng đường tròn, các dây bằng nhau cách đều tâm; dây gần tâm hơn thì dài hơn; đường kính là dây dài nhất."),
        ],
        "misconceptions": ["Nhầm dây với cung", "Lấy số đo góc ở tâm cho cung lớn", "Áp dụng Pythagore khi chưa dựng đường vuông góc", "Cho rằng dây nào cũng đi qua tâm"],
        "keywords": ["cung", "dây", "góc ở tâm", "cung nhỏ", "cung lớn", "vuông góc với dây", "trung điểm dây", "khoảng cách từ tâm"],
        "foundational_question": "Em đang dùng tính chất của cung, của dây hay của góc ở tâm? Hãy chỉ ra đúng đối tượng trên hình trước nhé.",
    },
    "b15": {
        "title": "Bài 15 · Độ dài cung tròn, diện tích hình quạt và vành khuyên", "short": "Cung – quạt – vành khuyên", "icon": "◔",
        "summary": "Tính độ dài cung, diện tích quạt tròn và diện tích hình vành khuyên theo bán kính, góc ở tâm.",
        "concepts": [
            ("Độ dài cung", "Với góc ở tâm n độ (0 ≤ n ≤ 360): l = (n/360)·2πR = πRn/180; đơn vị độ dài."),
            ("Diện tích hình quạt", "S = (n/360)·πR²; đơn vị diện tích, không nhầm với l."),
            ("Diện tích vành khuyên", "Giữa hai đường tròn đồng tâm bán kính R > r ≥ 0: S = π(R² − r²)."),
            ("Phân biệt đơn vị", "Góc n phải theo độ khi dùng công thức chia 360; độ dài là cm/m, diện tích là cm²/m²."),
        ],
        "misconceptions": ["Dùng πR² cho độ dài cung", "Quên chia 360", "Nhầm bán kính với đường kính", "Lấy π(R − r)² làm diện tích vành khuyên"],
        "keywords": ["độ dài cung", "quạt tròn", "vành khuyên", "diện tích", "góc ở tâm", "pi", "chu vi", "bánh xe", "mặt đồng hồ"],
        "foundational_question": "Bài yêu cầu độ dài hay diện tích? Em xác định bán kính và số đo góc ở tâm trước nhé.",
    },
    "b16": {
        "title": "Bài 16 · Vị trí tương đối của đường thẳng và đường tròn", "short": "Tiếp tuyến và cát tuyến", "icon": "⊙",
        "summary": "So sánh khoảng cách từ tâm đến đường thẳng với bán kính; tiếp tuyến và tính chất liên quan.",
        "concepts": [
            ("Ba vị trí", "Gọi h là khoảng cách từ O đến đường thẳng a: h < R ⇒ cắt tại hai điểm; h = R ⇒ tiếp xúc; h > R ⇒ không giao điểm."),
            ("Tiếp tuyến", "Đường thẳng tiếp xúc đường tròn tại A vuông góc với bán kính OA; đảo lại, đường thẳng vuông góc OA tại A thuộc đường tròn là tiếp tuyến."),
            ("Hai tiếp tuyến", "Từ điểm M ngoài (O), nếu MA, MB là hai tiếp tuyến tại A, B thì MA = MB."),
            ("Bài tính toán", "Dựng OH ⟂ a để dùng tam giác vuông. Chỉ áp dụng tính chất sau khi xác nhận chân H và các dữ kiện."),
        ],
        "misconceptions": ["Nhầm khoảng cách từ tâm đến đường thẳng với độ dài đoạn bất kỳ", "Cho h < R là tiếp tuyến", "Thiếu điều kiện A thuộc đường tròn", "Suy ra hai tiếp tuyến bằng nhau khi không cùng xuất phát từ một điểm"],
        "keywords": ["đường thẳng", "tiếp tuyến", "cát tuyến", "tiếp điểm", "khoảng cách từ tâm", "tiếp xúc", "vuông góc bán kính", "hai tiếp tuyến"],
        "foundational_question": "Em đã dựng đoạn vuông góc từ tâm O đến đường thẳng chưa? Độ dài đó so với bán kính R thế nào?",
    },
    "b17": {
        "title": "Bài 17 · Vị trí tương đối của hai đường tròn", "short": "Hai đường tròn", "icon": "◉",
        "summary": "So sánh khoảng cách hai tâm d với tổng và hiệu hai bán kính để phân loại số điểm chung.",
        "concepts": [
            ("Hai đường tròn cắt nhau", "Với R ≥ r > 0, hai đường tròn có hai điểm chung khi |R−r| < d < R+r."),
            ("Tiếp xúc ngoài / trong", "Tiếp xúc ngoài khi d = R+r; tiếp xúc trong khi d = |R−r| > 0. Nếu d=0 và R=r, hai đường tròn trùng nhau."),
            ("Không có điểm chung", "Rời nhau ở ngoài nếu d > R+r; chứa nhau không tiếp xúc khi 0 ≤ d < |R−r|. Trường hợp d=0, R≠r: đồng tâm, không điểm chung."),
            ("Cách phân loại", "Tính hai mốc |R−r|, R+r, rồi xác định vị trí d trên trục số; nên kiểm tra hình vẽ và số điểm chung."),
        ],
        "misconceptions": ["Chỉ xét d < R+r để kết luận cắt nhau", "Nhầm tiếp xúc trong với cắt nhau", "Cho rằng hai đường tròn đồng tâm luôn trùng nhau", "Quên xét cả hiệu hai bán kính"],
        "keywords": ["hai đường tròn", "khoảng cách hai tâm", "cắt nhau", "tiếp xúc trong", "tiếp xúc ngoài", "đồng tâm", "trùng nhau", "bán kính lớn bán kính nhỏ"],
        "foundational_question": "Em đã có R, r và khoảng cách hai tâm d chưa? Hãy tính cả |R−r| và R+r rồi thử so sánh với d.",
    },
}


def _e(code, lesson, title, problem, answer, hints, keywords, level=1):
    assert len(hints) == 3
    return {"id": code, "lesson": lesson, "title": title, "problem": problem,
            "teacher_answer": answer, "hints": hints, "keywords": keywords, "level": level,
            "original": True}

EXERCISES = [
    # Bài 13 – 8 bài tự biên soạn
    _e("13-01","b13","Điểm nằm ở đâu?","Cho đường tròn (O; 5 cm), điểm M thỏa mãn OM = 3 cm. M ở vị trí nào so với đường tròn?","M nằm trong đường tròn vì OM = 3 < 5 = R.",["OM được so sánh với đại lượng nào của đường tròn?","Em so sánh 3 và 5 xem số nào lớn hơn nhé.","Điểm cách tâm một khoảng nhỏ hơn bán kính sẽ ở đâu so với đường tròn?"],["điểm", "trong", "bán kính"]),
    _e("13-02","b13","Điểm thuộc đường tròn","Đường tròn tâm I bán kính 4 cm, điểm A cách I đúng 4 cm. A nằm trong, trên hay ngoài đường tròn?","A thuộc đường tròn do IA = R = 4 cm.",["Thế nào là điểm thuộc đường tròn?","Em so sánh IA với bán kính.","Khi IA bằng R, khoảng cách ấy đúng bằng điều kiện của tập hợp điểm nào?"],["thuộc", "điểm"]),
    _e("13-03","b13","Tìm đường kính","Một đường tròn có bán kính 6,5 cm. Tính độ dài đường kính.","D = 2R = 13 cm.",["Đường kính dài gấp bao nhiêu lần bán kính?","Em viết hệ thức giữa D và R.","Thay R = 6,5 vào công thức D = 2R và kiểm tra đơn vị."],["đường kính", "bán kính"]),
    _e("13-04","b13","Hai điểm ngoài","Cho (O; 3 cm), OA = 5 cm, OB = 3 cm. Trong hai điểm A, B, điểm nào nằm ngoài đường tròn?","A nằm ngoài (5 > 3); B thuộc đường tròn (3 = R).",["Em cần so sánh OA và OB với bán kính nào?","Xét riêng từng điểm thay vì suy luận chung.","Với OA > R và OB = R, em gọi tên hai vị trí khác nhau thế nào?"],["ngoài", "thuộc", "điểm"]),
    _e("13-05","b13","Tâm đối xứng","Đường tròn tâm O có điểm A thuộc đường tròn. Lấy B đối xứng với A qua O. B có thuộc đường tròn không? Vì sao?","Có. Vì O là trung điểm AB, OB = OA = R; nên B thuộc (O).",["Đối xứng A qua O có nghĩa là O giữ vai trò gì với AB?","Em suy ra OA và OB có quan hệ độ dài gì?","Nếu OA = R và OB = OA, B thỏa điều kiện thuộc đường tròn chứ?"],["tâm đối xứng", "đối xứng", "điểm"],2),
    _e("13-06","b13","Trục đối xứng","Đường thẳng d đi qua tâm O của đường tròn. d có phải trục đối xứng của đường tròn không? Giải thích ngắn gọn.","Có. Phép đối xứng qua mọi đường thẳng đi qua tâm O giữ nguyên đường tròn.",["Trục đối xứng phải biến đường tròn thành hình nào?","Với d đi qua O, điểm O biến thành đâu qua đối xứng trục?","Phản chiếu một điểm cách O bằng R có tạo điểm cũng cách O bằng R không?"],["trục đối xứng", "tâm"],2),
    _e("13-07","b13","Phân biệt hình tròn","Điểm P cách tâm O 2 cm, đường tròn có bán kính 5 cm. P thuộc hình tròn hay thuộc đường tròn?","P thuộc hình tròn (phần trong), nhưng không thuộc đường tròn vì OP < R.",["Em phân biệt tập hợp điểm có khoảng cách đúng R và không quá R nhé.","P cách O ít hơn R, vậy P ở biên hay phía trong?","Hình tròn bao gồm cả phía trong, còn đường tròn chỉ gồm những điểm nào?"],["hình tròn", "đường tròn", "trong"],2),
    _e("13-08","b13","Bài tổng hợp","Đường tròn (O) có đường kính AB = 12 cm, điểm M cách tâm O một khoảng 7 cm. Xác định vị trí M so với (O).","R = AB/2 = 6 cm; OM = 7 > 6, M ở ngoài.",["Đề cho đường kính, còn tiêu chí xét điểm cần đại lượng nào?","Tính bán kính từ AB = 12 cm.","Em so sánh OM = 7 với R = 6 rồi kết luận."],["đường kính", "ngoài", "điểm"],2),
    # Bài 14 – 8 bài
    _e("14-01","b14","Cung và góc ở tâm","Đường tròn (O) có góc ở tâm AOB = 80°. Số đo cung nhỏ AB là bao nhiêu?","80°.",["Số đo cung nhỏ gắn với góc nào?","Hai đầu cung là A, B; em tìm góc ở tâm tương ứng.","Góc ở tâm 80° (nhỏ hơn 180°) chắn cung nào?"],["góc ở tâm", "cung nhỏ"]),
    _e("14-02","b14","Cung lớn","Một cung nhỏ AB có số đo 110°. Tính số đo cung lớn AB cùng hai đầu mút.","360° − 110° = 250°.",["Một vòng tròn có số đo tổng cộng bao nhiêu độ?","Hai cung chung đầu mút AB tạo thành cả đường tròn.","Lấy 360° trừ số đo cung nhỏ nhé."],["cung lớn", "cung nhỏ"],2),
    _e("14-03","b14","Nửa dây","Dây AB dài 12 cm trong (O). Biết OH vuông góc AB tại H. Tính AH.","H là trung điểm AB; AH = 12/2 = 6 cm.",["Đường vuông góc kẻ từ tâm tới dây có tính chất gì?","OH ⟂ AB nên H chia dây AB thành hai phần như thế nào?","AB = 12 thì AH bằng bao nhiêu phần của AB?"],["vuông góc", "dây", "trung điểm"]),
    _e("14-04","b14","Từ dây tìm khoảng cách tâm","Trong đường tròn bán kính 10 cm, dây AB = 16 cm; OH ⟂ AB tại H. Tính OH.","AH = 8; OH² = OA² − AH² = 100 − 64 = 36; OH = 6 cm.",["Tam giác OHA vuông tại điểm nào?","Từ OH ⟂ AB suy ra AH dài bao nhiêu?","Áp dụng định lý Pythagore cho tam giác OHA: OA = 10, AH = 8."],["khoảng cách từ tâm", "dây", "pythagore"],2),
    _e("14-05","b14","So sánh hai dây","Trong cùng một đường tròn, dây AB cách tâm 3 cm và dây CD cách tâm 5 cm. Dây nào dài hơn?","AB dài hơn CD vì dây gần tâm hơn thì dài hơn.",["Hai dây nằm trong mấy đường tròn?","Dây gần tâm hơn thì dài hay ngắn hơn?","Em so sánh khoảng cách 3 và 5 cm rồi chọn dây gần tâm."],["so sánh dây", "khoảng cách từ tâm"]),
    _e("14-06","b14","Đường kính là dây lớn nhất","Trong đường tròn bán kính 7 cm, độ dài dây lớn nhất có thể là bao nhiêu?","Đường kính 2R = 14 cm.",["Dây nào đi qua tâm?","Có dây nào dài hơn đường kính không?","Từ R = 7, hãy tính đường kính."],["đường kính", "dây"],2),
    _e("14-07","b14","Chứng minh trung điểm","Trong đường tròn (O), dây MN không qua tâm và K là trung điểm MN. Giải thích vì sao OK vuông góc MN.","OM = ON (bán kính); KM = KN; OK chung. Tam giác OMK và ONK bằng nhau ⇒ góc MKO = OKN; do hai góc kề bù nên cùng 90°.",["Hai tam giác nào có các cạnh tương ứng bằng nhau?","Xét tam giác OMK và ONK, tìm ba cặp cạnh bằng nhau.","Hai góc kề nhau trên đường thẳng MN nếu bằng nhau sẽ bằng mấy độ?"],["trung điểm", "vuông góc", "chứng minh"],3),
    _e("14-08","b14","Góc ở tâm và cung lớn","Góc ở tâm MON = 135°. Hãy tính số đo cung nhỏ MN và cung lớn MN.","Cung nhỏ: 135°; cung lớn: 360° − 135° = 225°.",["Một góc ở tâm không quá 180° chắn cung nhỏ nào?","Số đo cung nhỏ MN là số đo góc gì?","Muốn tìm cung lớn, em lấy số đo cả đường tròn trừ cung nhỏ."],["góc ở tâm", "cung lớn", "cung nhỏ"],2),
    # Bài 15 – 8 bài
    _e("15-01","b15","Cung một phần tư","Tính độ dài cung 90° của đường tròn bán kính 8 cm (lấy π theo ký hiệu).","l = 2π·8·90/360 = 4π cm.",["Cung 90° chiếm bao nhiêu phần vòng tròn?","Chu vi đường tròn bán kính 8 là bao nhiêu?","Lấy một phần tư của 2πR để ra độ dài cung."],["độ dài cung", "90 độ"],1),
    _e("15-02","b15","Quạt một phần tư","Tính diện tích hình quạt góc ở tâm 90°, bán kính 6 cm.","S = π·6²·90/360 = 9π cm².",["Đề hỏi diện tích hay độ dài?","Hình quạt 90° chiếm bao nhiêu phần diện tích hình tròn?","Lấy πR² chia 4 và kiểm tra đơn vị cm²."],["hình quạt", "diện tích"],1),
    _e("15-03","b15","Cung 60 độ","Đường tròn R = 12 cm có cung nhỏ số đo 60°. Tính độ dài cung ấy.","l = 2π·12·60/360 = 4π cm.",["Em biết hai đại lượng nào dùng để tính độ dài cung?","60° là bao nhiêu phần của 360°?","Độ dài cung = phần góc × chu vi đường tròn."],["độ dài cung", "60 độ"],1),
    _e("15-04","b15","Quạt 120 độ","Một hình quạt tròn bán kính 9 cm có góc ở tâm 120°. Tính diện tích.","S = π·9²·120/360 = 27π cm².",["Góc 120° chiếm phần mấy hình tròn?","Tính trước diện tích hình tròn đầy đủ.","Lấy (120/360)·π·81 và ghi đơn vị diện tích."],["hình quạt", "120 độ", "diện tích"],2),
    _e("15-05","b15","Vành khuyên cơ bản","Vành khuyên giữa hai đường tròn đồng tâm bán kính 5 cm và 3 cm. Tính diện tích.","S = π(5² − 3²) = 16π cm².",["Diện tích vành khuyên là phần nào của hai hình tròn?","Cần lấy diện tích hình tròn lớn trừ phần nào?","Dùng πR² − πr² với R = 5, r = 3."],["vành khuyên", "diện tích"],2),
    _e("15-06","b15","Tính góc từ cung","Đường tròn bán kính 6 cm có cung dài 2π cm. Cung đó có số đo bao nhiêu độ?","n = 180l/(πR) = 180·2π/(6π) = 60°.",["Em nhớ công thức độ dài cung theo góc n không?","Trong l = πRn/180, đại lượng cần tìm là n.","Thay R = 6 và l = 2π, giải phương trình theo n."],["độ dài cung", "góc", "tính góc"],3),
    _e("15-07","b15","Bánh xe","Một bánh xe có bán kính 35 cm. Tính độ dài cung trên vành tương ứng với góc ở tâm 180°.","l = π·35 cm.",["Quay 180° tương ứng mấy phần vòng?","Chu vi bánh xe tính theo bán kính thế nào?","Lấy nửa chu vi 2π·35."],["bánh xe", "độ dài cung"],2),
    _e("15-08","b15","Vành khuyên ứng dụng","Một vành khuyên có đường kính ngoài 20 cm, đường kính trong 12 cm. Tính diện tích.","R = 10, r = 6; S = π(100 − 36) = 64π cm².",["Đề cho đường kính, công thức vành khuyên cần đại lượng nào?","Hãy đổi đường kính ngoài/trong thành hai bán kính.","Thay R = 10, r = 6 vào π(R² − r²)."],["vành khuyên", "đường kính", "diện tích"],3),
    # Bài 16 – 8 bài
    _e("16-01","b16","Cát tuyến","Đường tròn (O; 5 cm), khoảng cách từ O đến đường thẳng a bằng 3 cm. a có bao nhiêu điểm chung với đường tròn?","Vì h = 3 < R = 5, a cắt đường tròn tại 2 điểm.",["Đại lượng nào quyết định vị trí đường thẳng với đường tròn?","So sánh h với R.","h nhỏ hơn R tương ứng đường thẳng đi qua phần nào của đường tròn?"],["cát tuyến", "đường thẳng", "khoảng cách"],1),
    _e("16-02","b16","Tiếp tuyến","Đường tròn bán kính 4 cm, đường thẳng b cách tâm đúng 4 cm. b có vị trí nào với đường tròn?","b là tiếp tuyến vì h = R = 4.",["Đề cho khoảng cách tâm đến đường thẳng bằng mấy?","Em so sánh h với R.","Trường hợp h = R có mấy điểm chung?"],["tiếp tuyến", "tiếp xúc"],1),
    _e("16-03","b16","Không giao nhau","Đường tròn (O; 6 cm), đường thẳng m cách tâm O một khoảng 8 cm. Tìm số điểm chung.","Không có điểm chung vì 8 > 6.",["Khoảng cách từ tâm đến m đã được cho chưa?","So sánh h = 8 với R = 6.","Đường thẳng cách tâm xa hơn bán kính có cắt hình tròn không?"],["đường thẳng", "không giao", "khoảng cách"],1),
    _e("16-04","b16","Chứng minh tiếp tuyến","A thuộc (O; R). Đường thẳng d đi qua A và vuông góc OA. Chứng minh d tiếp xúc (O).","Vì A thuộc (O) và d ⟂ OA tại A, d là tiếp tuyến của (O) tại A.",["Để một đường thẳng là tiếp tuyến tại A, có điều kiện nào?","Em đã có A thuộc đường tròn chưa?","d vuông góc bán kính OA tại A có đủ theo dấu hiệu nhận biết không?"],["chứng minh tiếp tuyến", "vuông góc"],2),
    _e("16-05","b16","Hai tiếp tuyến","Từ điểm M ngoài (O) kẻ hai tiếp tuyến MA, MB (A, B là tiếp điểm). MA = 7 cm. Tính MB.","MB = MA = 7 cm.",["MA và MB được kẻ từ cùng điểm nào?","Hai đoạn tiếp tuyến xuất phát từ một điểm ngoài có tính chất gì?","Áp dụng MA = MB khi MA = 7 cm."],["hai tiếp tuyến", "tính độ dài"],2),
    _e("16-06","b16","Độ dài tiếp tuyến","Cho (O; 5 cm), M ở ngoài sao cho OM = 13 cm. MA là tiếp tuyến tại A. Tính MA.","OA ⟂ MA; MA² = OM² − OA² = 169 − 25 = 144; MA = 12 cm.",["Bán kính OA có quan hệ gì với tiếp tuyến MA?","Tam giác OAM có vuông không? Cạnh nào là cạnh huyền?","Dùng Pythagore với OM = 13, OA = 5 để tìm MA."],["tiếp tuyến", "pythagore", "độ dài"],3),
    _e("16-07","b16","Tìm bán kính khi tiếp xúc","Khoảng cách từ O đến đường thẳng t là 7 cm; t là tiếp tuyến của đường tròn tâm O. Tìm bán kính.","R = 7 cm vì khoảng cách tâm đến tiếp tuyến bằng R.",["Trong trường hợp tiếp xúc h liên hệ R thế nào?","Em viết điều kiện h = R.","Thay h = 7 cm vào quan hệ vừa nêu."],["bán kính", "tiếp tuyến", "khoảng cách"],2),
    _e("16-08","b16","Bác bỏ kết luận sai","Một bạn nói: 'Nếu đường thẳng a cắt đường tròn thì khoảng cách từ tâm đến a bằng R'. Em có đồng ý không? Vì sao?","Không. Nếu cắt tại hai điểm thì h < R; h = R là trường hợp tiếp xúc tại một điểm.",["Em phân biệt cắt tại hai điểm và tiếp xúc tại một điểm nhé.","Trong hai trường hợp, h so với R khác nhau ra sao?","Vẽ một đường qua tâm, h = 0 < R: có phải tiếp tuyến không?"],["sai lầm", "cát tuyến", "tiếp tuyến"],2),
    # Bài 17 – 8 bài
    _e("17-01","b17","Tiếp xúc trong","Hai đường tròn có R = 5 cm, r = 3 cm, khoảng cách hai tâm d = 2 cm. Xác định vị trí tương đối.","d = |R−r| = 2 > 0: tiếp xúc trong, 1 điểm chung.",["Em có đủ R, r, d chưa?","Tính cả tổng và hiệu hai bán kính.","So sánh d = 2 với |5−3|, rồi dùng số điểm chung để phân loại."],["hai đường tròn", "tiếp xúc trong", "bán kính"],1),
    _e("17-02","b17","Hai điểm chung","Hai đường tròn có R = 6 cm, r = 2 cm, d = 5 cm. Có bao nhiêu điểm chung?","|R−r| = 4 < 5 < R+r = 8, nên cắt nhau tại 2 điểm.",["Hai mốc cần dùng để xét cắt nhau là gì?","Tính |6−2| và 6+2.","Đặt d = 5 vào khoảng giữa hai mốc và xét bất đẳng thức nghiêm."],["hai đường tròn", "cắt nhau", "khoảng cách"],1),
    _e("17-03","b17","Tiếp xúc ngoài","Hai đường tròn có bán kính 4 cm và 3 cm, d = 7 cm. Xác định vị trí.","d = R+r = 7: tiếp xúc ngoài, 1 điểm chung.",["Tính tổng hai bán kính.","So sánh d với R+r và |R−r|.","Khi d bằng tổng R+r, có mấy điểm chung và thuộc loại tiếp xúc nào?"],["tiếp xúc ngoài", "hai đường tròn"],1),
    _e("17-04","b17","Rời nhau ở ngoài","Hai đường tròn có bán kính 2 cm, 5 cm, d = 10 cm. Có điểm chung không?","d = 10 > 7 = R+r: ngoài nhau, không có điểm chung.",["Em cần so d với tổng hay hiệu khi hai đường tròn ở xa nhau?","Tính R+r.","d lớn hơn tổng hai bán kính có đủ để chúng chạm nhau không?"],["rời nhau", "ngoài nhau", "hai đường tròn"],1),
    _e("17-05","b17","Chứa nhau không tiếp xúc","Hai đường tròn có bán kính 8 cm và 3 cm, khoảng cách hai tâm d = 2 cm. Hỏi có điểm chung không?","|R−r| = 5; d = 2 < 5 nên đường tròn nhỏ nằm trong đường tròn lớn, không điểm chung.",["Em xét hiệu hai bán kính trước nhé.","So sánh d = 2 với |8−3|.","Nếu khoảng cách hai tâm còn nhỏ hơn hiệu bán kính, đường tròn nhỏ đã chạm đường tròn lớn chưa?"],["chứa nhau", "không giao", "hai đường tròn"],2),
    _e("17-06","b17","Đồng tâm không trùng","Hai đường tròn có cùng tâm, bán kính lần lượt 4 cm và 6 cm. Hai đường tròn có trùng nhau không?","Không. d = 0 nhưng R≠r nên là hai đường tròn đồng tâm khác bán kính, không điểm chung.",["Đồng tâm có phải lúc nào cũng trùng nhau không?","Để hai đường tròn trùng, cần so sánh những đại lượng nào?","d = 0 rồi, nhưng R và r có bằng nhau không?"],["đồng tâm", "trùng nhau"],2),
    _e("17-07","b17","Khoảng giá trị nguyên","Hai đường tròn có R = 6 cm, r = 2 cm, d là số nguyên dương. Tìm mọi d để cắt nhau tại hai điểm.","4 < d < 8 nên d ∈ {5, 6, 7} cm.",["Điều kiện cắt tại hai điểm là bất đẳng thức nghiêm nào?","Tính |R−r| và R+r.","Liệt kê những số nguyên dương nằm giữa 4 và 8, không lấy hai mốc."],["giá trị nguyên", "cắt nhau", "bất đẳng thức"],3),
    _e("17-08","b17","Sai lầm chỉ xét tổng","Một bạn viết: 'd < R+r thì hai đường tròn luôn cắt nhau tại hai điểm'. Em hãy tìm phản ví dụ bằng hai đường tròn có bán kính 7 cm, 3 cm.","Chọn d = 4 (hoặc d < 4): d < 10 nhưng d=|7−3|=4 chỉ tiếp xúc trong (hoặc d<4 thì chứa nhau), nên khẳng định sai.",["Muốn bác bỏ một câu nói 'luôn', em cần tìm điều gì?","Ngoài R+r, thử tính |7−3|.","Chọn d = |7−3| = 4: d < 10 nhưng số điểm chung là bao nhiêu?"],["sai lầm", "phản ví dụ", "hai đường tròn", "cắt nhau"],3),
]

assert len(EXERCISES) == 40
assert len({x["id"] for x in EXERCISES}) == 40


def normalize(text: str) -> str:
    s = unicodedata.normalize("NFD", (text or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").replace("đ", "d")
    return " ".join(re.findall(r"[a-z0-9]+", s))


def lesson_exercises(lesson_id: str) -> list[dict]:
    return [e for e in EXERCISES if e["lesson"] == lesson_id]


def guess_lesson(problem: str, selected: str = "auto") -> tuple[str | None, int]:
    """Dò dạng toán theo thuật ngữ; không suy diễn rằng đã hiểu hoàn toàn đề."""
    if selected in LESSONS:
        return selected, 99
    p = normalize(problem)
    if not p:
        return None, 0
    scores: dict[str, int] = {}
    for lid, lesson in LESSONS.items():
        score = 0
        for kw in lesson["keywords"]:
            k = normalize(kw)
            if k and k in p:
                score += 2 + min(2, len(k.split()))
        # Thêm trọng số cho các dấu hiệu đủ đặc trưng.
        tokens = {
            "b13": ["tâm đối xứng", "trục đối xứng", "thuộc đường tròn"],
            "b14": ["cung nhỏ", "cung lớn", "dây", "góc ở tâm"],
            "b15": ["hình quạt", "vành khuyên", "độ dài cung", "diện tích quạt"],
            "b16": ["tiếp tuyến", "đường thẳng", "cát tuyến", "tiếp điểm"],
            "b17": ["hai đường tròn", "hai tâm", "tiếp xúc trong", "tiếp xúc ngoài", "r+r", "r-r"],
        }
        for term in tokens[lid]:
            if normalize(term) in p:
                score += 6
        scores[lid] = score
    best = max(scores, key=scores.get)
    if scores[best] < 3:
        return None, scores[best]
    return best, scores[best]


def retrieve(problem: str, lesson_id: str | None, limit: int = 3) -> list[dict]:
    p = normalize(problem)
    words = set(p.split())
    selected = [e for e in EXERCISES if lesson_id is None or e["lesson"] == lesson_id]
    def score(e):
        kw_score = sum(4 for kw in e["keywords"] if normalize(kw) in p)
        terms = set(normalize(e["title"]+" "+e["problem"]).split())
        overlap = len(words & terms - {"cho", "tinh", "hai", "mot", "co", "va", "cua", "duong", "tron", "cm", "o", "r", "the", "nao", "la", "de"})
        return kw_score + overlap
    ranked = sorted(selected, key=lambda x: (-score(x), x["id"]))
    return ranked[:limit]


def safe_teacher_context(problem: str, lesson_id: str | None) -> dict:
    """Chỉ kiến thức nền, lỗi điển hình và câu gợi ý; KHÔNG gửi đáp án bài mẫu vào prompt học sinh."""
    lesson = LESSONS.get(lesson_id)
    examples = retrieve(problem, lesson_id, limit=3)
    return {
        "lesson": lesson_id or "chưa xác định chắc chắn",
        "title": lesson["title"] if lesson else "Chương V – Đường tròn",
        "core": [f"{n}: {txt}" for n, txt in (lesson["concepts"] if lesson else [])],
        "mistakes": lesson["misconceptions"] if lesson else [],
        "reference_questions": [{"type": e["title"], "hint_1": e["hints"][0], "hint_2": e["hints"][1]} for e in examples],
    }
