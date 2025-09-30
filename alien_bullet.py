import pygame

from pygame.sprite import Sprite

from bullet import Bullet

class AlienBullet(Bullet):
    
    def __init__(self, gameSettings, screen, alien):
        # Create a Bullet Object and the Ship's current position
        
        super().__init__(gameSettings, screen, alien)
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set correct position

        self.bullet_width = 6
        self.bullet_height = 30
        self.rect = pygame.Rect(0, 0, self.bullet_width, self.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        # Store the bullet's position as a decimal value

        self.y = float(self.rect.y)
        self.color = gameSettings.bullet_color
        self.speed_factor = gameSettings.bullet_speed_factor
    
    def update(self):
        # Move the bullet down the screen

        # Update the decimal position of the bullet

        self.y += self.speed_factor * 0.35

        # Update the rect position

        self.rect.y = self.y

    
def draw_bullet(self):
    pygame.draw.rect(self.screen, self.color, self.rect)