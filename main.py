import sys
import os

# Add src to path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from logic.word_bank import WordBank
from logic.game_state import GameState
from logic.adaptive_engine import AdaptiveEngine
from ui.terminal_ui import TerminalUI
from rich.prompt import Prompt

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'words.yaml')

def main():
    ui = TerminalUI()
    try:
        word_bank = WordBank(DATA_PATH)
    except FileNotFoundError as e:
        ui.print_message(f"Critical Error: {e}", style="bold red")
        return

    adaptive_engine = AdaptiveEngine()
    
    while True:
        # Start new round
        difficulty = adaptive_engine.get_recommended_difficulty()
        word_data = word_bank.get_word(difficulty)
        
        if not word_data:
            ui.print_message("Error: Database Corrupted (No words found).", style="bold red")
            break
            
        game = GameState(word_data)
        
        # Game Loop
        while not game.status.game_over:
            ui.clear()
            ui.render_game_screen(game, game.status.message)
            
            user_input = Prompt.ask("ACTION").strip().upper()
            
            if user_input == 'EXIT':
                ui.print_message("Session Terminated by User.")
                return
            elif user_input == 'HINT':
                hint = game.get_hint()
                game.status.message = hint
            elif len(user_input) == 1 and user_input.isalpha():
                game.guess_letter(user_input)
            elif len(user_input) > 1 and user_input.isalpha():
                game.guess_word(user_input)
            else:
                 game.status.message = "INVALID INPUT. ENTER A LETTER."

        # End of Round
        ui.clear()
        ui.render_game_screen(game)
        
        if game.status.won:
            ui.print_message(f"\nSUCCESS. Target Decrypted: {game.word}", style="bold green")
            adaptive_engine.record_result(True)
        else:
            ui.print_message(f"\nFAILURE. System Compromised. Target was: {game.word}", style="bold red")
            adaptive_engine.record_result(False)
            
        if Prompt.ask("\nRe-initialize System? (Y/N)").upper() != 'Y':
            break

    ui.print_message("\nSECURE ACCESS SYSTEM SHUTTING DOWN...", style="dim white")

if __name__ == "__main__":
    main()
