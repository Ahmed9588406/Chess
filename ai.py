import copy
from math import inf
import random


class AI():
    def __init__(self, game, board):
        self.game = game
        self.board = board

    def evaluate(self, board, color):
        return board.scorewhite - board.scoreblack if color == 'white' else board.scoreblack - board.scorewhite

    def minimax(self, board, depth, alpha, beta, maximizingPlayer, maximizingColor):
        if depth == 0 or self.game.gameOver:
            return None, self.evaluate(board, maximizingColor)
        
        tempBoard = copy.deepcopy(board)
        moves = list(tempBoard.get_all_moves(maximizingColor).items())
        random.shuffle(moves)

        bestValue = -inf if maximizingPlayer else inf
        bestMove = random.choice(moves) if moves else bestValue,None

        if maximizingPlayer:
            for piece, movess in moves:
                tempPiece = copy.deepcopy(piece)
                for move in movess:
                    # tempMove = copy.deepcopy(move)
                    if tempBoard.valid_move(tempPiece, move):
                        print("trying ", piece.name, piece.color," in ", move.final.row, move.final.col, "score:", bestValue, "depth:", depth)
                        captured = tempBoard.squares[move.final.row][move.final.col].has_piece()
                        if captured:
                            piecee = tempBoard.squares[move.final.row][move.final.col].piece
                            if piecee.color == 'white' and tempPiece.color == 'black':
                                tempBoard.scorewhite -= piecee.value
                                print(tempBoard.scorewhite, tempBoard.scoreblack)
                            elif piecee.color == 'black' and tempPiece.color == 'white':
                                tempBoard.scoreblack -= piecee.value
                                print(tempBoard.scorewhite, tempBoard.scoreblack)
                            else:
                                continue
                        tempBoard.move(tempPiece, move)
                        tempBoard.set_true_en_passant(tempPiece)
                    else:
                        print("not valid")
                        continue
                    eval = self.minimax(tempBoard ,depth - 1, alpha, beta, False, maximizingColor)[1]
                    if eval > bestValue:
                        bestValue = eval
                        bestMove = (piece,move)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        print("prune1")
                        break
                if beta <= alpha:
                    print("prune2")
                    break
            return (bestMove, bestValue)
        else:
            for piece, movess in moves:
                tempPiece = copy.deepcopy(piece)
                for move in movess:
                    # tempMove = copy.deepcopy(move)
                    if tempBoard.valid_move(tempPiece, move):
                        print("trying ", piece.name, piece.color," in ", move.final.row, move.final.col, "score:", bestValue, "depth:", depth)
                        captured = tempBoard.squares[move.final.row][move.final.col].has_piece()
                        if captured:
                            piecee = tempBoard.squares[move.final.row][move.final.col].piece
                            if piecee.color == 'white' and tempPiece.color == 'black':
                                tempBoard.scorewhite -= piecee.value
                                print(tempBoard.scorewhite, tempBoard.scoreblack)
                            elif piecee.color == 'black' and tempPiece.color == 'white':
                                tempBoard.scoreblack -= piecee.value
                                print(tempBoard.scorewhite, tempBoard.scoreblack)
                            else:
                                continue
                        tempBoard.move(tempPiece, move)
                        tempBoard.set_true_en_passant(tempPiece)
                    else:
                        print("not valid")
                        continue
                    eval = self.minimax(tempBoard ,depth - 1, alpha, beta, True, maximizingColor)[1]
                    if eval < bestValue:
                        bestValue = eval
                        bestMove = (piece,move)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        print("prune1")
                        break
                if beta <= alpha:
                    print("prune2") 
                    break
            return (bestMove, bestValue)
            

