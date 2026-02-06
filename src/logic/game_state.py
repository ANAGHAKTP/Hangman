from typing import List, Dict, Set
from dataclasses import dataclass, field

@dataclass
class GameStatus:
    target_word: Dict
    masked_word: List[str]
    guessed_letters: Set[str] = field(default_factory=set)
    breach_level: int = 0
    max_breach_level: int = 5
    hints_used: int = 0
    game_over: bool = False
    won: bool = False
    message: str = ""

    def to_dict(self):
        return {
            "masked_word": " ".join(self.masked_word),
            "guessed_letters": list(self.guessed_letters),
            "breach_level": self.breach_level,
            "max_breach_level": self.max_breach_level,
            "hints_used": self.hints_used,
            "game_over": self.game_over,
            "won": self.won,
            "message": self.message
        }

class GameState:
    BREACH_STAGES = [
        "Secure",
        "Firewall Weakened",
        "Encryption Broken",
        "Credentials Exposed",
        "Unauthorized Access",
        "SYSTEM COMPROMISED"
    ]

    def __init__(self, word_data: Dict):
        self.word_data = word_data
        self.word = word_data['word'].upper()
        self.status = GameStatus(
            target_word=word_data,
            masked_word=['_' if c.isalpha() else c for c in self.word]
        )

    def guess_letter(self, letter: str) -> bool:
        letter = letter.upper()
        if letter in self.status.guessed_letters:
            self.status.message = f"Letter '{letter}' already attempted."
            return False

        self.status.guessed_letters.add(letter)

        if letter in self.word:
            self._reveal_letter(letter)
            self.status.message = "SECTION DECRYPTED."
            self._check_win()
            return True
        else:
            self.status.breach_level += 1
            self.status.message = f"ERROR: INVALID KEY. BREACH LEVEL INCREASED TO {self.status.breach_level}."
            self._check_loss()
            return False

    def guess_word(self, guess: str) -> bool:
        guess = guess.upper()
        if guess == self.word:
            self.status.masked_word = list(self.word)
            self.status.won = True
            self.status.game_over = True
            self.status.message = "SYSTEM ACCESS GRANTED."
            return True
        else:
            self.status.breach_level += 1
            self.status.message = "PASSWORD REJECTED. BREACH LEVEL INCREASED."
            self._check_loss()
            return False

    def _reveal_letter(self, letter: str):
        for idx, char in enumerate(self.word):
            if char == letter:
                self.status.masked_word[idx] = letter

    def _check_win(self):
        if '_' not in self.status.masked_word:
            self.status.won = True
            self.status.game_over = True
            self.status.message = "SYSTEM ACCESS RESTORED."

    def _check_loss(self):
        if self.status.breach_level >= self.status.max_breach_level:
            self.status.game_over = True
            self.status.won = False
            self.status.message = "CRITICAL FAILURE. SYSTEM COMPROMISED."

    def to_dict(self):
        return {
            "status": self.status.to_dict(),
            "breach_stage_name": self.get_breach_stage_name(),
            "word_length": len(self.word)
        }

    def get_breach_stage_name(self) -> str:
        return self.BREACH_STAGES[min(self.status.breach_level, len(self.BREACH_STAGES)-1)]

    def get_hint(self) -> str:
        # Simple progressive hint logic
        hints = self.word_data.get('hints', [])
        if not hints:
            return "No hints available."
        
        # Returns the next available hint based on how many have been used
        # If all used, returns definition
        hint_idx = self.status.hints_used
        
        if hint_idx < len(hints):
            self.status.hints_used += 1
            return f"HINT: {hints[hint_idx]}"
        else:
             return f"DEFINITION: {self.word_data.get('definition', 'No definition.')}"
