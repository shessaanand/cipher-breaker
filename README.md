# 🔐 Cipher Breaker

A Python tool that **automatically detects and cracks** classical ciphers.
Feed it ciphertext. It figures out the cipher type and breaks it.

## ✅ Progress

| Date | Work Done | Status |
|------|-----------|--------|
| 08/03/2026 | Caesar Cipher — encrypt & decrypt. Shift=3 means A→D, B→E, C→F... | ✅ |
| 09/03/2026 | Substitution Cipher — each letter replaced by another via a key. A→0, B→1, C→2... | ✅ |
| 10/03/2026 | Transposition Cipher — letters rearranged, not changed. Write row by row, read column by column | ✅ |
| 11/03/2026 | Caesar Cracker — automatically finds the shift using frequency analysis | ✅ |
| 11/03/2026 | Tests for Caesar Cipher — 13 unit tests, all passing | ✅ |
| 11/03/2026 | Tests for Substitution Cipher — 15 unit tests, all passing | ✅ |
| 11/03/2026 | Tests for Transposition Cipher — 11 unit tests, all passing | ✅ |
| 11/03/2026 | Index of Coincidence & Cipher Type Detector | ✅ |
| 11/03/2026 | Frequency Analysis for Caesar — chi-squared scoring, 250 combinations tested | ✅ |

---

## 🚀 What's Working Right Now

- **Caesar Cipher** — encrypt and decrypt ✅
- **Substitution Cipher** — encrypt and decrypt ✅
- **Transposition Cipher** — encrypt and decrypt ✅
- **Caesar Cracker** — automatically cracks Caesar using frequency analysis ✅
  - 100% accuracy on texts 40+ characters
  - Tested across 250 combinations (10 sentences × 25 shifts)
- **Index of Coincidence** — detects cipher type from ciphertext alone ✅
- **English Frequency Scorer** — chi-squared + frequency sum scoring ✅

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/cipher-breaker.git
cd cipher-breaker
python --version  # Requires Python 3.7+
```

No external dependencies — pure Python standard library only.

---

## 💻 Usage (Current)

The full CLI (`breaker.py`) is being built in Week 4. For now, use each module directly:

```python
# Encrypt and decrypt
from ciphers.caesar import encrypt, decrypt
ciphertext = encrypt("Hello World", 3)   # → "Khoor Zruog"
plaintext  = decrypt(ciphertext, 3)      # → "Hello World"

# Auto-crack Caesar (no key needed)
from crackers.crack_caesar import crack
result = crack("Khoor Zruog")
print(result['shift'])      # → 3
print(result['plaintext'])  # → "Hello World"

# Detect cipher type from ciphertext alone
from utils.detector import detect_cipher_type
detection = detect_cipher_type("Khoor Zruog")
print(detection['cipher_type'])   # → "caesar"
print(detection['confidence'])    # → "high"

# Verbose mode — see all 26 shift attempts ranked
result = crack("Khoor Zruog", verbose=True)
```

---

## 🔬 How It Works

### Caesar Cipher Breaking — Frequency Analysis
English letters appear at predictable frequencies: E≈13%, T≈9%, A≈8%...
A Caesar cipher just shifts these frequencies — it doesn't destroy them.
So if the most common letter in ciphertext is `X`, it probably maps to `E`.

The cracker tries all 26 possible shifts, scores each decryption using a
chi-squared statistic (how closely letter frequencies match real English),
and returns the shift with the best score.

**Accuracy: 100% on texts with 40+ letters. Tested on 250 combinations.**

---

### Auto-Detection — Index of Coincidence
The Index of Coincidence (IC) measures how "uneven" letter frequencies are in a text.

```
IC formula: Σ(f × (f-1)) / (N × (N-1))
where f = count of each letter, N = total letters
```

| Text type | IC value | Why |
|-----------|----------|-----|
| Normal English | ≈ 0.065 | Some letters appear much more than others |
| Caesar encrypted | ≈ 0.065 | Frequencies shifted but preserved |
| Substitution encrypted | ≈ 0.065 | Letters renamed but distribution unchanged |
| Transposition encrypted | ≈ 0.065 | Letters rearranged, counts unchanged |
| Truly random | ≈ 0.038 | All letters appear roughly equally |

The detector uses IC to confirm monoalphabetic structure, then attempts
a Caesar crack — if the best shift gives very English-like output, it's Caesar.
Otherwise it flags as Substitution or Transposition (handled in Week 3).

---

### Substitution Cipher Breaking — Hill Climbing *(coming next)*
With 26! (~400 septillion) possible keys, brute force is impossible.
Hill climbing starts with a frequency-based guess and iteratively swaps
letters in the key, keeping swaps that improve the quadgram score.

### Transposition Cipher Breaking — Column Search *(coming next)*
Tries every column count from 2–20, scores each reconstruction using
quadgram fitness, returns the column count that produces the most English-like output.

---

## 📁 Project Structure

```
cipher-breaker/
├── breaker.py                  ← Main CLI (coming in Week 4)
├── ciphers/
│   ├── caesar.py               ← Caesar encrypt + decrypt ✅
│   ├── substitution.py         ← Substitution encrypt + decrypt ✅
│   └── transposition.py        ← Transposition encrypt + decrypt ✅
├── crackers/
│   ├── crack_caesar.py         ← Frequency analysis cracker ✅
│   ├── crack_substitution.py   ← Hill climbing cracker (coming)
│   └── crack_transposition.py  ← Column search cracker (coming)
├── utils/
│   ├── frequency.py            ← English letter frequencies + chi-squared scoring ✅
│   ├── scorer.py               ← Quadgram fitness scoring (coming)
│   └── detector.py             ← IC calculator + cipher type detector ✅
├── data/
│   └── quadgrams.txt           ← English quadgram statistics (coming)
├── samples/                    ← Example ciphertext files
└── tests/
    ├── test_caesar.py          ← 13 unit tests ✅
    ├── test_substitution.py    ← 15 unit tests ✅
    ├── test_transposition.py   ← 11 unit tests ✅
    └── stress_test_caesar.py   ← 250-combination accuracy test ✅
```

---

## 🧪 Running Tests

```bash
# Run all unit tests
python tests/test_caesar.py
python tests/test_substitution.py
python tests/test_transposition.py

# Run Caesar cracker stress test (250 combinations)
python tests/stress_test_caesar.py
```

---

## ⚠️ Known Limitations

| Cipher | Min Recommended Length | Accuracy |
|--------|----------------------|----------|
| Caesar | 30+ letters | 100% |
| Caesar (short text) | < 20 letters | Unreliable — use top-3 candidates |

**Why short texts are hard:** Frequency analysis needs enough data to be statistically meaningful.
With only 10 letters, many different shifts can look equally "English-like."
For short Caesar ciphertext, use `crack_top_n()` to get the 3 most likely answers.

---

## 📚 What I Learned Building This

- How frequency analysis exploits statistical patterns in natural language
- Why the chi-squared statistic is better than a simple frequency comparison
- What the Index of Coincidence reveals about a cipher without knowing the key
- Why Caesar has only 26 keys but substitution has 26! — and why that matters
- The difference between confusion (substitution changes letters) and diffusion (transposition moves them)
- How modern ciphers like AES destroy both frequency patterns and positional patterns simultaneously

---

## 📄 License

MIT License — free to use, modify, and distribute.
