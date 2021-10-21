from pieces import *
from copy import deepcopy
import pickle
import time
import string

alphabet = string.ascii_lowercase

pieces = {
    "p" : "Pawn",
    "n" : "Knight",
    "b" : "Bishop",
    "r" : "Rook",
    "k" : "King",
    "q" : "Queen"
}

piece_value = {
    "Pawn" : 10,
    "Knight" : 30,
    "Bishop" : 30,
    "Rook" : 50,
    "Queen" : 90,
    "King" : 900
}

class Stack:
    def __init__(self):
        self.stack = []

    def add(self, x):
        self.stack.append(x)

    def pop(self):
        if len(self.stack) == 0:
            return None
        x = self.stack[-1]
        del self.stack[-1]
        return x

    def peek(self):
        if len(self.stack) != 0:
            return self.stack[-1]

    def length(self):
        return len(self.stack)

class Board:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"):
        self.board = []
        self.pieces = []
        self.player = "White"
        self.winner = None
        self.saved_state = Stack()
        for i in range(8):
            self.board.append([])
            for j in range(8):
                self.board[i].append(0)

        self.fen = fen
        self.load_fen()

    def load_fen(self):
        fen = self.fen.split(" ")

        self.pieces = []

        self.board = []
        for i in range(8):
            self.board.append([])
            for j in range(8):
self.board[i].append(0)

        for n, row in enumerate(fen[0].split("/")):
            c = 0
            for char in row:
                if char in [str(x) for x in range(1,9)]:
                    c += int(char)

                elif char.lower() in FEN_PIECES:
                    if char == char.upper():
                        colour = "White"

                    else:
                        colour = "Black"

                    piece = FEN_PIECES[char.lower()]([c,n], colour, self)
                    if piece.name == "Pawn":
                        if (piece.colour == "Black" and piece.y) == 1 or (piece.colour == "White" and piece.y == 6):
                            piece.moved = False
                        else:
                            piece.moved = True
                    self.board[c][n] = piece
                    self.pieces.append(piece)
                    c += 1

        if fen[1] == "w":
            self.player = "White"

        else:
            self.player = "Black"

        if fen[2] == "-":
            for piece in self.pieces:
                if piece.name == "Rook":
                    rook.moved = True


        if not self.winner is None:
            self.winner = None

        elif len(fen[2]) != 4:
            for char in fen[2]:
                if char == "K":
                    self.board[7][7].moved = False

                elif char == "Q":
                    self.board[0][7].moved = False

                elif char == "k":
                    self.board[7][0].moved = False

                elif char == "q":
                    self.board[0][0].moved = False

        if fen[3] != "-":
            for pos in fen[3].split(","):
                x = alphabet.index(pos[0])
                y = int(pos[1])
                if y == 3:
                    y = 4

                elif y == 6:
                    y = 5

                elif y == 7:
                    y = 6

                elif y == 2:
                    y = 3

                y = 8 - y
                print(self.fen)
                print(x,y)
                self.board[x][y].just_moved2 = True


    def get_fen(self):
        piece_info = ""
        for row in range(8):
            empty = 0
            for col in range(8):
                piece = self.board[col][row]
                if piece == 0:
                    empty += 1

                else:
                    if empty != 0:
                        piece_info += str(empty)
                        empty = 0

                    letter = PIECES_FEN[piece.name]
                    if piece.colour == "White":
                        letter = letter.upper()

                    piece_info += letter
            if empty != 0:
                piece_info += str(empty)
            piece_info += "/"
            empty = 0
        piece_info = piece_info[:-1]


        moving = "w" if self.player == "White" else "b"

        castling = []

        for piece in self.pieces:
            if piece.name == "Rook" and not piece.moved:
                letter = 0
                if piece.x == 7:
                    letter = "k"
                else:
                    letter = "q"
                if piece.colour == "White":
                    letter = letter.upper()

                castling.append(letter)

        for piece in self.pieces:
            if piece.name == "King" and piece.moved:
                if piece.colour == "White":
                    for char in castling:
                        if char == char.upper():
                            castling.remove(char)

                else:
                    for char in castling:
                        if char == char.lower():
                            castling.remove(char)

        castling = "".join(castling)

        en_passant = "-"
        c = 0
        for piece in self.pieces:
            if piece.name == "Pawn":
                if piece.just_moved2:
                    c += 1
                    standard_x = alphabet[piece.x]
                    print("xd")
                    print(piece.y)
                    standard_y = 8 - piece.y
                    
                    if standard_y == 4:
                        standard_y = 3

                    elif standard_y == 3:
                        standard_y = 2

                    elif standard_y == 5:
                        standard_y = 6

                    elif standard_y == 6:
                        standard_y = 7

                    print(standard_y)

                    if c == 1:
                        en_passant = standard_x + str(standard_y) + ","

                    else:
                        en_passant += standard_x + str(standard_y) + ","

        if len(en_passant) > 1:
            en_passant = en_passant[:-1]

        fen = piece_info + " " + moving + " " + castling + " " + en_passant
        return fen 

    def save_state(self):
        self.saved_state.add(self.get_fen())

    def load_state(self):
        to_load = self.saved_state.pop()
        self.fen = to_load
        self.load_fen()
        #self.__dict__.update(Board(self.saved_state).__dict__)

    def get_move_info(self, piece, pos):

        move_info = {"moving" : deepcopy(piece), "eating" : None, "enrocando" : None, "moved_to" : None} 
        
        #Enroque
        if len(pos) == 3 and pos[2].name == "Rook":
            if pos[2].x > 4:
                move_info["enrocando"] = [deepcopy(pos[2]), [5, piece.y]]
                move_info["moved_to"] = [6, piece.y]

            else:
                move_info["enrocando"] = [deepcopy(pos[2]), [3, piece.y]]
                move_info["moved_to"] = [2, piece.y]


        elif len(pos) == 3 and pos[2].name == "Pawn":
            move_info["eating"] = deepcopy(pos[2])
            move_info["moved_to"] = pos[:2]

        else:
            if self.board[pos[0]][pos[1]] != 0:
                move_info["eating"] = deepcopy(self.board[pos[0]][pos[1]])

            move_info["moved_to"] = pos

        return move_info
