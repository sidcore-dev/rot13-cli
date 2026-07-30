import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from rot13_cli.cli import main


class TestCli(unittest.TestCase):
    def test_transforms_positional_args(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["Hello, World!"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue(), "Uryyb, Jbeyq!\n")

    def test_reads_from_stdin_by_default(self) -> None:
        out = io.StringIO()
        with patch("sys.stdin", io.StringIO("attack at dawn\n")):
            with redirect_stdout(out):
                code = main([])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue(), "nggnpx ng qnja\n")

    def test_reads_from_file(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "msg.txt"
            path.write_text("secret\n")
            out = io.StringIO()
            with redirect_stdout(out):
                code = main(["--file", str(path)])
            self.assertEqual(code, 0)
            self.assertEqual(out.getvalue(), "frperg\n")

    def test_custom_shift(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["abc", "--shift", "1"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue(), "bcd\n")

    def test_decode_flag_reverses_shift(self) -> None:
        out1 = io.StringIO()
        with redirect_stdout(out1):
            main(["hello", "--shift", "5"])
        shifted = out1.getvalue().strip()

        out2 = io.StringIO()
        with redirect_stdout(out2):
            main([shifted, "--shift", "5", "--decode"])
        self.assertEqual(out2.getvalue().strip(), "hello")

    def test_double_rot13_returns_original(self) -> None:
        out1 = io.StringIO()
        with redirect_stdout(out1):
            main(["classic rot13 test"])
        once = out1.getvalue().strip()

        out2 = io.StringIO()
        with redirect_stdout(out2):
            main([once])
        self.assertEqual(out2.getvalue().strip(), "classic rot13 test")

    def test_missing_file_errors(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            code = main(["--file", "/no/such/file.txt"])
        self.assertEqual(code, 2)
        self.assertIn("error", err.getvalue())

    def test_multiple_positional_words_joined_with_spaces(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["hello", "world"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue(), "uryyb jbeyq\n")


if __name__ == "__main__":
    unittest.main()
