import random
import string


def generate_random_key()->str:
    alphabet = list(string.ascii_uppercase)
    random.shuffle(alphabet)
    return ''.join(alphabet)

def validate_key(key: str) -> bool:
    key_upper = key.upper()
    return (
        len(key_upper) == 26 and
        set(key_upper) == set(string.ascii_uppercase)
    )

def encrypt(plaintext:str,key:str)->str:
    if not validate_key(key): raise ValueError(f"Invalid key: must be 26 unique letters. Got: '{key}'")

    key_upper = key.upper()
    result = []

    for char in plaintext:
        if char.isalpha():
            index = ord(char.upper()) - ord('A')
            encrypted_char = key_upper[index]

            if char.islower():
                encrypted_char = encrypted_char.lower()

            result.append(encrypted_char)
        else:
            result.append(char)

    return ''.join(result)
  
def decrypt(ciphertext:str,key:str)->str:
    if not validate_key(key): raise ValueError(f"Invalid key: must be 26 unique letters. Got: '{key}'")

    key_upper = key.upper()

    reverse_key = [''] * 26
    for i, char in enumerate(key_upper):
        position = ord(char) - ord('A')
        reverse_key[position] = chr(ord('A') + i)

    return encrypt(ciphertext, ''.join(reverse_key))


if __name__ == "__main__":
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"

    test_cases = [
        "ciphertextwordshift",
        "Hello World",
        "Attack is fun",
        "His cared black cat ran away from home",
        "abcdefghijklmnopqrstuvwxyz!",
    ]

    print("=" * 50)
    print("SUBSTITUTION CIPHER — MANUAL TEST")
    print(f"Key: {key}")
    print("=" * 50)

    all_passed = True
    for plaintext in test_cases:
        encrypted=encrypt(plaintext,key)
        decrypted=decrypt(encrypted,key)
        passed=decrypted==plaintext
        status= "PASS" if passed else "FAIL"
        if not passed:
            all_passed= False

        print(f"\nPlaintext: {plaintext}")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print(f"Status: {status}")

    print("\n" + "-" * 50)
    print("Testing with a randomly generated key...")
    random_key = generate_random_key()
    print(f"Random key: {random_key}")
    test_text = "Hello from a random key"
    enc= encrypt(test_text,random_key)
    dec= decrypt(enc,random_key)
    print(f"Original: {test_text}")
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {dec}")
    print(f"Status: {'PASS' if dec ==test_text else 'FAIL'}")

    print("\n"+ "="*50)
    print("ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED")
    print("="*50)
