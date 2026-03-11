''' 
Date: 08/03/2026.
Work Done today: 
     1. Encrypted and decrypted text by shifting each letter by a fixed number. 
     2. shift=3 means, A shifts to D, B to E, C to F, ...
'''

def encrypt(plaintext:str,shift:int)->str:
    shift=shift%26
    result=[]
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result.append(chr(base + shifted))
        else:
            result.append(char)
    return ''.join(result)

def decrypt(ciphertext:str,shift:int)->str:
    return encrypt(ciphertext, 26 - shift)


if __name__ == "__main__":
    test_cases = [
        ("ciphertextwordshift", 3),
        ("Attack is fun", 13),
        ("Hates by dogs", 7),
        ("His cared black cat", 25),
        ("abcdefghijklmnopqrstuvwxyz", 1),
    ]
    print("="*50)
    print("CAESAR CIPHER—MANUAL TEST")
    print("="*50)

    all_passed=True
    for plaintext,shift in test_cases:
        encrypted=encrypt(plaintext, shift)
        decrypted=decrypt(encrypted, shift)
        passed=decrypted == plaintext
        status="PASS" if passed else "FAIL"
        if not passed:
            all_passed=False

        print(f"\nPlaintext: {plaintext}")
        print(f"Shift: {shift}")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print(f"Status: {status}")

    print("\n"+"="*50)
    print("ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED")
    print("="*50)

