from enum import Enum
import pygame
from pygame.math import Vector2
#from classes.figure import Figure
from misc.config import font
class Tile:

    def __init__(self, color: 'TileColor',x: int,y: int, pieces: list[any])-> None:
        self.color = color
        self.position = Vector2(x,y)
        self.content = None
        for piece in pieces:
            if piece.position == self.position:
                self.content = piece
                piece.tile = self

    class TileColor(Enum):
        Black = 'burlywood4'
        White = 'burlywood3'

        def equal(self, other) -> bool:
            return self.name == other.name


                


class Board:
    def __init__(self, width: int, height: int, tile_size: int, pieces: list[any]) -> None:
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.grid: list[list[Tile]] = None
        #self.tiles: list[Tile] = [self.grid[i][j] for i in range (8) for j in range (8)]
        self.color_map = {
            'Black': (115, 77, 38),
            'White': (210, 166, 121)
        }

    def display(self, screen, rotated: bool):
        for j in range(8):
            for i in range(8):
                if rotated:
                    color = self.grid[7-j][7-i].color.value
                else:
                    color = self.grid[j][i].color.value
                pygame.draw.rect(screen, color, pygame.Rect(i * self.tile_size, j * self.tile_size, self.tile_size, self.tile_size))

        #kolumny
        for i in range(8):
            if rotated:
                x = (7-i) * self.tile_size + 1
                y = 8 * self.tile_size -20
                index = i
            else:
                x = i * self.tile_size + 1
                y = 8 * self.tile_size -20
                index = 7-i
            text_surface = font.render(chr(i + 97), True, self.grid[index][7].color.value)  
            screen.blit(text_surface, (x, y)) 

        #wiersze
        for j in range(8):
            if rotated:
                x = 8 * self.tile_size - 15
                y = j * self.tile_size + 1
                index = 7-j
            else:
                x = 8 * self.tile_size - 15
                y = (7-j) * self.tile_size + 1
                index = j

            
            text_surface = font.render(str(j + 1), True, self.grid[7][index].color.value) 
            screen.blit(text_surface, (x, y)) 