import pygame.font

import utilities as ults

class Scoreboard():

    # Class to report scoring information

    def __init__(self, gameSettings, screen, stats):

        # Initialize scorekeeping attributes

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.gameSettings = gameSettings
        self.stats = stats

        # Font setttings for scoreboard
        self.board_text_color = (225, 225, 225)
        self.title_text_color = (255, 0, 0)
        text_font_path = ults.resource_path("Text_Font/Emulogic-zrEw.ttf")
        self.font = pygame.font.Font(text_font_path, 24)

        # Set the initial score image
        self.set_score()
        self.set_high_score()
        self.set_stage_number()
        self.set_lives_left()

    def set_score(self):

        # Renders the score into an image

        # Title
        score_title_string = "Score"
        self.score_title_image = self.font.render(score_title_string, True, self.title_text_color)

        # Score
        rounded_score = int(round(self.stats.score, -1))
        score_string = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_string, True, self.board_text_color)

        # Display the score and the title at the top right corner of the screen

        self.score_title_rect = self.score_title_image.get_rect()
        self.score_title_rect.right = self.screen_rect.right - 20
        self.score_title_rect.top = self.screen_rect.top

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.score_title_rect.bottom

    def show_score(self):

        # Draw the scores and their titles to the screen
        self.screen.blit(self.score_title_image, self.score_title_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_title_image, self.high_score_title_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.stage_title_image, self.stage_title_rect)
        self.screen.blit(self.stage_num_image, self.stage_num_rect)
        self.screen.blit(self.lives_title_image, self.lives_title_rect)
        self.screen.blit(self.lives_num_image, self.lives_num_rect)

    def set_high_score(self):

        # Turn High Score into image

        # Title
        high_score_title_string = "High Score"
        self.high_score_title_image = self.font.render(high_score_title_string, True, self.title_text_color)

        # Score
        high_score = int(round(self.stats.high_score, -1))
        high_score_string = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_string, True, self.board_text_color)

        # Center high score and title to the top of the screen

        self.high_score_title_rect = self.high_score_title_image.get_rect()
        self.high_score_title_rect.centerx = self.screen_rect.centerx
        self.high_score_title_rect.top = self.screen_rect.top

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.high_score_title_rect.bottom

    def set_stage_number(self):

        # Renders the current level into an image

        # Title
        stage_title_string = "Stage:"
        self.stage_title_image = self.font.render(stage_title_string, True, self.title_text_color)

        # Stage
        stage_num_string = "{:,}".format(self.stats.stage_number)
        self.stage_num_image = self.font.render(stage_num_string, True, self.board_text_color)

        # Displays the stage and the title at the top left corner of the screen

        self.stage_title_rect = self.stage_title_image.get_rect()
        self.stage_title_rect.left = self.screen_rect.left + 20
        self.stage_title_rect.top = self.screen_rect.top

        self.stage_num_rect = self.stage_num_image.get_rect()
        self.stage_num_rect.left = self.stage_title_rect.right
        self.stage_num_rect.top = self.screen_rect.top

    def set_lives_left(self):

        # Renders the current number of lives into an image

        # Title
        lives_title_string = "Lives:"
        self.lives_title_image = self.font.render(lives_title_string, True, self.title_text_color)

        # Lives
        lives_num_string = "{:,}".format(self.stats.ships_left)
        self.lives_num_image = self.font.render(lives_num_string, True, self.board_text_color)

        # Display the number of lives and the title at the top left corner of the screen, below the stage number

        self.lives_title_rect = self.stage_title_image.get_rect()
        self.lives_title_rect.left = self.screen_rect.left + 20
        self.lives_title_rect.top = self.stage_title_rect.bottom

        self.lives_num_rect = self.stage_num_image.get_rect()
        self.lives_num_rect.left = self.lives_title_rect.right
        self.lives_num_rect.top = self.stage_num_rect.bottom