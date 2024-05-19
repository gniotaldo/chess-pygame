import pygame
from misc.config import WIDTH, HEIGHT

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, show_hover, function=None,):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.function = function
        self.show_hover = show_hover
        self.text_color = text_color

    def draw(self, screen, font):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height and self.show_hover:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

    def click(self):
        if self.function:
            self.function()


