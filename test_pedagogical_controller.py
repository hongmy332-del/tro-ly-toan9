import unittest
from pedagogical_controller import (
    analyze_pedagogical_state, pedagogy_instruction,
    STAGE_EXPLORING, STAGE_CONCLUDED, STAGE_WRITING,
)

class PedagogyTests(unittest.TestCase):
    def state(self, txt, messages=None, previous_state=None):
        return analyze_pedagogical_state(txt, messages, previous_state)

    def test_unknown_start(self):
        self.assertEqual(self.state("Em chưa biết bắt đầu từ đâu")['stage'], STAGE_EXPLORING)

    def test_dont_confuse_unknown_solution_with_writing(self):
        self.assertEqual(self.state("Em chưa biết lời giải") ["stage"], STAGE_EXPLORING)

    def test_conclusion_circle(self):
        self.assertEqual(self.state("Em nghĩ hai đường tròn tiếp xúc ngoài và có một điểm chung")['stage'], STAGE_CONCLUDED)

    def test_writing_explicit(self):
        self.assertEqual(self.state("Em đã hiểu, hướng dẫn em trình bày lời giải cho chặt chẽ")['stage'], STAGE_WRITING)

    def test_writing_diacritics(self):
        self.assertEqual(self.state("Em chưa biết viết từng câu trong bài giải")['stage'], STAGE_WRITING)

    def test_writing_history(self):
        messages = [
            {'role': 'student', 'text': "Em đã biết OO' = R + r nên tiếp xúc ngoài"},
            {'role': 'assistant', 'text': "Em thử tính lại nhé"},
        ]
        self.assertEqual(self.state("Hãy hướng dẫn em cách trình bày", messages)['stage'], STAGE_WRITING)

    def test_no_assistant_evidence(self):
        messages = [{'role':'assistant', 'text': 'Hai đường tròn tiếp xúc ngoài'}]
        self.assertEqual(self.state("Em chưa biết bắt đầu", messages)['stage'], STAGE_EXPLORING)

    def test_writing_sticky(self):
        prior = {'stage': STAGE_WRITING}
        self.assertEqual(self.state("Ta có OO' = 8 cm", previous_state=prior)['stage'], STAGE_WRITING)

    def test_restart(self):
        prior = {'stage': STAGE_WRITING}
        self.assertEqual(self.state("Em muốn giải lại từ đầu", previous_state=prior)['stage'], STAGE_EXPLORING)

    def test_unverified(self):
        self.assertFalse(self.state("Hai đường tròn tiếp xúc ngoài")['conclusion_verified'])

    def test_instruction(self):
        p = pedagogy_instruction(self.state("Em muốn trình bày lời giải"))
        self.assertIn("T3", p)
        self.assertIn("MỘT", p)

if __name__ == '__main__':
    unittest.main()
