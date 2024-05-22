import pygame

pygame.init()

WIDTH = 800
HEIGHT = WIDTH
RIGHT_BAR = 200
TILE_SIZE = int(WIDTH/8)
screen = pygame.display.set_mode([WIDTH+RIGHT_BAR, HEIGHT])
font = pygame.font.Font('freesansbold.ttf', 20)
timer = pygame.time.Clock()
fps = 60
run = True

ENGINE_PATH = "./stockfish/stockfish-windows-x86-64-sse41-popcnt.exe"
AI_LEVEL = 1 #0-20


