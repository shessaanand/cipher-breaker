"""
Date: 11/03/2026.
Work Done today: 
     1. Tests for Caesar Cipher
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers.caesar import encrypt, decrypt


def test_basic_encryption():
    """Standard encryption with shift of 3"""
    assert encrypt("HELLO", 3) == "KHOOR"


def test_basic_decryption():
    """Standard decryption with shift of 3"""
    assert decrypt("KHOOR", 3) == "HELLO"


def test_round_trip():
    """Encrypt then decrypt should return original text"""
    original = "The Quick Brown Fox"
    shift = 7
    assert decrypt(encrypt(original, shift), shift) == original


def test_preserves_spaces_and_punctuation():
    """Non-letter characters should not be changed"""
    assert encrypt("Hello, World!", 3) == "Khoor, Zruog!"


def test_preserves_case():
    """Uppercase stays uppercase, lowercase stays lowercase"""
    result = encrypt("Hello World", 3)
    assert result == "Khoor Zruog"
    assert result[0].isupper()  # H → K (uppercase)
    assert result[6].isupper()  # W → Z (uppercase)


def test_shift_zero():
    """Shift of 0 should return the same text"""
    text = "Hello World"
    assert encrypt(text, 0) == text
    assert decrypt(text, 0) == text


def test_shift_26():
    """Shift of 26 should wrap around to same text"""
    text = "Hello World"
    assert encrypt(text, 26) == text


def test_shift_13_rot13():
    """Shift of 13 (ROT13) applied twice should return original"""
    text = "Hello"
    assert encrypt(encrypt(text, 13), 13) == text


def test_large_shift():
    """Shifts larger than 26 should still work correctly"""
    # Shift 29 is same as shift 3
    assert encrypt("HELLO", 29) == encrypt("HELLO", 3)


def test_wrap_around():
    """Letters near end of alphabet should wrap around correctly"""
    # X (23) + 3 = 26 → wraps to A (0)
    assert encrypt("XYZ", 3) == "ABC"
    assert decrypt("ABC", 3) == "XYZ"


def test_full_alphabet():
    """All 26 letters encrypted and decrypted correctly"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    shift = 5
    encrypted = encrypt(alphabet, shift)
    assert decrypt(encrypted, shift) == alphabet


def test_numbers_unchanged():
    """Numbers should not be changed"""
    assert encrypt("abc123", 3) == "def123"


def test_empty_string():
    """Empty string should return empty string"""
    assert encrypt("", 5) == ""
    assert decrypt("", 5) == ""


# --- Run manually if not using pytest ---
if __name__ == "__main__":
    tests = [
        ("test_basic_encryption", test_basic_encryption),
        ("test_basic_decryption", test_basic_decryption),
        ("test_round_trip", test_round_trip),
        ("test_preserves_spaces_and_punctuation", test_preserves_spaces_and_punctuation),
        ("test_preserves_case", test_preserves_case),
        ("test_shift_zero", test_shift_zero),
        ("test_shift_26", test_shift_26),
        ("test_shift_13_rot13", test_shift_13_rot13),
        ("test_large_shift", test_large_shift),
        ("test_wrap_around", test_wrap_around),
        ("test_full_alphabet", test_full_alphabet),
        ("test_numbers_unchanged", test_numbers_unchanged),
        ("test_empty_string", test_empty_string),
    ]

    print("=" * 50)
    print("CAESAR CIPHER TESTS")
    print("=" * 50)

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  ✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {name} — FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {name} — ERROR: {e}")
            failed += 1

    print(f"\n{passed}/{passed+failed} tests passed")
    if failed == 0:
        print("ALL TESTS PASSED ✓")
    else:
        print(f"{failed} TEST(S) FAILED ✗")
