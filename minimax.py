from board import *
from copy import deepcopy
import time

c = 0

def minimax(board, depth, alpha, beta, maximizing, initial=True):
    global c
    c += 1
    if depth == 0 or not (board.winner is None):
        if board.winner == "Draw":
            return 0

        elif board.winner == "White":
            return 9999

        elif board.winner == "Black":
            return -9999


        return board.evaluate()

    if maximizing:
        max_eval = -10000
        possible_moves = []
        if initial:
            best_move = 0
        
        for piece in board.pieces:
            if piece.colour == "White":
                for pos in piece.possible_moves():
                    possible_moves.append([[piece.x, piece.y], pos])

        count = 0
        
        for move in possible_moves:
            if initial:
                count += 1
                print(f"pito: {count}")

            new_piece = board.board[move[0][0]][move[0][1]]
            board.save_state()

            board.move(new_piece, move[1])
            evaluation = minimax(board, depth - 1, alpha, beta, False, False)

            if evaluation > max_eval:
                max_eval = evaluation
                if initial:
                    best_move = move

            if evaluation > alpha:
                alpha = evaluation

            if beta <= alpha:
                break

            board.load_state()


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
                for pos in piece.possible_moves():
                    possible_moves.append([[piece.x, piece.y], pos])


        for move in possible_moves:

            new_piece = board.board[move[0][0]][move[0][1]]
            
            board.save_state()
            board.move(new_piece, move[1])
            evaluation = minimax(board, depth - 1, alpha, beta, False, False)

            if evaluation < min_eval:
                min_eval = evaluation
                if initial:
                    best_move = move

            if evaluation < beta:
                beta = min_eval

            if beta <= alpha:
                break

            board.load_state()


        if initial:
            return min_eval, best_move

        return min_eval

if __name__ == "__main__":
    board = Board()
    start_time = time.time()
    print(minimax(board, 5, -10000, 10000, True))
    print(c)
