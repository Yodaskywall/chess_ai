from game_parser import parse
from board import Board, pieces, alphabet



def prepare_data(filename):
    moves = parse(filename)
    print(moves)
    board = Board()

    c = 0
    player = "w"
    for move in moves:
        c+=1
        print(f"Move: {c}")
        if player == "White":
            player = "Black"

        else:
            player = "White"


        if move == "O-O":
            print("Castle")

        elif move == "O-O-O":
            print("Castle xd")
            
        elif len(move) == 3 or len(move) == 2:
            if len(move) == 3:
                piece_name = pieces[move[0].lower()]
                x = alphabet.index(move[1])
                y = 8 - int(move[2])

            else:
                piece_name = "Pawn"
                x = alphabet.index(move[0])
                y = 8 - int(move[1])

            found = False
            moving_piece = None
            for piece in board.pieces:
                if piece.colour == player and piece.name == piece_name:
                    for poss_move in piece.possible_moves():
                        if poss_move[0] == x and poss_move[1] == y:
                            if not (moving_piece is None):
                                print("TROLIADO PUTO")
                            moving_piece = piece


            if moving_piece is None:
                print("CAGADAAAAAA")

            else:
                board.move(moving_piece, [x,y])



if __name__ == "__main__":
    prepare_data("sample_game.pgn")
            
