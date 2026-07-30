import unittest

from rot13_cli.core import caesar_shift


class TestCaesarShift(unittest.TestCase):
    def test_default_shift_is_rot13(self) -> None:
        self.assertEqual(caesar_shift("Hello, World!"), "Uryyb, Jbeyq!")

    def test_rot13_is_self_inverse(self) -> None:
        original = "The quick brown fox jumps over the lazy dog."
        once = caesar_shift(original)
        twice = caesar_shift(once)
        self.assertEqual(twice, original)

    def test_case_is_preserved(self) -> None:
        result = caesar_shift("AbCz")
        self.assertEqual(result[0], result[0].upper())
        self.assertEqual(result[2], result[2].upper())

    def test_non_letters_untouched(self) -> None:
        self.assertEqual(caesar_shift("123 !@# \n\t"), "123 !@# \n\t")

    def test_custom_shift(self) -> None:
        self.assertEqual(caesar_shift("abc", shift=1), "bcd")

    def test_negative_shift_reverses_positive(self) -> None:
        original = "attack at dawn"
        shifted = caesar_shift(original, shift=5)
        self.assertEqual(caesar_shift(shifted, shift=-5), original)

    def test_shift_normalizes_modulo_26(self) -> None:
        self.assertEqual(caesar_shift("a", shift=26), "a")
        self.assertEqual(caesar_shift("a", shift=27), "b")
        self.assertEqual(caesar_shift("a", shift=-1), "z")

    def test_wraps_at_alphabet_boundary(self) -> None:
        self.assertEqual(caesar_shift("xyz", shift=3), "abc")
        self.assertEqual(caesar_shift("XYZ", shift=3), "ABC")

    def test_empty_string(self) -> None:
        self.assertEqual(caesar_shift(""), "")


if __name__ == "__main__":
    unittest.main()
