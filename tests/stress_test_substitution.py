'''
Date: 14/03/2026.
Work Done today: 
     1. Documents accuracy at different text lengths and explains why longer text = higher accuracy for hill climbing.
'''

import sys
import os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers.substitution import encrypt,generateRandomKey
from crackers.crackSubstitution import crack

shortTexts=[
	"THEQUICKBROWNFOX",
	"PYTHONPROGRAMMING",
	"HELLOWORLD",
]

mediumTexts=[
	"THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",
	"TOBEORNOTTOBETHATISTHEQUESTION",
	"PYTHONISAHIGHLEVELPROGRAMMINGLANGUAGE",
	"CRYPTOGRAPHYISTHESTUDYOFSECURECOMMUNICATION",
	"NEVERGOINGTOGIVEYOUUPNEVERGOINGTOLETDOWN",
]

longTexts=[
	"THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"*3,
	"TOBEORNOTTOBETHATISTHEQUESTION"*4,
	"PYTHONPROGRAMMINGTEACHESLOGICALTHINKINGANDPROBLEMSOLVING"*2,
	"ALLTHEWORLDSASTAGEANDALLTHECANCELLAMANDAREWOMENSIMPLYGIFTED"*2,
]

def wordAccuracy(original:str,recovered:str)->float:
	if not original:
		return 0.0
	matches=sum(a==b for a,b in zip(original,recovered))
	return matches/len(original)*100

def runStressTest():
	print("="*65)
	print("SUBSTITUTION CRACKER — STRESS TEST")
	print("="*65)
	print("\n  Note: hill climbing accuracy depends on quadgrams.txt quality.")
	print("  Download the real file from practicalcryptography.com")
	print("  for best results.\n")
	print("📊 TEST 1: Medium texts (30–43 chars) × 5 random keys each")
	print("-"*65)
	total1=0
	above80=0
	above50=0
	for text in mediumTexts:
		textAccs=[]
		for trial in range(5):
			key=generateRandomKey()
			ciphertext=encrypt(text,key)
			result=crack(ciphertext,restarts=3,verbose=False)
			acc=wordAccuracy(text,result['plaintext'])
			textAccs.append(acc)
			total1+=1
			if acc>=80:
				above80+=1
			if acc>=50:
				above50+=1
		avg=sum(textAccs)/len(textAccs)
		print(f"  '{text[:35]}...' → avg {avg:.0f}% char accuracy")
	print(f"\n  Total tested : {total1}")
	print(f"  Above 80%   : {above80}/{total1} ({above80/total1*100:.0f}%)")
	print(f"  Above 50%   : {above50}/{total1} ({above50/total1*100:.0f}%)")
	print(f"\n📊 TEST 2: Long texts (100+ chars) × 3 random keys each")
	print("-"*65)
	total2=0
	above802=0
	for text in longTexts:
		textAccs=[]
		for trial in range(3):
			key=generateRandomKey()
			ciphertext=encrypt(text,key)
			result=crack(ciphertext,restarts=5,verbose=False)
			acc=wordAccuracy(text,result['plaintext'])
			textAccs.append(acc)
			total2+=1
			if acc>=80:
				above802+=1
		avg=sum(textAccs)/len(textAccs)
		bar="█"*int(avg/5)
		print(f"  len={len(text):<4} → avg {avg:5.1f}% {bar}")
	print(f"\n  Total tested : {total2}")
	print(f"  Above 80%   : {above802}/{total2} ({above802/total2*100:.0f}%)")
	print(f"\n📊 TEST 3: Short texts (<20 chars) — honest documentation")
	print("-"*65)
	print("  Short texts don't have enough letter variety for hill")
	print("  climbing to find the right key reliably.\n")
	for text in shortTexts:
		key=generateRandomKey()
		ct=encrypt(text,key)
		result=crack(ct,restarts=3,verbose=False)
		acc=wordAccuracy(text,result['plaintext'])
		print(f"  '{text}' (len={len(text)}) → {acc:.0f}% accuracy")
	print(f"\n{'='*65}")
	print("SUMMARY")
	print(f"{'='*65}")
	print(f"  Why longer texts work better:")
	print(f"    - More letters = more quadgrams to score")
	print(f"    - More quadgrams = clearer signal for hill climbing")
	print(f"    - Short texts have too few unique quadgrams to guide the search")
	print(f"\n  📌 Rule of thumb:")
	print(f"     < 30 chars  → Unreliable")
	print(f"     30–80 chars → Moderate (~50–80% char accuracy)")
	print(f"     80+ chars   → Good (~80–95% char accuracy)")
	print(f"     200+ chars  → Excellent (with real quadgrams.txt)")

if __name__=="__main__":
	runStressTest()
