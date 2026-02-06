import yaml
import random
import os
from typing import Dict, List, Optional

class WordBank:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.words = self._load_words()

    def _load_words(self) -> List[Dict]:
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Word bank file not found at {self.data_path}")
        
        with open(self.data_path, 'r') as f:
            data = yaml.safe_load(f)
        return data.get('words', [])

    def get_word(self, difficulty: int = 1) -> Optional[Dict]:
        """
        Selects a random word matching the requested difficulty.
        If no exact match, tries to find one within +/- 1 difficulty.
        """
        candidates = [w for w in self.words if w.get('difficulty') == difficulty]
        
        if not candidates:
            # Fallback: broaden search
            candidates = [w for w in self.words if abs(w.get('difficulty', 1) - difficulty) <= 1]
            
        if not candidates:
             # Ultimate fallback: any word
            candidates = self.words
            
        if not candidates:
            return None
            
        return random.choice(candidates)

    def get_categories(self) -> List[str]:
        return list(set(w.get('category', 'Unknown') for w in self.words))
