""" 
Date: 11/03/2026. 
Work Done today: 
		1. Making a cracker for Caesar Cipher
"""

import sys
import os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ciphers.caesar import decrypt
from utils.frequency import scoreByChiSquared,scoreByFrequencySum

def crack(ciphertext:str,verbose:bool=False)->dict:
	if not ciphertext.strip():
		raise ValueError("Cannot crack empty ciphertext")
	allResults=[]
	letterCount=0
	for c in ciphertext:
		if c.isalpha():
			letterCount=letterCount+1
	for shift in range(26):
		candidate=decrypt(ciphertext,shift)
		chiSq=scoreByChiSquared(candidate)
		freqSum=scoreByFrequencySum(candidate)
		allResults.append({'shift':shift,'plaintext':candidate,'score':chiSq,'freqSum':freqSum})
	if letterCount<20:
		allResults.sort(key=lambda x:-x['freqSum'])
	else:
		allResults.sort(key=lambda x:x['score'])
	best=allResults[0]
	if verbose:
		_printVerboseResults(ciphertext,allResults)
	return{'shift':best['shift'],'plaintext':best['plaintext'],'score':best['score'],'allResults':allResults}

def crackTopN(ciphertext:str,n:int=3)->list:
	result=crack(ciphertext)
	return result['allResults'][:n]

def _printVerboseResults(ciphertext:str,allResults:list):
	print("\n"+"="*65)
	print("CAESAR CRACKER — ALL 26 SHIFTS")
	if len(ciphertext)>50:
		display=ciphertext[:50]+"..."
	else:
		display=ciphertext
	print(f"Ciphertext: '{display}'")
	print("="*65)
	print(f"{'Rank':<5} {'Shift':<7} {'Score':<12} {'Decrypted (first 40 chars)'}")
	print("-"*65)
	rank=1
	for result in allResults:
		preview=result['plaintext'][:40]
		if rank==1:
			marker=" ← BEST"
		else:
			marker=""
		print(f"{rank:<5} {result['shift']:<7} {result['score']:<12.6f} {preview}{marker}")
		rank=rank+1
	print("="*65)
	print(f"\n✓ Best shift: {allResults[0]['shift']}")
	print(f"✓ Plaintext : {allResults[0]['plaintext'][:60]}")
	print(f"✓ Score     : {allResults[0]['score']:.6f}")

if __name__=="__main__":
	from ciphers.caesar import encrypt
	testCases=[("Hello World",3),("Attack at dawn",7),("The Quick Brown Fox Jumps Over The Lazy Dog",13),("Python programming is fascinating",19),("Never gonna give you up never gonna let you down",5)]
	print("="*65)
	print("CAESAR CRACKER — LIVE DEMO")
	print("="*65)
	allCorrect=True
	for plaintext,shift in testCases:
		ciphertext=encrypt(plaintext,shift)
		result=crack(ciphertext)
		correct=result['shift']==shift
		if correct:
			status="✓ CORRECT"
		else:
			status=f"✗ WRONG (expected {shift}, got {result['shift']})"
			allCorrect=False
		print(f"\nOriginal  : {plaintext}")
		print(f"Shift used: {shift}")
		print(f"Encrypted : {ciphertext}")
		print(f"Cracked   : {result['plaintext']}")
		print(f"Key found : shift = {result['shift']}")
		print(f"Status    : {status}")
	print("\n"+"="*65)
	if allCorrect:
		print("ALL CRACKED CORRECTLY ✓")
	else:
		print("SOME FAILURES ✗")
	print("\n\nVERBOSE MODE DEMO (shows all 26 attempts):")
	sample=encrypt("Secret message here",11)
	crack(sample,verbose=True)

