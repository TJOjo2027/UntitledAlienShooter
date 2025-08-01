import json

import utilities as ults

class GameStats():

    def __init__(self, gameSettings):

        # Initialize Statistics

        self.gameSettings = gameSettings
        self.reset_stats()

        # Start Untitiled Alien Shooter when game_active is TRUE
        self.game_active = False

        # Opens Options Menu when options_active is TRUE
        self.options_active = False

        # Puts the game in a game over state, where the player can either quit or play again
        self.game_over = False

        # High score (never reset, only updated)

        self.load_high_score()

    def reset_stats(self):

        # Initialize statistics that can change throughout the game

        self.ships_left = self.gameSettings.ship_limit
        self.score = 0
        self.stage_number = 1

        # Stat for number aliens destroyed
        self.num_aliens_destroyed = 0

        # Stat for number bullets shot
        self.num_bullets_fired = 0

        # Stats for number of bullets that have missed and left the screen
        self.missed_bullets = 0

    def load_high_score(self):
        try:
            high_score_file_path = ults.resource_path("Saves/high_score.json")
            with open(high_score_file_path, "r") as File:
                file_contents = json.load(File)
                self.high_score = file_contents.get("high_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.high_score = 0
