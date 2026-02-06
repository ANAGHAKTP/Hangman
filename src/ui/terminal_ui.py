from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
import os

class TerminalUI:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_game_screen(self, game_state, message: str = ""):
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        self.layout["main"].split_row(
            Layout(name="status", ratio=1),
            Layout(name="game_area", ratio=2),
        )

        # Header
        self.layout["header"].update(
             Panel(Align.center(Text("SECURE ACCESS TERMINAL v1.0", style="bold green")), style="green")
        )

        # Status Panel (Left)
        breach_text = Text()
        breach_text.append(f"\nBREACH STAGE:\n", style="bold white")
        
        stages = game_state.BREACH_STAGES
        current_stage_idx = min(game_state.status.breach_level, len(stages) - 1)
        
        for idx, stage in enumerate(stages):
            if idx < current_stage_idx:
                 breach_text.append(f"[X] {stage}\n", style="dim red")
            elif idx == current_stage_idx:
                 breach_text.append(f"[!] {stage} <ACTIVE>\n", style="bold red blink")
            else:
                 breach_text.append(f"[ ] {stage}\n", style="green")

        breach_text.append(f"\nGuessed Letters:\n{', '.join(sorted(game_state.status.guessed_letters))}", style="cyan")

        self.layout["status"].update(
            Panel(breach_text, title="SYSTEM STATUS", border_style="red" if game_state.status.breach_level > 0 else "green")
        )

        # Game Area (Right)
        word_display = " ".join(game_state.status.masked_word)
        
        # Build renderables for the central area
        from rich.console import Group
        
        game_elements = [
            Text("\n\n"),
            Align.center(Text(word_display, style="bold yellow on black")),
            Text("\n\n")
        ]
        
        if message:
            game_elements.append(Align.center(Text(f"> {message}", style="bold white")))

        self.layout["game_area"].update(
            Panel(Group(*game_elements), title="DECRYPTION INTERFACE", border_style="yellow")
        )
        
        # Footer
        self.layout["footer"].update(
             Panel(Align.center(Text("Type a letter to guess, 'HINT' for a clue, or 'EXIT' to quit.", style="italic grey50")))
        )

        self.console.print(self.layout)

    def print_message(self, message: str, style: str = "bold white"):
        self.console.print(message, style=style)
