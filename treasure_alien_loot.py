from alien_bullet import AlienBullet

import pygame

from random import randint, choice

class TreasureAlienLoot(AlienBullet):

    def __init__(self, gameSettings, screen, alien):
        super().__init__(gameSettings, screen, alien)

        # Create Bullet rect
        self.bullet_width = 30
        self.bullet_height  = 30
        self.rect = pygame.Rect(0, 0, self.bullet_width, self.bullet_height)
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom

        self.Drop_Dictionary = self.Create_Drop_Dictionary()

        self.color = self.Roll_Drop_Color()
    
    def update(self):
        # Move the treasure loot down the screen

        # Update the decimal position of the bullet

        self.y += 0.25

        # Update the rect position

        self.rect.y = self.y
    
    def Create_Drop_Dictionary(self):
        
        # Create of Dictionary of PowerUp - Color Pairs

        # Shield Should Be Blue
        # Main Peircing Should be Yellow
        # 1-UP Should Be Green
        # Bullet Speed Up Should Be Pink
        # Bullet Size Up Should Be Red

        Drop_Dict = {"Shield" : (59, 255, 252),
                        "Main Piercing" : (255, 234, 0),
                              "1-UP" : (82, 255, 59),
                                "Bullet Speed Up" : (255, 84, 252),
                                  "Bullet Size Up" : (255, 61, 61)}
        
        return Drop_Dict
        
    def Roll_Drop_Color(self):
        
        return choice(list(self.Drop_Dictionary.values()))
    
    def Loot_Effects(self, Bullet_Color, stats, gameSettings, scoreboard):
        if Bullet_Color == self.Drop_Dictionary["Shield"]:
            stats.Shields += 1
            scoreboard.set_shields_left()
            print("Shield")

        elif Bullet_Color == self.Drop_Dictionary["Main Piercing"]:
            stats.Main_Piercing = False
            print("MP")

        elif Bullet_Color == self.Drop_Dictionary["1-UP"]:
            stats.ships_left += 1
            scoreboard.set_lives_left()
            print("1 UP")

        elif Bullet_Color == self.Drop_Dictionary["Bullet Speed Up"]:
            stats.Bullet_Speed_Up += 0.5
            gameSettings.bullet_speed_factor += stats.Bullet_Speed_Up
            print("BSpeedU")

        elif Bullet_Color == self.Drop_Dictionary["Bullet Size Up"]:
            stats.Bullet_Size_Up += 5
            gameSettings.bullet_width += stats.Bullet_Size_Up
            print("BSizeU")