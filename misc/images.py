import pygame
import pygame.locals
from misc.config import TILE_SIZE

black_rook_img = pygame.transform.scale(pygame.image.load("images/black_rook.png"), (TILE_SIZE, TILE_SIZE))
black_bishop_img = pygame.transform.scale(pygame.image.load("images/black_bishop.png"), (TILE_SIZE, TILE_SIZE))
black_knight_img = pygame.transform.scale(pygame.image.load("images/black_knight.png"), (TILE_SIZE, TILE_SIZE))
black_king_img = pygame.transform.scale(pygame.image.load("images/black_king.png"), (TILE_SIZE, TILE_SIZE))
black_queen_img = pygame.transform.scale(pygame.image.load("images/black_queen.png"), (TILE_SIZE, TILE_SIZE))
black_pawn_img = pygame.transform.scale(pygame.image.load("images/black_pawn.png"), (TILE_SIZE, TILE_SIZE))

white_rook_img = pygame.transform.scale(pygame.image.load("images/white_rook.png"), (TILE_SIZE, TILE_SIZE))
white_bishop_img = pygame.transform.scale(pygame.image.load("images/white_bishop.png"), (TILE_SIZE, TILE_SIZE))
white_knight_img = pygame.transform.scale(pygame.image.load("images/white_knight.png"), (TILE_SIZE, TILE_SIZE))
white_king_img = pygame.transform.scale(pygame.image.load("images/white_king.png"), (TILE_SIZE, TILE_SIZE))
white_queen_img = pygame.transform.scale(pygame.image.load("images/white_queen.png"), (TILE_SIZE, TILE_SIZE))
white_pawn_img = pygame.transform.scale(pygame.image.load("images/white_pawn.png"), (TILE_SIZE, TILE_SIZE))
legal_move_img = pygame.transform.scale(pygame.image.load("images/legal_move.png"), (TILE_SIZE, TILE_SIZE))
