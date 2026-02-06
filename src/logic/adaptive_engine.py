class AdaptiveEngine:
    def __init__(self):
        self.player_wins = 0
        self.player_losses = 0
        self.streak = 0

    def record_result(self, won: bool):
        if won:
            self.player_wins += 1
            self.streak += 1
        else:
            self.player_losses += 1
            self.streak = 0

    def get_recommended_difficulty(self) -> int:
        # Simple logic: increase difficulty every 2 consecutive wins
        # Decrease if losing streak > 1 (not implemented yet, just base logic)
        if self.streak >= 2:
            return 2 # Harder
        elif self.streak >= 4:
            return 3 # Hardest
        else:
            return 1 # Normal
