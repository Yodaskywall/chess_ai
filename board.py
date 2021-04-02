from pieces import *
from copy import deepcopy

pieces = {
    "p" : "Pawn",
    "n" : "Knight",
    "b" : "Bishop",
    "r" : "Rook",
    "k" : "King",
    "q" : "Queen"
}

class Board:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        self.board = []
        self.pieces = []
        self.player = "White"
        self.winner = None
        for i in range(8):
            self.board.append([])
            for j in range(8):
                self.board[i].append(0)

        for n, row in enumerate(fen.split("/")):
            c = 0
            for char in row:
                if char in range(1,9):
                    c += int(char)

                elif char.lower() in FEN_PIECES:
                    if char == char.upper():
                        colour = "White"

                    else:
                        colour = "Black"

                    piece = FEN_PIECES[char.lower()]([c,n], colour, self)
                    self.board[c][n] = piece
                    self.pieces.append(piece)
                    c += 1

    def move(self, piece, pos, checking_mate=False):
        if len(pos) == 3 and pos[2].name == "Rook":
            if pos[2].x > 4:
                self.move(pos[2], [5, piece.y])
                pos = [6, piece.y]

            else:
                self.move(pos[2], [3, piece.y])
                pos = [2, piece.y]

        elif len(pos) == 3 and pos[2].name == "Pawn":
            #self.pieces.remove(pos[2])
            self.pieces.remove(self.board[pos[2].x][pos[2].y])
            self.board[pos[2].x][pos[2].y] = 0
            pos = pos[:2]

        elif piece.name == "Pawn":
            if piece.just_moved2:
                piece.just_moved2 = False

            if abs(piece.y - pos[1]) == 2:
                piece.just_moved2 = True


        self.board[piece.x][piece.y] = 0
        if self.board[pos[0]][pos[1]] != 0:
            self.pieces.remove(self.board[pos[0]][pos[1]])
        self.board[pos[0]][pos[1]] = piece
        piece.move(pos)

        if piece.name in ["Pawn", "King", "Rook"]:
            piece.moved = True

        if self.player == "White":
            self.player = "Black"

        else:
            self.player = "White"

        for p in self.pieces:
            if p.name == "Pawn" and p.just_moved2 and p.x != piece.x or p.y != piece.y:
                p.just_moved2 = False

        # CHECK finish

        lost = True

        if not checking_mate:
            for piece in self.pieces:
                if piece.colour == self.player:
                    if len(piece.possible_moves()) > 0:
                        lost = False

        if lost:
            if not checking_mate and not self.in_mate():
                self.winner = "Draw"

            elif self.player == "Black":
                self.winner = "White"
            else:
                self.winner = "Black"


    def check_mate(self, piece, move):
        new_board = deepcopy(self)
        for p in new_board.pieces:
            if p.pos == piece.pos:
                new_piece = p
        new_board.move(new_piece, move, True)
        opposite_king = {}
        for p in new_board.pieces:
            if p.name == "King":
                if p.colour == "White":
                    opposite_king["Black"] = p.pos
                else:
                    opposite_king["White"] = p.pos


        mate = 0

        for p in new_board.pieces:
            if opposite_king[p.colour] in p.possible_moves(True):
                if p.colour == "White":
                    if mate == 0:
                        mate = 2

                    else:
                        mate = 3
                    #return "Black"
                else:
                    if mate == 0:
                        mate = 1
                    else:
                        mate = 3
                    #return "White"


        new_board = 0
        return mate

    def in_mate(self):
        for p in self.pieces:
            if p.name == "King" and p.colour == self.player:
                return p.check_mate([p.x, p.y])



def print_board(board):
    for row in board.board:
        for c in row:
            print(c, end=" ")
        print("\n")

board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
