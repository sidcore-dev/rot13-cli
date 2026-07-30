"""Core ROT13 / Caesar cipher logic — pure functions, no I/O."""
from __future__ import annotations

import string

_ALPHABET_SIZE = 26


def caesar_shift(text: str, shift: int = 13) -> str:
    """Shift each letter in `text` by `shift` positions in the alphabet.

    Wraps around at the alphabet boundary and leaves case and all
    non-letter characters (digits, punctuation, whitespace) untouched.

    This is a pure letter-substitution transform with no cryptographic
    security whatsoever — it's the classic `rot13`/Caesar cipher, useful
    only for lightly obscuring text (spoiler warnings, joke answers),
    never for protecting anything actually sensitive.

    `shift` may be any integer, positive or negative; it's normalized
    modulo 26. Calling again with the sign of `shift` flipped reverses
    the transform — with the default shift of 13, ROT13 is its own
    inverse, so applying it twice returns the original text.
    """
    normalized_shift = shift % _ALPHABET_SIZE
    result_chars = []
    for char in text:
        if char in string.ascii_lowercase:
            index = (ord(char) - ord("a") + normalized_shift) % _ALPHABET_SIZE
            result_chars.append(chr(ord("a") + index))
        elif char in string.ascii_uppercase:
            index = (ord(char) - ord("A") + normalized_shift) % _ALPHABET_SIZE
            result_chars.append(chr(ord("A") + index))
        else:
            result_chars.append(char)
    return "".join(result_chars)
