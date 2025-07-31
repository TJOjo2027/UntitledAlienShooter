import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
    
    # Class used to manage pullet fired from the ship

    def __init__(self, gameSettings, screen, ship):

        # Create a Bullet Object and the Ship's current position
        
        super().__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position

        self.rect = pygame.Rect(0, 0, gameSettings.bullet_width, gameSettings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value

        self.y = float(self.rect.y)

        self.color = gameSettings.bullet_color
        self.speed_factor = gameSettings.bullet_speed_factor
    
    def update(self):

        # Move the bullet up the screen

        # Update the decimal position of the bullet

        self.y -= self.speed_factor

        # Update the rect position

        self.rect.y = self.y

    def draw_bullet(self):

        # Draw the bullet to the screen

        pygame.draw.rect(self.screen, self.color, self.rect)

    