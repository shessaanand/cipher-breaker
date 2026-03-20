import sys
import os

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ciphers.transposition import decrypt,decryptStripPadding
from utils.scorer import QuadgramScorer

def crack(ciphertext:str,minCols:int=2,maxCols:int=20,verbose:bool=False)->dict:
	if not ciphertext.strip():
		raise ValueError("Cannot crack empty ciphertext")
	cleaned=''.join(c.upper() for c in ciphertext if c.isalpha())
	if len(cleaned)<4:
		raise ValueError("Ciphertext too short to crack (need at least 4 letters)")
	scorer=QuadgramScorer()
	allResults=[]
	maxCols=min(maxCols,len(cleaned)//2)
	for cols in range(minCols,maxCols+1):
		try:
			candidate=decryptStripPadding(cleaned,cols)
			score=scorer.score(candidate)
			allResults.append({
				'numColumns':cols,
				'plaintext':candidate,
				'score':score,
			})
		except (ValueError,ZeroDivisionError):
			continue
	if not allResults:
		raise ValueError("No valid column counts found for this ciphertext length")
	allResults.sort(key=lambda x:x['score'],reverse=True)
	best=allResults[0]
	if verbose:
		_printVerboseResults(cleaned,allResults)
	return {
		'numColumns':best['numColumns'],
		'plaintext':best['plaintext'],
		'score':best['score'],
		'allResults':allResults,
	}

def _printVerboseResults(ciphertext:str,allResults:list):
	byCols=sorted(allResults,key=lambda x:x['numColumns'])
	print("\n"+"="*65)
	print("TRANSPOSITION CRACKER — ALL COLUMN COUNTS TRIED")
	print(f"Ciphertext: '{ciphertext[:50]}{'...' if len(ciphertext)>50 else ''}'")
	print("="*65)
	print(f"{'Cols':<6} {'Score':<12} {'Decrypted (first 45 chars)'}")
	print("-"*65)
	bestScore=max(r['score'] for r in allResults)
	for result in byCols:
		marker=" ← BEST" if result['score']==bestScore else ""
		preview=result['plaintext'][:45]
		print(f"{result['numColumns']:<6} {result['score']:<12.2f} {preview}{marker}")
	best=max(allResults,key=lambda x:x['score'])
	print("="*65)
	print(f"\nBest column count : {best['numColumns']}")
	print(f"Plaintext         : {best['plaintext'][:60]}")
	print(f"Score             : {best['score']:.2f}")

if __name__=="__main__":
	from ciphers.transposition import encrypt
	testCases=[
		("HELLOWORLD",4),
		("ATTACKATDAWN",3),
		("THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG",7),
		("PYTHONPROGRAMMINGISFUN",5),
		("THECATSATONTHEMAT",4),
		("SECRETMESSAGEHERE",6),
		("ABCDEFGHIJKLMNOPQRSTUVWXYZ",3),
		("CRYPTOGRAPHYISTHESTUDYOFSECURECOMMUNICATION",8),
		("NEVERGOINGTOGIVEYOUUPNEVERGOINGTOLETDOWNYOU",6),
		("COMPUTERORGANIZATIONTEACHESHOWCPUSWORK",9),
	]
	print("="*65)
	print("TRANSPOSITION CRACKER — LIVE DEMO")
	print("="*65)
	correct=0
	for plaintext,cols in testCases:
		ciphertext=encrypt(plaintext,cols)
		result=crack(ciphertext,verbose=False)
		foundCols=result['numColumns']
		recovered=result['plaintext']
		match=recovered==plaintext or recovered==plaintext.rstrip('X')
		status="CORRECT" if match else f"WRONG (expected {cols}, got {foundCols})"
		if match:
			correct+=1
		print(f"\nPlaintext  : {plaintext}")
		print(f"Cols used  : {cols}")
		print(f"Ciphertext : {ciphertext}")
		print(f"Cracked    : {recovered}")
		print(f"Cols found : {foundCols}")
		print(f"Status     : {status}")
	print(f"\n{'='*65}")
	print(f"Results: {correct}/{len(testCases)} cracked correctly")
	print("\n\nVERBOSE MODE DEMO:")
	sampleCt=encrypt("SECRETMESSAGEISHERE",5)
	crack(sampleCt,verbose=True)
