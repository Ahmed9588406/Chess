import copy

from const import *
from square import *
from piece import *
from move import *
from sound import *
import os
from game import *


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._creat()
        self._add_piece("white")
        self._add_piece("black")
        self.moves_series = []
        self.whiteScore = 49
        self.blackScore = -49

    def UndoMove(self, piece):
        move = self.moves_series.pop()
        initial = move.initial
        final = move.final
        self.move(
            piece, Move(Square(final.row, final.col), Square(initial.row, initial.col))
        )
        self.moves_series.pop()

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        en_passant_empty = self.squares[final.row][final.col].is_empty()

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update

                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join("assets/sounds/capture.wav"))
                    sound.play()

            # pawn en passant
            #  if self.en_passant(initial, final):
            #     piece.en_passant = True
            # test: print(" pawn moved two sqrs")

            # Pawn promotion
            else:
                self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid moves from the list that we created to store moves
        piece.clear_moves()

        # set last move
        self.last_move = move  # every time we want to render the move

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
            if piece.color == "white":
                self.scorewhite += 9
                print(self.scorewhite, "white", self.scoreblack)
            else:
                self.scoreblack += 9
                print(self.scorewhite, self.scoreblack, "black")

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    #  def en_passant(self, initial, final):
    #     return abs(initial.row - final.row) == 2

    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        piece.en_passant = True

    def in_check(self, piece, move):
        # coping all the properties of the board
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def valid_move(self, piece, move):
        return move in piece.moves

    # get all the valid moves of all the pieces of a specific color
    def get_all_moves(self, color):
        moves = {}
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    piece = self.squares[row][col].piece
                    if piece.color == color:
                        self.calc_moves(piece, row, col)
                        if len(piece.moves) > 0:
                            moves[piece] = piece.moves
        return moves

    def calc_moves(self, piece, row, col, bool=True):
        """
        Calculate all the valid moves of an specific piece on a specific position
        """

        def pawn_moves():
            # steps
            # this is the moves of the piece pawn first 2 steps after that 1 step
            steps = 1 if piece.moved else 2

            # Vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)

                        # create a new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):

                                # append new move in move list in the function add_move
                                piece.add_move(move)
                        else:
                            # append new moves
                            piece.add_move(move)

                        # blocked
                    else:
                        break
                    # not in range
                else:
                    break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][
                        possible_move_col
                    ].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][
                            possible_move_col
                        ].piece
                        final = Square(
                            possible_move_row, possible_move_col, final_piece
                        )
                        # create a new move
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move in move list in the function add_move
                                piece.add_move(move)
                        else:
                            # append new moves
                            piece.add_move(move)

            # en passant moves
            r = 3 if piece.color == "white" else 4
            fr = 2 if piece.color == "white" else 5
            # left en passant
            if Square.in_range(col - 1) and row == r:
                if self.squares[row][col - 1].has_enemy_piece(piece.color):
                    p = self.squares[row][col - 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            # final_piece = self.squares[row][col-1].piece
                            final = Square(fr, col - 1, p)
                            # create a new move
                            move = Move(initial, final)
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move in move list in the function add_move
                                    piece.add_move(move)
                            else:
                                # append new moves
                                piece.add_move(move)

            # right en passant
            if Square.in_range(col + 1) and row == r:
                if self.squares[row][col + 1].has_enemy_piece(piece.color):
                    p = self.squares[row][col + 1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            # final_piece = self.squares[row][col-1].piece
                            final = Square(fr, col + 1, p)
                            # create a new move
                            move = Move(initial, final)
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move in move list in the function add_move
                                    piece.add_move(move)
                            else:
                                # append new moves
                                piece.add_move(move)

        def knight_moves():
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][
                        possible_move_col
                    ].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)  # the current row
                        final_piece = self.squares[possible_move_row][
                            possible_move_col
                        ].piece
                        final = Square(
                            possible_move_row, possible_move_col, final_piece
                        )  # use the final square of the board

                        # create new move
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move in move list in the function add_move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new moves
                            piece.add_move(move)

        # this function will be used in Bishop Rook and Queen because they move in straight lines but in different increment
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][
                            possible_move_col
                        ].piece
                        final = Square(
                            possible_move_row, possible_move_col, final_piece
                        )
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][
                            possible_move_col
                        ].is_empty():
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move in move list in the function add_move
                                    piece.add_move(move)
                            else:
                                # append new moves
                                piece.add_move(move)

                        # has enemy piece
                        elif self.squares[possible_move_row][
                            possible_move_col
                        ].has_enemy_piece(piece.color):
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move in move list in the function add_move
                                    piece.add_move(move)
                            else:
                                # append new moves
                                piece.add_move(move)

                            break
                            # has team piece = break : handling the bug that if you are a white piece and it is you first move you can't move the queen or the king or the rook and so on
                        elif self.squares[possible_move_row][
                            possible_move_col
                        ].has_team_piece(piece.color):
                            break

                    # not in range
                    else:
                        break

                    # increment the incrs of each piece
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row - 1, col + 0),  # up
                (row - 1, col + 1),  # up_right
                (row + 0, col + 1),  # right
                (row + 1, col + 1),  # down_right
                (row + 1, col + 0),  # down
                (row + 1, col - 1),  # down_left
                (row + 0, col - 1),  # left
                (row - 1, col - 1),  # up_left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][
                        possible_move_col
                    ].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # create new move
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move in move list in the function add_move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new moves
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # Queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            # castling is not possible because there are pieces in between
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # check potential checks
                                if bool:
                                    if not self.in_check(
                                        piece, moveK
                                    ) and not self.in_check(left_rook, moveR):
                                        # append new move for the rook
                                        left_rook.add_move(moveR)
                                        # append new move in move list in the function add_move
                                        # for the king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # check potential checks
                                if bool:
                                    if not self.in_check(
                                        piece, moveK
                                    ) and not self.in_check(right_rook, moveR):
                                        # append new move for the rook
                                        right_rook.add_move(moveR)
                                        # append new move in move list in the function add_move
                                        # for the king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move king
                                    piece.add_move(moveK)

        # chercking if the the child piece is an instance of the Knight class
        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves(
                [
                    (-1, 1),  # up_right
                    (-1, -1),  # up_left
                    (1, 1),  # down_right
                    (1, -1),  # down_left
                ]
            )

        elif isinstance(piece, Rook):
            straightline_moves(
                [
                    (-1, 0),  # straight_up
                    (0, 1),  # straight_right
                    (1, 0),  # straight_down
                    (0, -1),  # straight_left
                ]
            )

        # Queen is a merge between Bishop move and Rook move
        elif isinstance(piece, Queen):
            straightline_moves(
                [
                    (-1, 1),  # up_right
                    (-1, -1),  # up_left
                    (1, 1),  # down_right
                    (1, -1),  # down_left
                    (-1, 0),  # straight_up
                    (0, 1),  # straight_right
                    (1, 0),  # straight_down
                    (0, -1),  # straight_left
                ]
            )

        elif isinstance(piece, King):
            king_moves()

    # make it private by passing _ before creat
    def _creat(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_piece(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)
        """
        Here you can make any object from any class to check if the function that responsible for moving pieces works 
        """
        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        # test # self.squares[4][4] = Square(4, 4, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        # test #self.squares[3][3] = Square(4, 4, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    # self.squares[5][3] = Square(5, 3, King(color)) -> testing if the king moves valid for the enemy pieces
    # self.squares[2][3] = Square(2, 3, King(color)) -> testing if the king will eat his own ally

    def get_peaces(self, color):
        peaces = {}
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    piece = self.squares[row][col].piece
                    if piece.color == color:
                        peaces[piece] = (row, col)
        return peaces

    def get_score(self, board):
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if piece.color == "black":
                        score += piece.value
                    elif piece.color == "white":
                        score -= piece.value

        return score

    def getBlackScore(self, board):
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if piece.color == "black":
                        score -= piece.value
        return score

    def getWhiteScore(self, board):
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    piece = board.squares[row][col].piece
                    if piece.color == "white":
                        score += piece.value
        return score

    def reset_score(self):
        self.whiteScore = 49
        self.blackScore = -49

    def AllPossible(self, color):
        moves = {}
        dic = self.get_peaces(color)
        for piece in dic.keys():
            self.calc_moves(piece, dic[piece][0], dic[piece][1])
            tmp = []
            for move in piece.moves:
                if self.valid_move(piece, move):
                    tmp.append(move)
            moves[piece] = tmp
        return moves

    def reset_score(self):
        self.white_score = 49
        self.black_score = -49
