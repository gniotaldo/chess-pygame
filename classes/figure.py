from pygame.math import Vector2
from classes.board import Tile
from enum import Enum
from misc.images import *
from misc.sounds import *


image_dict = {
    Tile.TileColor.White: {
        'Rook': white_rook_img,
        'Bishop': white_bishop_img,
        'Knight': white_knight_img,
        'King': white_king_img,
        'Queen': white_queen_img,
        'Pawn': white_pawn_img
    },
    Tile.TileColor.Black: {
        'Rook': black_rook_img,
        'Bishop': black_bishop_img,
        'Knight': black_knight_img,
        'King': black_king_img,
        'Queen': black_queen_img,
        'Pawn': black_pawn_img
    }
}


class Figure:

    class FigureType(Enum):
        Rook = 'Rook'
        Bishop = 'Bishop'
        Knight = 'Knight'
        King = 'King'
        Queen = 'Queen'
        Pawn = 'Pawn'



    def __init__(self, figureType, color, position) -> None:
        self.figureType: Figure.FigureType = figureType
        self.color: Tile.TileColor = color
        self.position: Vector2 = position
        self.hovered = False
        self.active = False
        self.activeAnimation = False
        self.activeTicks = 0
        self.availableMoves = []
        self.tile = None
        self.legal_moves = []
        self.board = None
        self.moves = 0
        self.is_last_move = False
        self.pawn_long_move = False

    def set_board(self, board):
        self.board = board

    def availible_for_pawn(self, moves, previous_piece):

        legal_moves = []
        blocked_column = False
        for x, y in moves:
            x = int(x)
            y = int(y)
            if x not in range(8) or y not in range (8):
                continue
            piece_in_xy: Figure = self.board.grid[x][y].content
            if piece_in_xy == None:
                if (int(self.position.x) == x):
                    if not blocked_column:
                        legal_moves.append(Vector2(x,y))
                    else:
                        continue
                else:
                    piece: Figure = self.board.grid[x][y+1].content
                    if self.color == Tile.TileColor.White and piece and piece == previous_piece and piece.figureType == self.FigureType.Pawn and piece.pawn_long_move:
                        legal_moves.append(Vector2(x,y))
                    piece: Figure = self.board.grid[x][y-1]
                    if self.color == Tile.TileColor.Black and  piece and piece == previous_piece and piece.figureType == self.FigureType.Pawn and piece.pawn_long_move:
                        legal_moves.append(Vector2(x,y))

                    else:
                        continue
            elif not(Tile.TileColor.equal(piece_in_xy.color, self.color)):
                if(int(self.position.x) == x):
                    blocked_column = True
                    continue
                legal_moves.append(Vector2(x,y))
            else:
                continue
        return legal_moves

    def get_legal_moves(self, previous_piece):
        match self.figureType:
            case self.FigureType.Pawn:
                if self.color == Tile.TileColor.Black:
                    moves = [(self.position.x, self.position.y + 1),            #move forward
                             (self.position.x + 1, self.position.y + 1), (self.position.x - 1, self.position.y + 1)]    #move diagonally (capture)
                    if not self.moves:
                        moves.append((self.position.x, self.position.y + 2))
                else:
                    moves = [(self.position.x, self.position.y - 1),
                             (self.position.x + 1, self.position.y - 1), (self.position.x - 1, self.position.y - 1)]
                    if not self.moves:
                        moves.append((self.position.x, self.position.y - 2))
                
                self.legal_moves = self.availible_for_pawn(moves, previous_piece)
            case _:
                self.legal_moves = [Vector2(4,4)]


    def move(self, x, y, white_captured, black_captured):
        old_x = int(self.position.x)
        old_y = int(self.position.y)
        print(f"moves from : {chr(old_x + 97)}{8 - old_y} to {chr(x + 97)}{8 - y}")

        if self.board.grid[x][y].content:
            self.capture(x, y, white_captured, black_captured)
            capture_sound.play()
        elif self.color == Tile.TileColor.White and self.board.grid[x][y+1].content and int(self.position.x) != x:
            self.capture(x, y+1, white_captured, black_captured)
            capture_sound.play()
        elif self.color == Tile.TileColor.Black and self.board.grid[x][y-1].content and int(self.position.x) != x:
            self.capture(x, y-1, white_captured, black_captured)
            capture_sound.play()
        move_sound.play()
        self.board.grid[old_x][old_y].content = None
        self.board.grid[x][y].content = self
        self.position.x = x
        self.position.y = y
        if abs(y-old_y) > 1 and self.figureType == self.FigureType.Pawn:
            self.pawn_long_move = True
        else:
            self.pawn_long_move = False

        self.moves += 1


    def capture(self, x, y,  white_captured: list[any], black_captured: list[any]):
        captured_tile: Tile = self.board.grid[x][y]
        if captured_tile.color == Tile.TileColor.Black:
            black_captured.append(captured_tile.content.figureType.name)
        else:
            white_captured.append(captured_tile.content.figureType.name)
        captured_tile.content.position = Vector2(8,8)
        captured_tile.content = None


    def render(self, screen, size, rotated, previous_piece=None):
        
        
        x,y = pygame.mouse.get_pos()
        x = int(x/TILE_SIZE)
        y = int(y/TILE_SIZE)
        if self.position == Vector2(x,y):
            self.hovered = True
        else:
            self.hovered = False
        if rotated:
            x = 7-x
            y = 7-y
        if rotated:
            screen.blit(
                image_dict[self.color][self.figureType.value],
                ((7-self.position.x)  * size, (7-self.position.y) * size)
            )
        else: 
            screen.blit(
                image_dict[self.color][self.figureType.value],
                (self.position.x  * size, self.position.y * size)
            )
        if self.active:


            surface = pygame.Surface((size, size))
            surface.set_alpha(60) 
            surface.fill('yellow')
            if rotated:
                screen.blit(surface, ((7-self.position.x)*size, (7-self.position.y)*size))
            else:
                screen.blit(surface, (self.position.x*size, self.position.y*size))
            self.get_legal_moves(previous_piece)
            for move in self.legal_moves:
                if rotated:
                    screen.blit(legal_move_img, ((7-move.x)*size, (7-move.y)*size))
                else:
                    screen.blit(legal_move_img, (move.x*size, move.y*size))


            if self.activeAnimation:
                surface = pygame.Surface((size, size))
                surface.set_alpha(60) 
                surface.fill('white')
                if rotated:
                    screen.blit(surface, ((7-self.position.x)*size, (7-self.position.y)*size))
                else:
                    screen.blit(surface, (self.position.x*size, self.position.y*size))
                self.activeTicks += 1
                if self.activeTicks > 10:
                    self.activeAnimation = False
                    self.activeTicks = 0
        elif self.hovered:
            surface = pygame.Surface((size, size))
            surface.set_alpha(30) 
            surface.fill((255, 255, 255))
            screen.blit(surface, (self.position.x*size, self.position.y*size))





