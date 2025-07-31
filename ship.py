import pygame

import game_functions as gf

class Ship():

    def __init__(self, game_settings, screen):

        # Initialize the Ship and configure its starting position
        self.screen = screen
        self.game_settings = game_settings

        # Load the ship image
        ship_image_path = gf.resource_path("Game_Images/ship.bmp")
        self.image = pygame.image.load(ship_image_path)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start the new Ship at the bottom center of the Screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)

        # Movement Flags

        self.move_right = False
        self.move_left = False

    def update(self):

        # Update the ship's center value (not the rect) based on its movement flags
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor
        if self.move_left and self.rect.left > self.screen_rect.left:
            self.center -= self.game_settings.ship_speed_factor

        self.rect.centerx = self.center

    def center_ship(self):
        
        # Center the ship on screen

        self.center = self.screen_rect.centerx

    def blitme(self):

        # Draw the ship in its current location
        self.screen.blit(self.image, self.rect)