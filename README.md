# Hangman


A retro-futuristic terminal hacking simulation inspired by the Fallout series. Test your deduction skills by guessing the correct password from a clutter of characters.

## 🌟 Features

- **Dual Interfaces**:
  - **CLI Mode**: Authentic terminal experience using Python `rich`.
  - **Web Mode**: Browser-based interface with CRT effects and responsive design.
- **Adaptive Difficulty**: The system analyzes your win/loss ratio and adjusts word length and complexity dynamically.
- **Visuals**: Immersive "green screen/amber" aesthetic.

## 🛠️ Prerequisites

- Python 3.8 or higher
- `pip` (Python Package Manager)

## 🚀 Installation

1. **Clone the repository** (or download source):
   ```bash
   git clone <repository-url>
   cd secure_access_system
   ```

2. **Set up the environment**:
   ```bash
   # Windows (Fast Setup)
   run_game.bat
   ```
   
   *Or manually:*
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🎮 How to Play

### CLI Version
Launch the desktop terminal version:
```bash
run_game.bat
# OR
python main.py
```

### Web Version
Launch the local web server:
```bash
run_web.bat
# OR
python src/web/app.py
```
Open your browser to `http://127.0.0.1:5000`.

## ☁️ Deployment

### Deploy to Vercel
This project is configured for easy deployment on [Vercel](https://vercel.com).

1. Install Vercel CLI: `npm i -g vercel`
2. Run deployment:
   ```bash
   vercel
   ```
   
*Configuration is handled automatically via `vercel.json`.*

## 📂 Project Structure

```
secure_access_system/
├── data/               # Game data (word usage stats, word lists)
├── src/
│   ├── logic/          # Core game logic (Engine, State, WordBank)
│   ├── ui/             # CLI Interface modules
│   └── web/            # Flask Web Application
├── main.py             # CLI Entry point
├── run_game.bat        # CLI Launcher script
├── run_web.bat         # Web Launcher script
├── requirements.txt    # Python dependencies
└── vercel.json         # Deployment configuration
```


