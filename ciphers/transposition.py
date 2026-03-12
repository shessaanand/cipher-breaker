import math


def encrypt(plaintext: str, num_columns: int) -> str:
    if num_columns < 2:
        raise ValueError("Number of columns must be at least 2")
    if num_columns > len(plaintext):
        raise ValueError("Number of columns cannot exceed text length")

    num_rows = math.ceil(len(plaintext) / num_columns)

    padded_length = num_rows * num_columns
    padded_text = plaintext.upper() + 'X' * (padded_length - len(plaintext))

    grid = []
    for row in range(num_rows):
        start = row * num_columns
        end = start + num_columns
        grid.append(list(padded_text[start:end]))

    ciphertext = []
    for col in range(num_columns):
        for row in range(num_rows):
            ciphertext.append(grid[row][col])

    return ''.join(ciphertext)


def decrypt(ciphertext: str, num_columns: int) -> str:
    if num_columns < 2:
        raise ValueError("Number of columns must be at least 2")

    text_length = len(ciphertext)
    num_rows = math.ceil(text_length / num_columns)

    num_full_cols = text_length % num_columns
    if num_full_cols == 0:
        num_full_cols = num_columns

    grid = [['' for _ in range(num_columns)] for _ in range(num_rows)]

    index = 0
    for col in range(num_columns):
        col_height = num_rows if col < num_full_cols else num_rows - 1
        for row in range(col_height):
            grid[row][col] = ciphertext[index]
            index += 1

    plaintext = []
    for row in range(num_rows):
        for col in range(num_columns):
            if grid[row][col]: 
                plaintext.append(grid[row][col])
    return ''.join(plaintext)


def decrypt_strip_padding(ciphertext:str,num_columns: int) -> str:
    return decrypt(ciphertext, num_columns).rstrip('X')


if __name__ == "__main__":
    test_cases = [
        ("HELLOWORLD", 4),
        ("ATTACKATDAWN", 3),
        ("THEQUICKBROWNFOX", 5),
        ("PYTHON", 2),
        ("CRYPTOGRAPHY", 6),
    ]

    print("=" * 55)
    print("TRANSPOSITION CIPHER — MANUAL TEST")
    print("="*55)

    all_passed = True
    for plaintext,cols in test_cases:
        encrypted=encrypt(plaintext,cols)
        decrypted=decrypt(encrypted, cols)

        passes=decrypted.startswith(plaintext)
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed=False

        print(f"\nPlaintext: {plaintext}")
        print(f"Columns: {cols}")
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print(f"Stripped: {decrypt_strip_padding(encrypted, cols)}")
        print(f"Status: {status}")

    print("\n"+"="*55)
    print("ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED")
    print("="*55)
