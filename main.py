import pygame
from pygame.math import Vector2
from classes.figure import Figure, pieces, white_pieces, black_pieces, black_king, white_king, Tile
from classes.board import Board
from classes.button import *
from misc.config import *
from misc.images import *
from misc.dictionary import *
from copy import deepcopy
import time
from misc.sounds import *
from stockfish import Stockfish
from time import sleep


def next_turn():
    global turn, stockfish

    info = stockfish.get_evaluation()
    evaluation = info['value']
    evaluation_type = info['type']
    if evaluation_type == 'mate':
        eval_button.text = f"Mate in {abs(evaluation)}"
    else:
        eval_button.text = f"Evaluation: {evaluation/100.00}"

    if turn == Tile.TileColor.White:
        turn = Tile.TileColor.Black
        return False
    elif turn == Tile.TileColor.Black:
        turn = Tile.TileColor.White
        return True
    

def rotate_board():
    global rotated
    print("Rotating the board...")
    rotated = not rotated

def play_again():
    global moves_counter, board, white_captured, black_captured, previous_piece, promotion, promotedTo, is_game_over, turn, pieces, initialBoard, initialPieces,black_pieces, white_pieces, black_king, white_king
    pieces = deepcopy(initialPieces)
    black_pieces = [piece for piece in pieces if piece.color == Tile.TileColor.Black]
    white_pieces = [piece for piece in pieces if piece.color == Tile.TileColor.White]
    black_king = [piece for piece in black_pieces if piece.figureType == Figure.FigureType.King][0]
    white_king = [piece for piece in white_pieces if piece.figureType == Figure.FigureType.King][0]
    board = Board(WIDTH,HEIGHT,TILE_SIZE, pieces)
    board.grid = [[Tile(Tile.TileColor.Black, j, i, pieces) if ((i+j) % 2 == 1) else Tile(Tile.TileColor.White, j, i, pieces) for i in range(8)] for j in range(8)]
    white_captured = []
    black_captured = []
    previous_piece = None
    promotion = False
    promotedTo = None
    is_game_over = False
    turn = Tile.TileColor.Black
    next_turn()
    previous_piece = None
    moves_counter = 0
    draw_board()  # Update the display immediately after res +=    rint("nowa gra")

def draw_board():
    global screen, board, pieces, TILE_SIZE, rotated, turn, active_piece, rotate_button, font, previous_piece
    screen.fill((0,0,0))
    board.display(screen, rotated)
    for piece in pieces:
        piece.render(screen, TILE_SIZE, rotated, turn, previous_piece)
    if active_piece:
        active_piece.render(screen, TILE_SIZE, rotated, turn, previous_piece)  
    rotate_button.draw(screen, font)
    active_piece_button.draw(screen, font)
    eval_button.draw(screen, font)

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

def draw_game_over():
        background = pygame.Surface((700, 300))
        background.set_alpha(240) 
        background.fill('black')
        if black_king.is_check(black_king.position) or white_king.is_check(white_king.position):
            text = font.render(f"Game Over: {previous_piece.color.name} Won!", True, 'white')
        else:
            text = font.render(f"Draw", True, 'white')

        screen.blit(background, (50, 250))
        screen.blit(text,(270,300))
        game_over_button.draw(screen, font)

def game_over(board: Board):
    global previous_piece
    if previous_piece:
        if previous_piece.color == Tile.TileColor.White:
            pieces = black_pieces
        else:
            pieces = white_pieces
        canMove = False
        for piece in pieces:
                if piece.position != Vector2(8,8):
                    piece.get_legal_moves(previous_piece)
                    piece.delete_illegal_moves()
                    piece.availible_castling()
                    if piece.legal_moves != []:
                        canMove = True
                        break
        return not(canMove)
    return False

def tick():
    global timer, fps, promotion
    timer.tick(fps)
    draw_board()
    if promotion:
        draw_promotion_menu()
    if is_game_over:
        draw_game_over()
    pygame.display.flip()

