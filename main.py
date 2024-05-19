import pygame
from pygame.math import Vector2
from classes.figure import Figure, pieces
from classes.board import Board
from classes.button import Button
from misc.config import *

rotated = False

def rotate_board():
    global rotated
    print("Rotating the board...")
    rotated = not rotated

active_piece = None
rotate_button = Button(WIDTH+20, 50, 150, 50, "Rotate Board", (0, 255, 0), (0, 200, 0), (0, 0, 0), True, rotate_board)
active_piece_button = Button(WIDTH+20, 150, 100, 50, " ", (0, 0, 0), (0, 0, 0), (255, 255, 255), False, None)

def tick():
    global timer, fps, screen, pieces, rotate_button
    timer.tick(fps)
    screen.fill((0,0,0))
    board.display(screen, rotated)
    for piece in pieces:
        piece.render(screen, TILE_SIZE, rotated)
    if active_piece:
        active_piece.render(screen, TILE_SIZE, rotated, previous_piece)  
    rotate_button.draw(screen, font)
    active_piece_button.draw(screen, font)
    pygame.display.flip()

#main
if __name__ == '__main__':
    board = Board(WIDTH,HEIGHT,TILE_SIZE, pieces)
    white_captured = []
    black_captured = []
    previous_piece = None
    for piece in pieces:
        piece.set_board(board)
    while run:

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in board.grid:
                        for tile in row:
                            print(tile.color)
                        print()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #clicked on rotate button
                    if rotate_button.x < event.pos[0] < rotate_button.x + rotate_button.width \
                        and rotate_button.y < event.pos[1] < rotate_button.y + rotate_button.height:
                        rotate_button.click()
                    #clicked on board
                    else:
                        x,y = event.pos
                        x = int(x/TILE_SIZE)
                        y = int(y/TILE_SIZE)
                        if rotated:
                            x = 7-x
                            y = 7-y
                        if 0 <= x <= 7 and 0 <= y <= y:
                            print(f"kliknieto w: {chr(x + 97)}{8-y}")
                            figure: Figure = board.grid[x][y].content


                            #move piece
                            if active_piece and Vector2(x,y) in active_piece.legal_moves:
                                active_piece.move(x,y, white_captured, black_captured, previous_piece)
                                active_piece.active = False
                                active_piece.is_last_move = True
                                if previous_piece:
                                    previous_piece.is_last_move = False
                                previous_piece = active_piece
                                active_piece = None

                            #select piece
                            elif figure:
                                print(f"kliknieto w figure: {figure.figureType.value}")
                                figure.active = not figure.active
                                figure.activeAnimation = True
                                active_piece_button.text = figure.color.name + " " + figure.figureType.value
                                if active_piece:
                                    active_piece.active = False
                                if figure.active:
                                    active_piece: Figure = figure
                                else:
                                    previous_piece = active_piece
                                    active_piece = None






        
        tick()
    pygame.quit()