# 
#     def remove_piece(self, pos):
#         piece = self.board[pos[0]][pos[1]]
#         print(f"removing from pos: {pos}")
#         if piece == 0:
#             print("LA ESTÁS LIANDO MUCHOO**************************************************")
#         if piece in self.pieces:
#             self.pieces.remove(piece)
#         self.board[pos[0]][pos[1]] = 0
# 
#     def add_piece(self, piece):
#         print(f"adding piece {piece.name} {piece.pos}")
#         self.pieces.append(piece)
#         self.board[piece.x][piece.y] = piece
#         piece.board.__dict__.update(self.__dict__)
# 
#     def unmove(self, move_info):
#         if not (move_info["enrocando"] is None):
#             self.remove_piece(move_info["enrocando"][1])
#             self.remove_piece(move_info["moved_to"])
#             self.add_piece(move_info["enrocando"][0])
#             self.add_piece(move_info["moving"])
# 
#         else:
#             self.remove_piece(move_info["moved_to"])
#             self.add_piece(move_info["moving"])
#             if not (move_info["eating"] is None):
#                 self.add_piece(move_info["eating"])
# 
#         if not (self.winner is None):
#             self.winner = None
# 
#         if self.player == "Black":
#             self.player = "White"
# 
#         else:
#             self.player = "Black"
# 
# 
    def move(self, piece, pos, checking_mate=False, enrocando=False):
        if len(pos) == 3 and pos[2].name == "Rook":
            if pos[2].x > 4:
                self.move(pos[2], [5, piece.y], enrocando=True)
                pos = [6, piece.y]

            else:
                self.move(pos[2], [3, piece.y], enrocando=True)
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
            if self.board[pos[0]][pos[1]].name == "Queen" and not checking_mate:
                print("CHUPA MI MUÑEÑO")
        self.board[pos[0]][pos[1]] = piece
        piece.move(pos)

        if piece.name in ["Pawn", "King", "Rook"]:
            piece.moved = True

        # Pawn to Queen
        if piece.name == "Pawn":
            if piece.colour == "White" and piece.y == 0:
                new_piece = Queen(piece.pos, piece.colour, self)
                self.board[piece.x][piece.y] = new_piece
                self.pieces.remove(piece)
                self.pieces.append(new_piece)

            elif piece.colour == "Black" and piece.y == 7:
                new_piece = Queen(piece.pos, piece.colour, self)
                self.board[piece.x][piece.y] = new_piece
                self.pieces.remove(piece)
                self.pieces.append(new_piece)
                

        if self.player == "White" and not enrocando:
            self.player = "Black"

        elif not enrocando:
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
        ini = time.time()
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
    
    def check_maate(self, piece, move):
        ini = time.time()
        self.save_state()
        self.move(piece, move, True)
        opposite_king = {}
        for p in self.pieces:
            if p.name == "King":
                if p.colour == "White":
                    opposite_king["Black"] = p.pos
                else:
                    opposite_king["White"] = p.pos


        mate = 0

        for p in self.pieces:
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


        self.load_state()
        print(f"mate runtime: {time.time()-ini}")
        return mate

    
    def in_mate(self):
        for p in self.pieces:
            if p.name == "King" and p.colour == self.player:
                return p.check_mate([p.x, p.y])


    def evaluate(self):
        value = 0
        for piece in self.pieces:
            if piece.colour == "White":
                value += piece_value[piece.name]

            else:
                value -= piece_value[piece.name]

        return value



def print_board(board):
    for row in board.board:
        for c in row:
            print(c, end=" ")
        print("\n")
board = Board()
