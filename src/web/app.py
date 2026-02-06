from flask import Flask, render_template, jsonify, request
import sys
import os

# Add src to path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from logic.word_bank import WordBank
from logic.game_state import GameState
from logic.adaptive_engine import AdaptiveEngine

app = Flask(__name__)

# Global Game State (Simple in-memory storage for single player MVP)
# In a real multi-player app, this would be a database or session-based
current_game: GameState = None
adaptive_engine = AdaptiveEngine()
word_bank = None

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'words.yaml')

def init_word_bank():
    global word_bank
    try:
        word_bank = WordBank(DATA_PATH)
    except FileNotFoundError:
        print("CRITICAL: Word bank not found.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_game():
    global current_game, word_bank
    if not word_bank:
        init_word_bank()
    
    difficulty = adaptive_engine.get_recommended_difficulty()
    word_data = word_bank.get_word(difficulty)
    
    if not word_data:
        return jsonify({"error": "Database Error"}), 500

    current_game = GameState(word_data)
    return jsonify(current_game.to_dict())

@app.route('/api/guess', methods=['POST'])
def guess():
    global current_game
    if not current_game:
        return jsonify({"error": "No game active"}), 400

    data = request.json
    guess_input = data.get('guess', '').strip().upper()

    if not guess_input:
        return jsonify({"error": "Empty guess"}), 400

    if len(guess_input) == 1:
        current_game.guess_letter(guess_input)
    else:
        current_game.guess_word(guess_input)
    
    # Check for game end to record stats
    if current_game.status.game_over:
        adaptive_engine.record_result(current_game.status.won)

    response = current_game.to_dict()
    # Reveal word if game over
    if current_game.status.game_over:
        response['target_word'] = current_game.word

    return jsonify(response)

@app.route('/api/hint', methods=['POST'])
def hint():
    global current_game
    if not current_game:
        return jsonify({"error": "No game active"}), 400
    
    hint_text = current_game.get_hint()
    current_game.status.message = hint_text
    return jsonify(current_game.to_dict())

if __name__ == '__main__':
    init_word_bank()
    app.run(debug=True, port=5000)
