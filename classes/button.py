import pygame
from misc.config import WIDTH, HEIGHT
from classes.board import Tile

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, show_hover, function=None):
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
        self.images = []
        self.piece = None

    def colide(self, mousePos):
        if self.x < mousePos[0] < self.x + self.width and self.y < mousePos[1] < self.y + self.height:
            return True
        return False

    def draw(self, screen, font, player: Tile.TileColor = None):
        if self.images:
            if player == Tile.TileColor.White:
                screen.blit(self.images[0],(self.x, self.y))
                background = pygame.Surface((100, 100))
                background.set_alpha(30) 
                background.fill('white')
            else:
                screen.blit(self.images[1],(self.x, self.y))
                background = pygame.Surface((100, 100))
                background.set_alpha(30) 
                background.fill('black')
                
            if self.colide(pygame.mouse.get_pos()):
                screen.blit(background, (self.x, self.y))
        else:
            if self.colide(pygame.mouse.get_pos()) and self.show_hover:
                pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            screen.blit(text_surface, text_rect)

    def click(self):
        if self.piece:
            return self.piece
        if self.function:
            self.function()


