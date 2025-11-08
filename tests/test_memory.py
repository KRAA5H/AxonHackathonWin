import unittest
from src.games.memory import generate_sequence


class TestGenerateSequence(unittest.TestCase):
    def test_length_and_choices(self):
        seq = generate_sequence(5, choices=("a", "b", "c"))
        self.assertEqual(len(seq), 5)
        for s in seq:
            self.assertIn(s, ("a", "b", "c"))

    def test_zero_length(self):
        self.assertEqual(generate_sequence(0), [])

    def test_negative_length_raises(self):
        with self.assertRaises(ValueError):
            generate_sequence(-1)


if __name__ == "__main__":
    unittest.main()
