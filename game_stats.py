import json

class GameStats():

    def __init__(self, gameSettings):

        # Initialize Statistics

        self.gameSettings = gameSettings
        self.reset_stats()

        # Start Untitiled Alien Shooter when game_active is TRUE
        self.game_active = False

        # Opens Options Menu when options_active is TRUE
        self.options_active = False

        # High score (never reset, only updated)

        self.load_high_score()

    def reset_stats(self):

        # Initialize statistics that can change throughout the game

        self.ships_left = self.gameSettings.ship_limit
        self.score = 0
        self.stage_number = 1

    def load_high_score(self):
        try:
            with open("Saves/high_score.json", "r") as File:
                file_contents = json.load(File)
                self.high_score = file_contents.get("high_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.high_score = 0
