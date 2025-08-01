import pygame

from pygame.sprite import Sprite

import utilities as ults

class Alien(Sprite):

    # Class to represent a single alien in the grand alien fleet

    def __init__(self, gameSettings, screen):

        # Initialize the alien and set its starting position

        super().__init__()
        self.screen = screen
        self.gameSettings = gameSettings

        # Load the alien image and set its rect attribute
        alien_image_path = ults.resource_path("Game_Images/alien_basic.bmp")
        self.image = pygame.image.load(alien_image_path)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position

        self.x = float(self.rect.x)

    def update(self):

        # Move the Alien Left or Right
        self.x += (self.gameSettings.alien_speed_factor * self.gameSettings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):

        # Returns True is aliens is at the edge of the screen

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= screen_rect.left:
            return True

    def blitme(self):

        # Draw the alien at its current location

        self.screen.blit(self.image, self.rect)