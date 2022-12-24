import copy
from math import inf
import random


class AI():
    def __init__(self, game, board):
        self.game = game
        self.board = board

    def evaluate(self, board, color):
        return (board.get_score(board)) * (1 if color == "black" else -1)

    def minimax(self, board, depth, alpha, beta, maximizingPlayer, maximizingColor):
        if depth == 0 or self.game.gameOver:
            return None, self.evaluate(board, maximizingColor)
        
        moves = list(board.get_moves(maximizingColor, board).items())
        random.shuffle(moves)
        bestMove = random.choice(moves)
        tempBoard = copy.deepcopy(board)

        bestValue = alpha if maximizingPlayer else beta

        for piece, movess in moves:
            tempPiece = copy.deepcopy(piece)
            for move in movess:
                print("trying ", piece.name, piece.color," in ", move.final.row, move.final.col, "score:", bestValue, "depth:", depth)
                tempBoard.move(tempPiece, move, testing=True)
                tempBoard.set_true_en_passant(tempPiece)
                eval = self.minimax(tempBoard ,depth - 1, alpha, beta, False, maximizingColor)[1]
                if maximizingPlayer:
                    if eval > bestValue:
                        bestValue = eval
                        bestMove = (piece,move)
                    alpha = max(alpha, eval)
                else:
                    if eval < bestValue:
                        bestValue = eval
                        bestMove = (piece,move)
                    beta = min(beta, eval)
                tempBoard = copy.deepcopy(self.board)
                tempPiece = copy.deepcopy(piece)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return (bestMove, bestValue)
            