#init figures
#white
white_rook1 = Figure(Figure.FigureType.Rook, Tile.TileColor.White, Vector2(0,7))
white_rook2 = Figure(Figure.FigureType.Rook, Tile.TileColor.White, Vector2(7,7))

white_bishop1 = Figure(Figure.FigureType.Bishop, Tile.TileColor.White, Vector2(1,7))
white_bishop2 = Figure(Figure.FigureType.Bishop, Tile.TileColor.White, Vector2(6,7))

white_knight1 = Figure(Figure.FigureType.Knight, Tile.TileColor.White, Vector2(2,7))
white_knight2 = Figure(Figure.FigureType.Knight, Tile.TileColor.White, Vector2(5,7))

white_queen = Figure(Figure.FigureType.Queen, Tile.TileColor.White, Vector2(3,7))
white_king = Figure(Figure.FigureType.King, Tile.TileColor.White, Vector2(4,7))

white_pawn1 = Figure(Figure.FigureType.Pawn, Tile.TileColor.White, Vector2(0,6))
white_pawn2 = Figure(Figure.FigureType.Pawn, Tile.TileColor.White, Vector2(1,6))
white_pawn3 = Figure(Figure.FigureType.Pawn, Tile.TileColor.White, Vector2(2,6))
white_pawn4 = Figure(Figure.FigureType.Pawn, Tile.TileColor.White, Vector2(3,6))
white_pawn5 = Figure(Figure.FigureType.Pawn, Tile.TileColor.White, Vector2(4,6))
white_pawn6 = Figure(Figure.FigureType.Pawn, Tile.TileColor.White, Vector2(5,6))
white_pawn7 = Figure(Figure.FigureType.Pawn, Tile.TileColor.White, Vector2(6,6))
white_pawn8 = Figure(Figure.FigureType.Pawn, Tile.TileColor.White, Vector2(7,6))


white_pieces = [
    white_rook1, white_rook2,
    white_bishop1, white_bishop2,
    white_knight1, white_knight2,
    white_king, white_queen,
    white_pawn1, white_pawn2, white_pawn3, white_pawn4,
    white_pawn5, white_pawn6, white_pawn7, white_pawn8
]

#black
black_rook1 = Figure(Figure.FigureType.Rook, Tile.TileColor.Black, Vector2(0,0))
black_rook2 = Figure(Figure.FigureType.Rook, Tile.TileColor.Black, Vector2(7,0))

black_bishop1 = Figure(Figure.FigureType.Bishop, Tile.TileColor.Black, Vector2(1,0))
black_bishop2 = Figure(Figure.FigureType.Bishop, Tile.TileColor.Black, Vector2(6,0))

black_knight1 = Figure(Figure.FigureType.Knight, Tile.TileColor.Black, Vector2(2,0))
black_knight2 = Figure(Figure.FigureType.Knight, Tile.TileColor.Black, Vector2(5,0))

black_queen = Figure(Figure.FigureType.Queen, Tile.TileColor.Black, Vector2(3,0))
black_king = Figure(Figure.FigureType.King, Tile.TileColor.Black, Vector2(4,0))

black_pawn1 = Figure(Figure.FigureType.Pawn, Tile.TileColor.Black, Vector2(0,1))
black_pawn2 = Figure(Figure.FigureType.Pawn, Tile.TileColor.Black, Vector2(1,1))
black_pawn3 = Figure(Figure.FigureType.Pawn, Tile.TileColor.Black, Vector2(2,1))
black_pawn4 = Figure(Figure.FigureType.Pawn, Tile.TileColor.Black, Vector2(3,1))
black_pawn5 = Figure(Figure.FigureType.Pawn, Tile.TileColor.Black, Vector2(4,1))
black_pawn6 = Figure(Figure.FigureType.Pawn, Tile.TileColor.Black, Vector2(5,1))
black_pawn7 = Figure(Figure.FigureType.Pawn, Tile.TileColor.Black, Vector2(6,1))
black_pawn8 = Figure(Figure.FigureType.Pawn, Tile.TileColor.Black, Vector2(7,1))

black_pieces = [
    black_rook1, black_rook2,
    black_bishop1, black_bishop2,
    black_knight1, black_knight2,
    black_king, black_queen,
    black_pawn1, black_pawn2, black_pawn3, black_pawn4,
    black_pawn5, black_pawn6, black_pawn7, black_pawn8
]

pieces = white_pieces + black_pieces