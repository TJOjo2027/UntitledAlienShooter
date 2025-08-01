import pygame

from pygame.sprite import Sprite

from alien import Alien

import utilities as ults

class TreasureAlien(Alien):
    def __init__(self, gameSettings, screen):

        super().__init__(gameSettings, screen)

        treasure_alien_path = ults.resource_path("Game_Images/alien_treasure.bmp")
        self.image = pygame.image.load(treasure_alien_path)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)