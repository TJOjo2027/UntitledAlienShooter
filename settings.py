class Settings():
    # A class that stores settings for Untitled Alien Shooter!

    def __init__(self):

        # Initialize the game's default settings

        # Screen Settings
        self.screen_width = 1500
        self.screen_height = 750
        self.background_color = (0, 0, 0)

        # Ship Settings
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_width = 6
        self.bullet_height = 30
        self.bullet_color = (251, 254, 217)
        self.bullets_allowed = 5

        # Alien Settings
        self.fleet_drop_speed = 5

        # Difficulty Scaling
        self.diff_scale = 1.1

        # Score Scaling
        self.score_scale = 1.5

        self.init_dynamic_speed_factors()

    def init_dynamic_speed_factors(self):

        # Set the difficulty scalling factors

        self.ship_speed_factor = 0.5
        self.bullet_speed_factor = 1.5
        self.alien_speed_factor = 0.1

        # Scoring
        self.alien_points = 50

        # For fleet directions, 1 is right, -1 is left
        self.fleet_direction = 1
    
    def increase_speed(self):

        # Increase the game difficulty through speed
    
        self.ship_speed_factor *= self.diff_scale
        self.bullet_speed_factor *= self.diff_scale
        self.alien_speed_factor *= self.diff_scale
        self.alien_points = int(self.alien_points * self.score_scale)