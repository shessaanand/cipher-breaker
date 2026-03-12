"""
Date: 11/03/2026.
Work Done today: 
     1. Frequency Analysis of Caesar Ciphers
"""


ENGLISH_FREQ={'A':0.08167,'B':0.01492,'C':0.02782,'D':0.04253,'E':0.12702,'F':0.02228,'G':0.02015,'H':0.06094,'I':0.06966,'J':0.00153,'K':0.00772,'L':0.04025,'M':0.02406,'N':0.06749,'O':0.07507,'P':0.01929,'Q':0.00095,'R':0.05987,'S':0.06327,'T':0.09056,'U':0.02758,'V':0.00978,'W':0.02360,'X':0.00150,'Y':0.01974,'Z':0.00074}
LETTERS_BY_FREQUENCY=sorted(ENGLISH_FREQ,key=ENGLISH_FREQ.get,reverse=True)

def getTextFrequency(text:str)->dict:
	lettersOnly=[]
	for c in text:
		if c.isalpha():
			upperC=c.upper()
			lettersOnly.append(upperC)
	total=len(lettersOnly)
	if total==0:
		emptyResult={}
		for i in range(ord('A'),ord('Z')+1):
			letter=chr(i)
			emptyResult[letter]=0.0
		return emptyResult
	counts={}
	for i in range(ord('A'),ord('Z')+1):
		letter=chr(i)
		counts[letter]=0
	for letter in lettersOnly:
		currentCount=counts[letter]
		newCount=currentCount+1
		counts[letter]=newCount
	result={}
	for letter,count in counts.items():
		value=count/total
		result[letter]=value
	return result

def scoreByChiSquared(text:str)->float:
	observed=getTextFrequency(text)
	chiSquared=0.0
	for letter in ENGLISH_FREQ:
		observedFreq=observed.get(letter,0.0)
		expectedFreq=ENGLISH_FREQ[letter]
		if expectedFreq>0:
			difference=observedFreq-expectedFreq
			squared=difference**2
			value=squared/expectedFreq
			chiSquared=chiSquared+value
	return chiSquared

def scoreByFrequencySum(text:str)->float:
	observed=getTextFrequency(text)
	score=0.0
	for letter in ENGLISH_FREQ:
		observedValue=observed.get(letter,0.0)
		expectedValue=ENGLISH_FREQ[letter]
		product=observedValue*expectedValue
		score=score+product
	return score

def getMostCommonLetters(text:str,n:int=6)->list:
	freq=getTextFrequency(text)
	items=[]
	for item in freq.items():
		items.append(item)
	sortedLetters=sorted(items,key=lambda x:x[1],reverse=True)
	result=[]
	index=0
	for item in sortedLetters:
		if index>=n:
			break
		result.append(item)
		index=index+1
	return result

if __name__=="__main__":
	import sys
	import os
	currentPath=os.path.abspath(__file__)
	parent=os.path.dirname(currentPath)
	grandparent=os.path.dirname(parent)
	sys.path.insert(0,grandparent)
	from ciphers.caesar import encrypt
	englishText=("the quick brown fox jumps over the lazy dog "
	"this is a sample of normal english text with common words "
	"and typical letter frequency distribution")
	caesarEncrypted=encrypt(englishText,13)
	gibberish="xkqzwjvbmptyrfsdlnhcgoueia"*5
	print("="*60)
	print("FREQUENCY ANALYSIS DEMO")
	print("="*60)
	print(f"\nEnglish text (first 50 chars): '{englishText[:50]}...'")
	chi1=scoreByChiSquared(englishText)
	print(f"  Chi-squared score : {chi1:.6f} (lower = more English)")
	freq1=scoreByFrequencySum(englishText)
	print(f"  Frequency sum     : {freq1:.6f} (higher = more English)")
	top1=getMostCommonLetters(englishText,6)
	print(f"  Top 6 letters     : {top1}")
	print(f"\nCaesar (shift=13): '{caesarEncrypted[:50]}...'")
	chi2=scoreByChiSquared(caesarEncrypted)
	print(f"  Chi-squared score : {chi2:.6f}")
	freq2=scoreByFrequencySum(caesarEncrypted)
	print(f"  Frequency sum     : {freq2:.6f}")
	top2=getMostCommonLetters(caesarEncrypted,6)
	print(f"  Top 6 letters     : {top2}")
	print(f"\nGibberish: '{gibberish[:50]}...'")
	chi3=scoreByChiSquared(gibberish)
	print(f"  Chi-squared score : {chi3:.6f}")
	freq3=scoreByFrequencySum(gibberish)
	print(f"  Frequency sum     : {freq3:.6f}")
	top3=getMostCommonLetters(gibberish,6)
	print(f"  Top 6 letters     : {top3}")
	print("\n"+"="*60)
	print("EXPECTED: English scores LOWEST chi-squared, HIGHEST freq sum")
	print("="*60)

