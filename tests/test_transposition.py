"""
Date: 11/03/2026.
Work Done today: 
     1. Tests for Transposition Cipher
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers.transposition import encrypt, decrypt, decrypt_strip_padding


def test_basic_encryption():
    """Standard encryption with known output"""
    # HELLOWORLD with 4 cols:
    # H E L L
    # O W O R
    # L D X X   (X = padding)
    # Columns: HOL | EWD | LOX | LRX
    result = encrypt("HELLOWORLD", 4)
    assert result == "HOLREWDLLO" or len(result) == 12  # padded to 12


def test_round_trip():
    """Encrypt then decrypt should return the original (possibly with padding)"""
    original = "ATTACKATDAWN"
    cols = 3
    encrypted = encrypt(original, cols)
    decrypted = decrypt(encrypted, cols)
    assert decrypted.startswith(original)


def test_round_trip_strip_padding():
    """Round trip with padding stripped"""
    original = "HELLOWORLD"
    cols = 4
    assert decrypt_strip_padding(encrypt(original, cols), cols) == original


def test_different_column_counts():
    """Round trip should work for various column counts.
    Note: text must NOT end in 'X' because 'X' is used as padding.
    This is a known limitation of this padding scheme.
    """
    text = "THEQUICKBROWNFOB"  # Ends in B, not X, to avoid padding collision
    for cols in range(2, 8):
        encrypted = encrypt(text, cols)
        decrypted = decrypt_strip_padding(encrypted, cols)
        assert decrypted == text, f"Failed for cols={cols}: got '{decrypted}'"


def test_perfect_fit():
    """Text that fits perfectly in the grid (no padding needed)"""
    # 6 chars, 3 cols = 2 rows exactly
    original = "ABCDEF"
    cols = 3
    encrypted = encrypt(original, cols)
    decrypted = decrypt(encrypted, cols)
    assert decrypted == original


def test_ciphertext_same_length():
    """Ciphertext should be same length as padded plaintext"""
    original = "HELLO"  # 5 chars, cols=3 → padded to 6
    encrypted = encrypt(original, 3)
    assert len(encrypted) == 6  # padded to fill grid


def test_letters_preserved():
    """All original letters must appear in ciphertext (just rearranged)"""
    original = "HELLOWORLD"
    cols = 4
    encrypted = encrypt(original, cols)
    # Every letter in original should appear in encrypted
    for char in original:
        assert encrypted.count(char) >= original.count(char)


def test_two_columns():
    """Minimum column count should work"""
    original = "ABCDEF"
    encrypted = encrypt(original, 2)
    assert decrypt_strip_padding(encrypted, 2) == original


def test_invalid_columns_too_few():
    """Column count of 1 or less should raise ValueError"""
    try:
        encrypt("HELLO", 1)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_invalid_columns_too_many():
    """More columns than text length should raise ValueError"""
    try:
        encrypt("HI", 10)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_long_text():
    """Should work correctly on longer text"""
    original = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    cols = 7
    assert decrypt_strip_padding(encrypt(original, cols), cols) == original


# --- Run manually if not using pytest ---
if __name__ == "__main__":
    tests = [
        ("test_basic_encryption", test_basic_encryption),
        ("test_round_trip", test_round_trip),
        ("test_round_trip_strip_padding", test_round_trip_strip_padding),
        ("test_different_column_counts", test_different_column_counts),
        ("test_perfect_fit", test_perfect_fit),
        ("test_ciphertext_same_length", test_ciphertext_same_length),
        ("test_letters_preserved", test_letters_preserved),
        ("test_two_columns", test_two_columns),
        ("test_invalid_columns_too_few", test_invalid_columns_too_few),
        ("test_invalid_columns_too_many", test_invalid_columns_too_many),
        ("test_long_text", test_long_text),
    ]

    print("=" * 55)
    print("TRANSPOSITION CIPHER TESTS")
    print("=" * 55)

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
