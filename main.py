import pygame
from pygame.math import Vector2
from classes.figure import Figure, pieces, Tile
from classes.board import Board
from classes.button import Button
from misc.config import *
from misc.images import *

rotated = False

def next_turn():
    global turn
    if turn == Tile.TileColor.White:
        turn = Tile.TileColor.Black
    elif turn == Tile.TileColor.Black:
        turn = Tile.TileColor.White


def rotate_board():
    global rotated
    print("Rotating the board...")
    rotated = not rotated

active_piece = None
rotate_button = Button(WIDTH+20, 50, 150, 50, "Rotate Board", (0, 255, 0), (0, 200, 0), (0, 0, 0), True, rotate_board)
active_piece_button = Button(WIDTH+20, 150, 100, 50, " ", (0, 0, 0), (0, 0, 0), (255, 255, 255), False, None)
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


def draw_board():
    global screen, board, pieces, TILE_SIZE, rotated, turn, active_piece, rotate_button, font, previous_piece
    screen.fill((0,0,0))
    board.display(screen, rotated)
    for piece in pieces:
        piece.render(screen, TILE_SIZE, rotated, turn)
    if active_piece:
        active_piece.render(screen, TILE_SIZE, rotated, turn, previous_piece)  
    rotate_button.draw(screen, font)
    active_piece_button.draw(screen, font)

def draw_promotion_menu():
    
    if previous_piece.color == Tile.TileColor.White:
        background = pygame.Surface((700, 300))
        background.set_alpha(220) 
        background.fill('black')
        text = font.render("Choose promotion piece:", True, 'white')
    else:
        background = pygame.Surface((700, 300))
        background.set_alpha(60) 
        background.fill('white')
        text = font.render("Choose promotion piece:", True, 'black')
    screen.blit(background, (50, 250))

    screen.blit(text,(270,300))

    for button in promotion_choice:
        button.draw(screen, font, previous_piece.color)


def tick():
    global timer, fps, promotion
    timer.tick(fps)
    draw_board()
    if promotion:
        draw_promotion_menu()
    pygame.display.flip()

#main
if __name__ == '__main__':
    board = Board(WIDTH,HEIGHT,TILE_SIZE, pieces)
    white_captured = []
    black_captured = []
    previous_piece = None
    promotion = False
    promotedTo = None
    turn = Tile.TileColor.White
    for piece in pieces:
        piece.set_board(board)


    while run:
        #event handling
        for event in pygame.event.get():

            if promotion:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #click on promotion piece
                        for button in promotion_choice:
                            if button.colide(event.pos):
                                promotedTo = button.click()
                                if promotedTo:
                                    previous_piece.figureType = promotedTo
                                    promotion = False
                                    promotedTo = None
                elif event.type == pygame.QUIT:
                    run = False

            else:
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
                                figure: Figure = board.grid[x][y].content


                                #move piece
                                if active_piece and Vector2(x,y) in active_piece.legal_moves:
                                    promotion = active_piece.move(x,y, white_captured, black_captured)
                                    active_piece.active = False
                                    active_piece.is_last_move = True
                                    if previous_piece:
                                        previous_piece.is_last_move = False
                                    previous_piece = active_piece
                                    board.grid[int(previous_piece.position.x)][int(previous_piece.position.y)].content = None
                                    board.grid[x][y].content = active_piece
                                    active_piece = None
                                    next_turn()
                                    


                                #select piece
                                elif figure and figure.color == turn:
                                    figure.active = not figure.active
                                    
                                    figure.activeAnimation = True
                                    active_piece_button.text = figure.color.name + " " + figure.figureType.value
                                    if active_piece:
                                        active_piece.active = False
                                    if figure.active:
                                        active_piece: Figure = figure
                                        active_piece.get_legal_moves(previous_piece)
                                        active_piece.delete_illegal_moves()
                                        active_piece.availible_castling()
                                    else:
                                        active_piece = None
            tick()
    pygame.quit()

