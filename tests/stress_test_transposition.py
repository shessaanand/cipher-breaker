'''
Date: 14/03/2026.
Work Done today: 
     1. Transposition Cracker Stress Test: tested the cracker across many texts and column counts.
'''
import sys
import os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers.transposition import encrypt,decryptStripPadding
from crackers.crackTransposition import crack

shortTexts=[
	"HELLOWORLD",
	"ATTACKATDAWN",
	"SECRETCODE",
	"PYTHONROCKS",
]

mediumTexts=[
	"THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",
	"PYTHONPROGRAMMINGTEACHESLOGICALTHINKING",
	"CRYPTOGRAPHYISTHESTUDYOFSECURECOMMUNICATION",
	"NEVERGOINGTOGIVEYOUUPNEVERGOINGTOLETDOWN",
	"COMPUTERORGANIZATIONTEACHESHOWCPUSWORK",
]

longTexts=[
	"THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"*2,
	"TOBEORNOTTOBETHATISTHEQUESTIONWHETHERITIS"*2,
	"PYTHONISAHIGHLEVELPROGRAMMINGLANGUAGEKNOWNFORITSREADABILITY",
	"ALLTHEWORLDSASTAGEANDALLTHECANCELLAMANDAREWOMEN"*2,
	"CRYPTOGRAPHYPROTECTSDATASECURITYANDENSURESPRIVACY"*2,
]

def runStressTest():
	print("="*65)
	print("TRANSPOSITION CRACKER — STRESS TEST")
	print("="*65)
	print("\n📊 TEST 1: Medium texts (35–43 chars) × cols 2–8")
	print("-"*65)
	correct=0
	total=0
	failures=[]
	for text in mediumTexts:
		for cols in range(2,9):
			if cols>=len(text)//2:
				continue
			ct=encrypt(text,cols)
			result=crack(ct)
			total+=1
			recovered=result['plaintext']
			match=(recovered==text or recovered==text.rstrip('X'))
			if match:
				correct+=1
			else:
				failures.append({
					'text':text[:30],
					'cols':cols,
					'gotCols':result['numColumns'],
					'recovered':recovered[:30]
				})
	accuracy=correct/total*100 if total>0 else 0
	print(f"  Tested : {total} combinations ({len(mediumTexts)} texts × up to 7 col counts)")
	print(f"  Correct: {correct}/{total} ({accuracy:.1f}%)")
	if failures:
		print(f"\n  ⚠ Failures ({len(failures)}):")
		for f in failures[:5]:
			print(f"    cols={f['cols']} on '{f['text']}'")
			print(f"    → Got cols={f['gotCols']}: '{f['recovered']}'")
	print(f"\n📊 TEST 2: Long texts (59–98 chars) × cols 2–10")
	print("-"*65)
	correct2=0
	total2=0
	failures2=[]
	for text in longTexts:
		for cols in range(2,11):
			if cols>=len(text)//2:
				continue
			ct=encrypt(text,cols)
			result=crack(ct)
			total2+=1
			recovered=result['plaintext']
			match=(recovered==text or recovered==text.rstrip('X'))
			if match:
				correct2+=1
			else:
				failures2.append({
					'text':text[:30],
					'cols':cols,
					'gotCols':result['numColumns'],
				})
	accuracy2=correct2/total2*100 if total2>0 else 0
	print(f"  Tested : {total2} combinations ({len(longTexts)} texts × up to 9 col counts)")
	print(f"  Correct: {correct2}/{total2} ({accuracy2:.1f}%)")
	if failures2:
		print(f"\n  ⚠ Failures ({len(failures2)}):")
		for f in failures2[:5]:
			print(f"    cols={f['cols']} on '{f['text']}' → got cols={f['gotCols']}")
	print(f"\n📊 TEST 3: Short texts (10–12 chars) — honest edge cases")
	print("-"*65)
	print("  Note: Very short texts are ambiguous — many column counts")
	print("  can produce plausible-looking output.\n")
	for text in shortTexts:
		ct=encrypt(text,3)
		result=crack(ct)
		top3Cols=[r['numColumns'] for r in result['allResults'][:3]]
		match=(result['plaintext']==text or result['plaintext']==text.rstrip('X'))
		status="✓ Correct" if match else f"✗ Got cols={result['numColumns']}"
		print(f"  '{text}' (len={len(text)}, cols=3)")
		print(f"  → {status} | Top 3 guesses: cols={top3Cols}")
	print(f"\n{'='*65}")
	print("SUMMARY")
	print(f"{'='*65}")
	print(f"  Medium texts (35–43 chars) : {accuracy:.1f}% accuracy")
	print(f"  Long texts   (59–98 chars) : {accuracy2:.1f}% accuracy")
	print(f"  Short texts  (<15 chars)   : Unreliable — ambiguous by nature")
	print(f"\n  📌 Rule of thumb: Use texts with 40+ characters for")
	print(f"     reliable transposition cracking results.")

if __name__=="__main__":
	runStressTest()
