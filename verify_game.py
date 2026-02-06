import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from logic.word_bank import WordBank
from logic.game_state import GameState
from logic.adaptive_engine import AdaptiveEngine

def test_game_flow():
    print("Testing WordBank...")
    wb = WordBank(os.path.join(os.path.dirname(__file__), 'data', 'words.yaml'))
    word = wb.get_word(1)
    if not word:
        print("FAIL: Could not load word.")
        return
    print(f"PASS: Loaded word: {word['word']}")

    print("\nTesting GameState (Scenario: Win)...")
    game = GameState(word)
    target = word['word']
    for char in target:
        game.guess_letter(char)
    
    if game.status.won:
        print("PASS: Game won correctly.")
    else:
        print(f"FAIL: Game not won after guessing {target}. Status: {game.status}")

    print("\nTesting GameState (Scenario: Loss)...")
    word2 = wb.get_word(1)
    game2 = GameState(word2)
    # Intentionally guess wrong 6 times
    bad_chars = "12345678"
    for char in bad_chars[:6]:
        game2.guess_letter(char)
        print(f"Breach Level: {game2.status.breach_level} ({game2.get_breach_stage_name()})")

    if game2.status.game_over and not game2.status.won:
        print("PASS: Game lost correctly.")
    else:
        print("FAIL: Game should be lost.")

    print("\nTesting Adaptive Engine...")
    engine = AdaptiveEngine()
    engine.record_result(True) # Win 1
    engine.record_result(True) # Win 2
    if engine.get_recommended_difficulty() == 2:
        print("PASS: Difficulty increased to 2.")
    else:
        print("FAIL: Difficulty did not increase.")

if __name__ == "__main__":
    test_game_flow()
