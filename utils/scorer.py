'''
Date: 14/03/2026.
Work Done today: 
     1. Quadgram Fitness Scorer
'''

import os
import math
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class QuadgramScorer:
    def __init__(self, quadgram_file: str = None):
        self.quadgrams={}
        self.total=0
        self.floor=0.0
        if quadgram_file is None:
            base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            quadgram_file=os.path.join(base_dir,'data','quadgrams.txt')
        if os.path.exists(quadgram_file):
            self._load_from_file(quadgram_file)
        else:
            raise FileNotFoundError(f"quadgrams.txt not found at {quadgram_file}. Run: python data/generate_quadgrams.py")

    def _load_from_file(self, filepath: str):
        with open(filepath,'r') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts=line.split()
                if len(parts)==2:
                    quadgram,count=parts[0].upper(),int(parts[1])
                    self.quadgrams[quadgram]=count
                    self.total+=count
        for q in self.quadgrams:
            self.quadgrams[q]=math.log10(self.quadgrams[q]/self.total)
        self.floor=math.log10(0.01/self.total)

    def score(self, text: str) -> float:
        letters=''.join(c.upper() for c in text if c.isalpha())
        if len(letters)<4:
            return float('-inf')
        score=0.0
        for i in range(len(letters)-3):
            quad=letters[i:i+4]
            score+=self.quadgrams.get(quad,self.floor)
        return score

_scorer_instance=None

def get_scorer() -> QuadgramScorer:
    global _scorer_instance
    if _scorer_instance is None:
        _scorer_instance=QuadgramScorer()
    return _scorer_instance

def score_text(text: str) -> float:
    return get_scorer().score(text)

if __name__=="__main__":
    from ciphers.caesar import encrypt as caesar_encrypt
    from ciphers.substitution import encrypt as sub_encrypt,generate_random_key
    scorer=QuadgramScorer()
    english="the quick brown fox jumps over the lazy dog and the cat sat on the mat"
    encrypted_caesar=caesar_encrypt(english,13)
    encrypted_sub=sub_encrypt(english.upper(),generate_random_key())
    print("="*55)
    print("QUADGRAM SCORER — DEMO")
    print("="*55)
    print(f"\nEnglish text   : score = {scorer.score(english):.2f}")
    print(f"Caesar (rot13) : score = {scorer.score(encrypted_caesar):.2f}")
    print(f"Substitution   : score = {scorer.score(encrypted_sub):.2f}")
    print("\nExpected: English scores highest, encrypted scores lowest")
