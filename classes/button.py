import pygame
from misc.config import WIDTH, HEIGHT
from classes.board import Tile
from classes.figure import Figure
from misc.images import *

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




rotate_button = Button(WIDTH+20, 50, 150, 50, "Rotate Board", (0, 255, 0), (0, 200, 0), (0, 0, 0), True, None)
active_piece_button = Button(WIDTH+20, 150, 100, 50, " ", (0, 0, 0), (0, 0, 0), (255, 255, 255), False, None)
eval_button = Button(WIDTH+40, 100, 100, 50, "Evaluation: 0.3", (0, 0, 0), (0, 0, 0), (255, 255, 255), False, None)
promotion_queen = Button(125, 350, 100, 100, "", (0, 0, 0), (0, 0, 0), (255, 255, 255), False, None) 
promotion_rook = Button(275, 350, 100, 100, "", (0, 0, 0), (0, 0, 0), (255, 255, 255), False, None) 
promotion_knight = Button(425, 350, 100, 100, "", (0, 0, 0), (0, 0, 0), (255, 255, 255), False, None) 
promotion_bishop = Button(575, 350, 100, 100, "", (0, 0, 0), (0, 0, 0), (255, 255, 255), False, None) 
promotion_queen.images = [white_queen_img, black_queen_img]
promotion_queen.piece = Figure.FigureType.Queen
promotion_rook.images = [white_rook_img, black_rook_img]
promotion_rook.piece = Figure.FigureType.Rook
promotion_bishop.images = [white_bishop_img, black_bishop_img]
promotion_bishop.piece = Figure.FigureType.Bishop
promotion_knight.images = [white_knight_img, black_knight_img]
promotion_knight.piece = Figure.FigureType.Knight
promotion_choice  = [promotion_bishop, promotion_knight, promotion_queen, promotion_rook]
game_over_button = Button(325, 350, 100, 100, "Play again", (0, 255, 0), (0, 200, 0), (0, 0, 0), True, None)