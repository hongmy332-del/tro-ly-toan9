"""Chạy bằng: python -m unittest -v test_khkt_v53.py"""
import unittest
from khkt_v53 import classify_b17, apply_v53


class TestV53Rules(unittest.TestCase):
    def test_unknown(self):
        self.assertEqual(classify_b17("")["code"], "U00")

    def test_help(self):
        self.assertEqual(classify_b17("Em chưa hiểu câu hỏi trước ạ")["code"], "H01")

    def test_missing_difference(self):
        self.assertEqual(classify_b17("Hai đường tròn cắt nhau vì d < R + r")["code"], "E01")

    def test_internal_touch_confused(self):
        self.assertEqual(classify_b17("Tiếp xúc trong khi d = R + r")["code"], "E02")

    def test_external_touch_confused(self):
        self.assertEqual(classify_b17("Tiếp xúc ngoài vì d = |R-r|")["code"], "E03")

    def test_do_not_misclassify_full_condition(self):
        self.assertEqual(classify_b17("Em thấy |R-r| < d < R+r nên hai đường tròn cắt nhau")["code"], "W00")

    def test_no_claim_of_correctness(self):
        result = apply_v53({"hint_level": 1}, student_step="d = R+r theo đề", lesson_id="b17")
        self.assertIn("chưa phát hiện", result["khkt_v53"]["observed_signal"].lower())
        self.assertIn("cần giáo viên", result["khkt_v53"]["validation_status"])

    def test_unrelated_lesson_preserves_level(self):
        result = apply_v53({"hint_level": 3}, student_step="Em chưa hiểu", lesson_id="b14")
        self.assertEqual(result["hint_level"], 3)
        self.assertEqual(result["khkt_v53"]["rule_id"], "OUT_OF_SCOPE")

    def test_repeat_help_escalates_only_as_needed(self):
        messages = [{"role": "student", "text": "Em chưa hiểu"}]
        result = apply_v53({"hint_level": 1}, student_step="Em vẫn chưa hiểu", lesson_id="b17", messages=messages)
        self.assertEqual(result["hint_level"], 2)

    def test_original_plan_unchanged(self):
        plan = {"hint_level": 1, "needs_work": "ban đầu"}
        apply_v53(plan, student_step="Hai đường tròn cắt nhau vì d < R+r", lesson_id="b17")
        self.assertEqual(plan, {"hint_level": 1, "needs_work": "ban đầu"})


if __name__ == "__main__":
    unittest.main()
