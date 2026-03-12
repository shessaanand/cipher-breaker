'''
Date: 11/03/2026.
Work Done today: 
     1. Index of Coincidence & Cipher Detection
'''

import sys
import os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.frequency import scoreByChiSquared

IC_ENGLISH=0.065
IC_RANDOM=0.038
IC_THRESHOLD=0.043

def calculateIc(text:str)->float:
	letters=[]
	for c in text:
		if c.isalpha():
			letters.append(c.upper())
	n=len(letters)
	if n<2:
		return 0.0
	counts={}
	for letter in letters:
		counts[letter]=counts.get(letter,0)+1
	numerator=0
	for f in counts.values():
		value=f*(f-1)
		numerator=numerator+value
	denominator=n*(n-1)
	return numerator/denominator

def classifyIc(icValue:float)->str:
	if icValue>=0.045:
		return "English-like (monoalphabetic cipher or plaintext)"
	elif icValue>=0.042:
		return "Slightly flattened (could be short text or weak polyalphabetic)"
	elif icValue>=0.040:
		return "Polyalphabetic cipher (e.g., Vigenere)"
	else:
		return "Random-like (uniformly random or strongly polyalphabetic)"

def detectCipherType(ciphertext:str)->dict:
	from crackers.crackCaesar import crack as crackCaesar
	ic=calculateIc(ciphertext)
	icClass=classifyIc(ic)
	if ic<IC_THRESHOLD:
		return{'cipherType':'unknown','ic':ic,'icClassification':icClass,'confidence':'low','reasoning':f"IC={ic:.4f} is too low for Caesar/Substitution/Transposition. This might be a polyalphabetic cipher (like Vigenere) or random data."}
	try:
		caesarResult=crackCaesar(ciphertext)
		bestScore=caesarResult['score']
		CAESAR_CONFIDENCE_THRESHOLD=1.5
		if bestScore<CAESAR_CONFIDENCE_THRESHOLD:
			return{'cipherType':'caesar','ic':ic,'icClassification':icClass,'confidence':'high','caesarShift':caesarResult['shift'],'reasoning':f"IC={ic:.4f} (English-like). Best Caesar shift={caesarResult['shift']} gives chi-squared={bestScore:.4f} (very English-like). High confidence this is Caesar."}
		else:
			return{'cipherType':'substitution_or_transposition','ic':ic,'icClassification':icClass,'confidence':'medium','reasoning':f"IC={ic:.4f} (English-like, so monoalphabetic). But best Caesar score={bestScore:.4f} is too high — letter frequencies don't match a simple shift. Likely Substitution or Transposition cipher."}
	except Exception as e:
		return{'cipherType':'unknown','ic':ic,'icClassification':icClass,'confidence':'low','reasoning':f"Detection failed: {str(e)}"}

if __name__=="__main__":
	from ciphers.caesar import encrypt as caesarEncrypt
	from ciphers.substitution import encrypt as subEncrypt,generateRandomKey
	from ciphers.transposition import encrypt as transEncrypt
	sampleText=("the quick brown fox jumps over the lazy dog "
	"this demonstrates how index of coincidence works in practice")
	caesarCt=caesarEncrypt(sampleText,7)
	subKey=generateRandomKey()
	subCt=subEncrypt(sampleText.upper(),subKey)
	transCt=transEncrypt(sampleText.upper().replace(" ",""),6)
	tests=[("Plain English",sampleText),("Caesar (shift=7)",caesarCt),("Substitution",subCt),("Transposition (cols=6)",transCt)]
	print("="*65)
	print("INDEX OF COINCIDENCE — DEMO")
	print("="*65)
	for label,text in tests:
		ic=calculateIc(text)
		detection=detectCipherType(text)
		print(f"\n{label}:")
		print(f"Text preview: '{text[:45]}...'")
		print(f"IC value: {ic:.4f}")
		print(f"IC class: {classifyIc(ic)}")
		print(f"Detected as: {detection['cipherType']} (confidence: {detection['confidence']})")
		print(f"Reasoning: {detection['reasoning'][:80]}...")
