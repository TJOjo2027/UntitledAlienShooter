import pygame.font

import utilities as ults

class Button():

    def __init__(self, gameSettings, screen, message):

        # Initialize button attributes
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.width = 200
        self.height = 50
        self.text_color = (255, 255, 255)
        text_font_path = ults.resource_path("Text_Font/Emulogic-zrEw.ttf")
        self.font = pygame.font.Font(text_font_path, 45)

        # Build the button's rect and center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Prep button message
        self.set_message(message)

    def set_message(self, message):

        # Turns the message into a rendered image and center text on the button
        self.message_image = self.font.render(message, True, self.text_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):

        # Draw blank button and then draw message
        self.screen.blit(self.message_image, self.message_image_rect)