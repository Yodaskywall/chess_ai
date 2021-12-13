import numpy as np
from game_parser import parse
from board import Board, pieces, alphabet


def board_to_array(board=Board()):
    # Will convert a board to an 385 array
    # 0th value is player to move
    # Then 6 neurons representing each piece for each square
    # 1 means there is a white piece
    # -1 means there is a black piece
    # 0 means no piece

    
    piece_to_num = {"Pawn" : 0, "Knight" : 1, "Bishop" : 2,
            "Rook" : 3, "Queen" : 4, "King": 5}


    array = [0] * 385
    if board.player == "White":
        array[0] = 1 

    else:
        array[0] = -1

    for piece in board.pieces:
        pos = piece.x * 48 + piece.y * 6 + piece_to_num[piece.name] + 1
        if piece.colour == "White":
            array[pos] = 1

        else:
            array[pos] = -1

    return array



def movepair_to_1darray(pair):
    array = [0] * 4096
    index = pair[1][1] * 512 + pair[1][0] * 64 + pair[0][1] * 8 + pair[0][0]
    array[index] = 1
    return array


def index_to_movepair(index):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    while index > 0:
        if index >= 512:
            index -= 512
            y2 += 1

        elif index >= 64:
            index -= 64
            x2 += 1

        elif index >= 8:
            index -=8 
            y1 += 1

        else:
            index -= 1
            x1 += 1


    return [[x1,y1], [x2,y2]]


def prepare_data(filename):
    raw_moves = parse(filename)
    board = Board()
    moves = []


    c = 0
    player = "w"
    boards = []
    for move in raw_moves:
        c+=1
        boards.append(board_to_array(board))
        print(f"Move: {c}")
        print(move)
        if player == "White":
            player = "Black"

        else:
            player = "White"
        
        # X means capture, the program handles if there is a capture or not on its own
        move = move.replace("cx", "")
        move = move.replace("x", "")
        move = move.replace("+", "")

        if move == "O-O-O":
            #Queenside castle
            if player == "White":
                king = board.board[4][7]
                rook = board.board[0][7]
                piece_pos = king.pos
                board.move(king, [2, 7, rook])
                pos = [2,7] 

            else:
                king = board.board[4][0]
                rook = board.board[0][0]
                piece_pos = king.pos
                board.move(king, [2, 0, rook])
                pos = [2,0]
                

        elif move == "O-O":
            #Kingside castle
            if player == "White":
                king = board.board[4][7]
                rook = board.board[7][7]
                piece_pos = king.pos
                board.move(king, [6, 7, rook])
                pos = [6,7]

            else:
                king = board.board[4][0]
                rook = board.board[7][0]
                piece_pos = king.pos
                board.move(king, [6, 0, rook])
                pos = [6,0]

            
        elif len(move) == 3 or len(move) == 2 or len(move) == 4:
            # I know its bad practice but Im lazy
            # moving_y is a flag, moving_x is the coordinate
            # if moving_y is false, moving_x is the x coordinate
            # if moving_y is true, moving_x is the y coordinate
            moving_x = None
            moving_y = False

            if len(move) == 4:
                is_int = False
                piece_name = pieces[move[0].lower()]
                try:
                    num = int(move[1])
                    is_int = True
                except Exception as e:
                    print(e)
                    print("***********************************************************************************************************************")
                if is_int:
                    moving_x = 8 - num
                    moving_y = True
                else:
                    moving_x = alphabet.index(move[1])
                x = alphabet.index(move[2])
                y = 8 - int(move[3])

            elif len(move) == 3:
                if move[0].upper() == move[0]:
                    piece_name = pieces[move[0].lower()]
                else:
                    moving_x = alphabet.index(move[0])
                    piece_name = "Pawn"
                x = alphabet.index(move[1])
                y = 8 - int(move[2])

            else:
                piece_name = "Pawn"
                x = alphabet.index(move[0])
                y = 8 - int(move[1])

            found = False
            moving_piece = None
            for piece in board.pieces:
                if piece.colour == player and piece.name == piece_name and ((moving_x is None) or (piece.x == moving_x and not moving_y) or (piece.y == moving_x and moving_y)):
                    for poss_move in piece.possible_moves():
                        if poss_move[0] == x and poss_move[1] == y:
                            if not (moving_piece is None):
                                print("TROLIADO PUTO")
                            moving_piece = piece



            if moving_piece is None:
                print("CAGADAAAAAA")
                pos = None

            else:
                piece_pos = moving_piece.pos
                board.move(moving_piece, [x,y])
                pos = [x,y]

        else:
            pos = None
            moving_piece = None
            print("QU EAPSPASDASJKLDSKN")
            print(move)

        if moving_piece is not None and pos is not None:
            moves.append([piece_pos, pos])
    print(moves)


    return moves, boards


def get_XY(moves, boards):
    X = []
    Y = []
    for move in moves:
       Y.append(np.array(movepair_to_1darray(move)))

    for board in boards:
        X.append(np.array(board))

    X = np.array(X)
    Y = np.array(Y)

    return X, Y



if __name__ == "__main__":
    moves, boards = prepare_data("stored_games/102game.pgn")
    X, Y = get_XY(moves,boards)
    print("X: ")
    print(X)
    print(type(X))
    print(X.shape)
    print("Y: ")
    print(Y)
    print(type(Y))
    print(Y.shape)
