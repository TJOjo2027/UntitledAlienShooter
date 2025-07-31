import pygame

class ImageButton:
    def __init__(self, screen, image_path, image_scale):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        scaled_width = image_scale * self.image.get_width()
        scaled_height = image_scale * self.image.get_height()
        scaled_coords = (scaled_width, scaled_height)
        self.image = pygame.transform.scale(self.image, scaled_coords)

        self.rect = self.image.get_rect()

    def draw_button(self):
        self.screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def change_orientation(self, image_attribute_name, screen_attribute_name):

        # Takes the image_attribute_name (like right) and sets it to a screen_attribute_name (like right)!
        setattr(self.rect, image_attribute_name, getattr(self.screen.get_rect(), screen_attribute_name))