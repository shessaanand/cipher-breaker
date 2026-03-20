'''
Date: 08/03/2026.
Work Done today: 
        1. Substitution Cipher Cracker: Hill Climbing Algorithm
'''
import random
import sys
import os

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers.substitution import encrypt,decrypt,generateRandomKey
from utils.scorer import QuadgramScorer
from utils.frequency import getMostCommonLetters,lettersByFrequency

def getFrequencyBasedKey(ciphertext:str)->str:
	cipherFreq=getMostCommonLetters(ciphertext,26)
	cipherLettersByFreq=[pair[0] for pair in cipherFreq]
	key=['A']*26
	for i,cipherLetter in enumerate(cipherLettersByFreq):
		if i<len(lettersByFrequency):
			englishLetter=lettersByFrequency[i]
			pos=ord(englishLetter)-ord('A')
			key[pos]=cipherLetter
	used=set(key)
	unusedCipher=[c for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if c not in used]
	for i in range(26):
		if key[i]=='A' and i>0:
			if unusedCipher:
				key[i]=unusedCipher.pop(0)
	return ''.join(key)

def hillClimb(ciphertext:str,scorer:QuadgramScorer,iterations:int=2000)->tuple:
	currentKey=getFrequencyBasedKey(ciphertext)
	currentPlain=decrypt(ciphertext,currentKey)
	currentScore=scorer.score(currentPlain)
	bestKey=currentKey
	bestScore=currentScore
	bestPlain=currentPlain
	improved=True
	iters=0
	while improved and iters<iterations:
		improved=False
		keyList=list(currentKey)
		for i in range(26):
			for j in range(i+1,26):
				keyList[i],keyList[j]=keyList[j],keyList[i]
				newKey=''.join(keyList)
				newPlain=decrypt(ciphertext,newKey)
				newScore=scorer.score(newPlain)
				if newScore>currentScore:
					currentKey=newKey
					currentScore=newScore
					currentPlain=newPlain
					keyList=list(currentKey)
					improved=True
					if newScore>bestScore:
						bestKey=newKey
						bestScore=newScore
						bestPlain=newPlain
				else:
					keyList[i],keyList[j]=keyList[j],keyList[i]
				iters+=1
				if iters>=iterations:
					break
			if iters>=iterations:
				break
	return bestKey,bestScore,bestPlain

def crack(ciphertext:str,restarts:int=5,iterationsPerRestart:int=5000,verbose:bool=False)->dict:
	if not ciphertext.strip():
		raise ValueError("Cannot crack empty ciphertext")
	scorer=QuadgramScorer()
	bestKey=None
	bestScore=float('-inf')
	bestPlain=''
	if verbose:
		print(f"\n[*] Starting substitution cracker")
		print(f"[*] Ciphertext length : {len(ciphertext)} chars")
		print(f"[*] Restarts          : {restarts}")
		print(f"[*] Iterations each   : {iterationsPerRestart}")
		print(f"[*] Running...\n")
	for restart in range(restarts):
		key,score,plain=hillClimb(ciphertext,scorer,iterations=iterationsPerRestart)
		if score>bestScore:
			bestScore=score
			bestKey=key
			bestPlain=plain
		if verbose:
			print(f"  Restart {restart+1}/{restarts} → score={score:.2f} | sample='{plain[:50]}'")
	if verbose:
		print(f"\n[✓] Best score : {bestScore:.2f}")
		print(f"[✓] Key found  : {bestKey}")
		print(f"[✓] Plaintext  : {bestPlain[:80]}")
	return {
		'key':bestKey,
		'plaintext':bestPlain,
		'score':bestScore,
	}

if __name__=="__main__":
	from ciphers.substitution import encrypt,generateRandomKey
	testCases=[
		"the quick brown fox jumps over the lazy dog and the cat sat on the mat near the river",
		"in the beginning was the word and the word was with god and the word was god",
		"to be or not to be that is the question whether tis nobler in the mind to suffer",
		"four score and seven years ago our fathers brought forth on this continent a new nation",
		"python is a high level general purpose programming language known for its readability",
	]
	print("="*65)
	print("SUBSTITUTION CRACKER — LIVE DEMO")
	print("="*65)
	correct=0
	for i,plaintext in enumerate(testCases):
		key=generateRandomKey()
		ciphertext=encrypt(plaintext.upper(),key)
		result=crack(ciphertext,restarts=5,verbose=False)
		originalWords=plaintext.upper().split()
		crackedWords=result['plaintext'].upper().split()
		matches=sum(1 for a,b in zip(originalWords,crackedWords) if a==b)
		accuracy=matches/len(originalWords)*100
		status="✓" if accuracy>=80 else "✗"
		if accuracy>=80:
			correct+=1
		print(f"\nTest {i+1}: '{plaintext[:50]}...'")
		print(f"  Key used  : {key}")
		print(f"  Cracked   : '{result['plaintext'][:50]}'")
		print(f"  Accuracy  : {accuracy:.0f}% word match  {status}")
	print(f"\n{'='*65}")
	print(f"Results: {correct}/{len(testCases)} cracked with 80%+ word accuracy")
