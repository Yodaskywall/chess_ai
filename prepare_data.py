from game_parser import parse
from board import Board, pieces, alphabet



def prepare_data(filename):
    raw_moves = parse(filename)
    board = Board()
    moves = []


    c = 0
    player = "w"
    for move in raw_moves:
        c+=1
        print(f"Move: {c}")
        if player == "White":
            player = "Black"

        else:
            player = "White"
        
        # X means capture, the program handles if there is a capture or not on its own
        move = move.replace("cx", "")
        move = move.replace("x", "")

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

            
        elif len(move) == 3 or len(move) == 2:
            moving_x = None
            if len(move) == 3:
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
                if piece.colour == player and piece.name == piece_name and (moving_x is None or piece.x == moving_x):
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


    return moves



if __name__ == "__main__":
    prepare_data("sample_game.pgn")
            