def fen(board: Board):
    global stockfish
    res = ""
    
    tiles = [board.grid[x][y].content for y in range(8) for x in range(8)]
    blanks = 0
    for index, tile in enumerate(tiles):
        if index != 0 and index % 8 == 0:
            if blanks != 0:
                res += str(blanks)
            blanks = 0
            res += "/"
        if tile:
            if blanks != 0:
                res += str(blanks)
                blanks = 0
            if tile.figureType == Figure.FigureType.Pawn:
                char = "p"
            elif tile.figureType == Figure.FigureType.Knight:
                char = "n"
            elif tile.figureType == Figure.FigureType.Bishop:
                char = "b"
            elif tile.figureType == Figure.FigureType.King:
                char = "k"
            elif tile.figureType == Figure.FigureType.Queen:
                char = "q"
            elif tile.figureType == Figure.FigureType.Rook:
                char = "r"
            if tile.color == Tile.TileColor.White:
                char = char.upper()
            res += char
        else:
            blanks += 1
    if blanks != 0:
        res += str(blanks)
    move = "w " if turn == Tile.TileColor.White else "b "
    res += " " + move

    castles = ""
    if black_king.moves == 0:
        if board.grid[7][0].content and board.grid[7][0].content.moves == 0:
            castles += "K"
        if board.grid[0][0].content and board.grid[0][0].content.moves == 0:
            castles += "Q"
    if white_king.moves == 0:
        if board.grid[7][7].content and board.grid[7][7].content.moves == 0:
            castles += "k"
        if board.grid[0][7].content and board.grid[0][7].content.moves == 0:
            castles += "q"
    if castles == "":
        res += "-"
    else:
        res += castles
    if previous_piece and previous_piece.pawn_long_move == True:
        en_passant = f"{chr(int(previous_piece.position.x) + 97)}{8 - int(previous_piece.position.y)}"
    else:
        en_passant = "-"
    res += " " + en_passant
    res += " " + str(0)
    res += " " + str(moves_counter // 2 +1)
    return res

def ai_play():
    global white_captured, black_captured, board, previous_piece, moves_counter, is_game_over, stockfish
    
    move = stockfish.get_best_move()

    from_x = int(ord(move[0])-97)
    from_y = 8-int(move[1])
    to_x = int(ord(move[2])-97)
    to_y = 8-int(move[3])

    piece: Figure = board.grid[from_x][from_y].content
    board.grid[int(piece.position.x)][int(piece.position.y)].content = None
    piece.move(to_x, to_y, white_captured, black_captured)
    board.grid[to_x][to_y].content = piece


    if len(move) > 4:
        promo_choice = move[4]
        match promo_choice:
            case 'q':
                piece.figureType = Figure.FigureType.Queen
            case 'n':
                piece.figureType = Figure.FigureType.Knight
            case 'b':
                piece.figureType = Figure.FigureType.Bishop
            case 'r':
                piece.figureType = Figure.FigureType.Rook

    piece.is_last_move = True
    if previous_piece:
        previous_piece.is_last_move = False
    previous_piece = piece

    next_turn()
    is_game_over = game_over(board)
    moves_counter += 1

#main
if __name__ == '__main__':
    
    
    player_color = Tile.TileColor.Black

    active_piece = None
    stockfish = Stockfish(ENGINE_PATH)
    stockfish.set_depth(12)
    stockfish.set_skill_level(AI_LEVEL)
    rotated = False
    rotate_button.function = rotate_board
    game_over_button.function = play_again
    board = Board(WIDTH,HEIGHT,TILE_SIZE, pieces)
    board.grid = [[Tile(Tile.TileColor.Black, j, i, pieces) if ((i+j) % 2 == 1) else Tile(Tile.TileColor.White, j, i, pieces) for i in range(8)] for j in range(8)]
    white_captured = []
    black_captured = []
    previous_piece = None
    promotion = False
    promotedTo = None
    is_game_over = False
    turn = Tile.TileColor.White
    for piece in pieces:
        piece.set_board(board)
    initialBoard = deepcopy(board)
    initialPieces = deepcopy(pieces)
    moves_counter = 0
    tick()
    sleep(1)

    while run:

        if turn != player_color and not promotion:
            stockfish.set_fen_position(fen(board))
            ai_play()
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

            if is_game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if game_over_button.colide(event.pos):
                                game_over_button.click()
                elif event.type == pygame.QUIT:
                    run = False
            else:
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if  event.key == pygame.K_SPACE:
                        best_move = stockfish.get_best_move(fen(board))
                        print(f"The best move is: {best_move}")
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
                                    board.grid[int(active_piece.position.x)][int(active_piece.position.y)].content = None
                                    promotion = active_piece.move(x,y, white_captured, black_captured)
                                    active_piece.active = False
                                    active_piece.is_last_move = True
                                    if previous_piece:
                                        previous_piece.is_last_move = False
                                    previous_piece = active_piece
                                    board.grid[x][y].content = active_piece
                                    active_piece = None

                                    next_turn()
                                    is_game_over = game_over(board)
                                    moves_counter += 1

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

