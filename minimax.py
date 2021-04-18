from board import *
from copy import deepcopy
import time

c = 0

def minimax(board, depth, alpha, beta, maximizing, initial=True):
    global c
    c += 1
    if depth == 0 or not (board.winner is None):
        print("RETURNING")
        if board.winner == "Draw":
            return 0

        elif board.winner == "White":
            return 9999

        elif board.winner == "Black":
            return -9999


        return board.evaluate()

    if maximizing:
        print(f"depth: {depth}")
        max_eval = -10000
        possible_moves = []
        if initial:
            best_move = 0
        
        for piece in board.pieces:
            if piece.colour == "White":
                for pos in piece.possible_moves():
                    possible_moves.append([piece, pos])

        count = 0
        for piece in board.pieces:
            if piece.colour == "White":
                for move in piece.possible_moves():
                    if initial:
                        count += 1
                        print(f"pito: {count}")
                    #new_board = deepcopy(board)
                    #new_piece = board.board[move[0].x][move[0].y]

                    move_info = board.get_move_info(piece, move)
                    board.move(piece, move)
                    
                    evaluation = minimax(board, depth - 1, alpha, beta, False, False)
                    
                    board.unmove(move_info)
                    print("UNMOVINGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG")

                    if evaluation > max_eval:
                        max_eval = evaluation
                        if initial:
                            best_move = move

                    if evaluation > alpha:
                        alpha = evaluation

                    if beta <= alpha:
                        break


        if initial:
            return max_eval, best_move

        return max_eval

    else:
        min_eval = 10000
        possible_moves = []
        if initial:
            best_move = 0
        
        for piece in board.pieces:
            if piece.colour == "Black":
                for move in piece.possible_moves():
                    #new_board = deepcopy(board)
                    #new_piece = new_board.board[move[0].x][move[0].y]
                    #new_board.move(new_piece, move[1])


                    print(f"DEPTH: {depth}")
                    move_info = board.get_move_info(piece, move)
                    board.move(piece, move)

                    evaluation = minimax(board, depth - 1, alpha, beta, True, False)
                    
                    board.unmove(move_info)
                    print(f"DEPTH: {depth}")

                    if evaluation < min_eval:
                        min_eval = evaluation
                        if initial:
                            best_move = move

                    if evaluation < beta:
                        beta = min_eval

                    if beta <= alpha:
                        break


        if initial:
            return min_eval, best_move

        return min_eval

if __name__ == "__main__":
    board = Board()
    start_time = time.time()
    print(minimax(board, 5, -10000, 10000, True))
    print(c)
