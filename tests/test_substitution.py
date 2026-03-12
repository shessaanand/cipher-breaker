''' 
Date: 11/03/2026.
Work Done today: 
     1. Tests for Substitution Cipher
     
'''

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers.substitution import encrypt, decrypt, generate_random_key, validate_key


def test_basic_encryption():
    """Standard encryption with a known key"""
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    assert encrypt("HELLO", key) == "ITSSG"


def test_basic_decryption():
    """Standard decryption with a known key"""
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    assert decrypt("ITSSG", key) == "HELLO"


def test_round_trip():
    """Encrypt then decrypt should return original text"""
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    original = "Hello World"
    assert decrypt(encrypt(original, key), key) == original


def test_round_trip_random_key():
    """Round trip with a randomly generated key"""
    key = generate_random_key()
    original = "The Quick Brown Fox Jumps Over The Lazy Dog"
    assert decrypt(encrypt(original, key), key) == original


def test_preserves_spaces():
    """Spaces should be preserved unchanged"""
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    result = encrypt("HELLO WORLD", key)
    assert result[5] == " "  # Space stays a space


def test_preserves_punctuation():
    """Punctuation should be preserved unchanged"""
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    result = encrypt("HELLO!", key)
    assert result[-1] == "!"


def test_preserves_case():
    """Uppercase stays uppercase, lowercase stays lowercase"""
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    result = encrypt("Hello", key)
    assert result[0].isupper()
    assert result[1].islower()


def test_validate_key_valid():
    """A proper 26-letter shuffled alphabet should be valid"""
    assert validate_key("QWERTYUIOPASDFGHJKLZXCVBNM") == True
    assert validate_key("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == True


def test_validate_key_invalid_length():
    """Key shorter than 26 chars should be invalid"""
    assert validate_key("ABCDE") == False


def test_validate_key_duplicate_letters():
    """Key with duplicate letters should be invalid"""
    assert validate_key("AACDEFGHIJKLMNOPQRSTUVWXYZ") == False


def test_generate_random_key():
    """Generated key should always be valid"""
    for _ in range(10):
        key = generate_random_key()
        assert validate_key(key), f"Generated key was invalid: {key}"


def test_identity_key():
    """Key ABCDE... (identity) should return same text"""
    identity_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = "HELLO"
    assert encrypt(text, identity_key) == text
    assert decrypt(text, identity_key) == text


def test_full_alphabet_round_trip():
    """Full alphabet should survive a round trip"""
    key = "ZYXWVUTSRQPONMLKJIHGFEDCBA"  # Reversed alphabet
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert decrypt(encrypt(alphabet, key), key) == alphabet


def test_numbers_unchanged():
    """Numbers should not be modified"""
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    assert encrypt("ABC123", key) == "QWE123"


def test_invalid_key_raises():
    """Invalid key should raise ValueError"""
    try:
        encrypt("HELLO", "NOTAVALIDKEY")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected


# --- Run manually if not using pytest ---
if __name__ == "__main__":
    tests = [
        ("test_basic_encryption", test_basic_encryption),
        ("test_basic_decryption", test_basic_decryption),
        ("test_round_trip", test_round_trip),
        ("test_round_trip_random_key", test_round_trip_random_key),
        ("test_preserves_spaces", test_preserves_spaces),
        ("test_preserves_punctuation", test_preserves_punctuation),
        ("test_preserves_case", test_preserves_case),
        ("test_validate_key_valid", test_validate_key_valid),
        ("test_validate_key_invalid_length", test_validate_key_invalid_length),
        ("test_validate_key_duplicate_letters", test_validate_key_duplicate_letters),
        ("test_generate_random_key", test_generate_random_key),
        ("test_identity_key", test_identity_key),
        ("test_full_alphabet_round_trip", test_full_alphabet_round_trip),
        ("test_numbers_unchanged", test_numbers_unchanged),
        ("test_invalid_key_raises", test_invalid_key_raises),
    ]

    print("=" * 55)
    print("SUBSTITUTION CIPHER TESTS")
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
