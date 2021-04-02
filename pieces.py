class Piece:
    def __init__(self, pos, colour, board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.board = board
        self.colour = colour

    def move(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    def check_mate(self, move):
        #if self.board.check_mate(self, move) == self.colour:
        color_mate = {"White" : 1, "Black" : 2}
        if self.board.check_mate(self, move) in [color_mate[self.colour], 3]:
            return True
        return False
    
    def mate_proof(self, possible_moves):
        delete_moves = []
        for move in possible_moves:
            if self.check_mate(move):
                delete_moves.append(move)

        for move in delete_moves:
            possible_moves.remove(move)


class Pawn(Piece):
    name = "Pawn"
    def __str__(self):
        return self.name

    def __init__(self, pos, colour, board):
        super().__init__(pos, colour, board)
        self.moved = False
        self.just_moved2 = False

    def possible_moves(self, checking_mate=False):
        possible_moves = []
        colour_int = -1 if self.colour == "White" else 1
        if not (self.colour == "White" and self.y == 7) and not (self.colour == "Black" and self.y == 0) and self.board.board[self.x][self.y + (1 * colour_int)] == 0:
            possible_moves.append([self.x, self.y + (1 * colour_int)])
            if not self.moved and 0 <= self.y + (2 * colour_int) <= 7 and self.board.board[self.x][self.y + (2 * colour_int)] == 0:
                possible_moves.append([self.x, self.y + (2 * colour_int)])


        if self.y != 7 and self.y != 0:
            for c in [-1, 1]:
                if 0 <= self.x + c <= 7 and self.board.board[self.x + c][self.y + (1* colour_int)] != 0:
                    eat = self.board.board[self.x + c][self.y + (1 * colour_int)]
                    if eat.colour != self.colour:
                        possible_moves.append([self.x + c, self.y + (1 * colour_int)])

        
        for i in [-1, 1]:
            colour_int = -1 if self.colour == "White" else 1
            if 0 <= self.x + i <= 7 and 0 <= self.y + colour_int <= 7:
                adjacent_piece = self.board.board[self.x + i][self.y]
                if adjacent_piece and adjacent_piece.colour != self.colour and adjacent_piece.name == "Pawn" and adjacent_piece.just_moved2:
                    print("pitodeleche")
                    possible_moves.append([self.x + i, self.y + colour_int, adjacent_piece])


        if not checking_mate:
            self.mate_proof(possible_moves)

        return possible_moves
        


class Knight(Piece):
    name = "Knight"
    def __str__(self):
        return self.name

    def possible_moves(self, checking_mate=False):
        possible_moves = []
        for c in [2, -2 ,1 ,-1]:
            for m in [-1, 1]:
                new_pos = [self.x + c, self.y + (m * (3 - abs(c)))]
                if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                    if self.board.board[new_pos[0]][new_pos[1]] == 0:
                        possible_moves.append(new_pos)

                    else:
                        if self.board.board[new_pos[0]][new_pos[1]].colour != self.colour:
                            possible_moves.append(new_pos)

        if not checking_mate:
            self.mate_proof(possible_moves)

        return possible_moves


class Bishop(Piece):
    name = "Bishop"
    def __str__(self):
        return self.name


    def possible_moves(self, checking_mate=False):
        possible_moves = []

        for i in [-1, 1]:
            for j in [-1, 1]:
                n = 0
                stop = False
                while not stop:
                    n += 1
                    if 0 <= self.x + (n * i) <= 7 and 0 <= self.y + (n * j) <= 7:
                        new_pos = [self.x + (n * i), self.y + (n * j)]
                        if self.board.board[new_pos[0]][new_pos[1]] == 0:
                            possible_moves.append(new_pos)

                        else:
                            if self.board.board[new_pos[0]][new_pos[1]].colour != self.colour:
                                possible_moves.append(new_pos)
                            stop = True

                    else:
                        stop = True

        if not checking_mate:
            self.mate_proof(possible_moves)

        return possible_moves
                    


class Rook(Piece):
    name = "Rook"
    
    def __init__(self, pos, colour, board):
        super().__init__(pos, colour, board)
        self.moved = False
    
    def __str__(self):
        return self.name

    def possible_moves(self, checking_mate=False):
        possible_moves = []

        for i in [-1, 1, 2, -2]:
            if abs(i) > 1:
                j = i // 2
                i = 0
            else:
                j = 0
            n = 0
            stop = False
            while not stop:
                n += 1
                if 0 <= self.x + (n * i) <= 7 and 0 <= self.y + (n * j) <= 7:
                    new_pos = [self.x + (n * i), self.y + (n * j)]
                    if self.board.board[new_pos[0]][new_pos[1]] == 0:
                        possible_moves.append(new_pos)

                    else:
                        if self.board.board[new_pos[0]][new_pos[1]].colour != self.colour:
                            possible_moves.append(new_pos)
                        stop = True

                else:
                    stop = True

        if not checking_mate:
            self.mate_proof(possible_moves)

        return possible_moves
                    


class Queen(Piece):
    name = "Queen"
    def __str__(self):
        return self.name

    def possible_moves(self, checking_mate=False):
        possible_moves = []
        
        for i in [-1, 1, 0]:
            for j in [-1, 1, 0]:
                n = 0
                stop = False
                while not stop:
                    n += 1
                    if 0 <= self.x + (n * i) <= 7 and 0 <= self.y + (n * j) <= 7:
                        new_pos = [self.x + (n * i), self.y + (n * j)]
                        if self.board.board[new_pos[0]][new_pos[1]] == 0:
                            possible_moves.append(new_pos)

                        else:
                            if self.board.board[new_pos[0]][new_pos[1]].colour != self.colour:
                                possible_moves.append(new_pos)
                            stop = True

                    else:
                        stop = True

        if not checking_mate:
            self.mate_proof(possible_moves)

        return possible_moves

class King(Piece):
    name = "King"

    def __init__(self, pos, colour, board):
        super().__init__(pos, colour, board)
        self.moved = False
    
    def __str__(self):
        return self.name

    def possible_moves(self, checking_mate=False):
        possible_moves = []

        for i in [-1, 1, 0]:
            for j in [-1, 1, 0]:
                if 0 <= self.x + i <= 7 and 0 <= self.y + j <= 7 and (self.board.board[self.x + i][self.y + j] == 0 or self.board.board[self.x + i][self.y + j].colour != self.colour):
                    possible_moves.append([self.x + i, self.y + j])

        if not checking_mate:
            self.mate_proof(possible_moves)
        
            if not self.moved:
                for i in [-1, 1]:
                    valid = True
                    c = 1
                    new_x = self.x + (i * c)
                    rook = 0
                    while 0 <= new_x <= 7 and valid:
                        if self.board.board[new_x][self.y] != 0:
                            if self.board.board[new_x][self.y].name != "Rook":
                                valid = False

                            elif self.board.board[new_x][self.y].moved:
                                valid = False

                            else:
                                rook = self.board.board[new_x][self.y]

                        c += 1
                        new_x = self.x + (i * c)

                    if valid:
                        moving_king = []
                        if i == 1:
                            for l in range(5,7):
                                moving_king.append([l,self.y])

                        else:
                            for l in range(1, 3):
                                moving_king.append([self.x - l,self.y])
                            
                        len_before = len(moving_king)
                        self.mate_proof(moving_king)
                        if len_before == len(moving_king):
                            new_pos = moving_king[-1]
                            new_pos.append(rook)
                            possible_moves.append(new_pos)
                            

        return possible_moves

FEN_PIECES = {
    "p" : Pawn,
    "n" : Knight,
    "b" : Bishop,
    "r" : Rook,
    "q" : Queen,
    "k" : King
}

