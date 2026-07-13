class GameState:

    def __init__(self):
        self._is_game_over = False

    def is_game_over(self):
        return self._is_game_over

    def mark_game_over(self):
        self._is_game_over = True
