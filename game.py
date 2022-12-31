import random
import pygame
from numpy.core.defchararray import center

from const import *
from board import *
from dragger import Drager
from ai import AI
from piece import *
from move import *
from config import *
from math import inf
from copy import *
from board import Board
from square import *


class Game:
    def __init__(self):
        self.next_player = "white"
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Drager()
        self.config = Config()
        self.mode = "pvp"
        self.gameOver = False
        self.ai = AI(self, self.board)

    # Show methods
    # surface = screen
    def show_bg(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # if (row + col) % 2 == 0:
                #    color = (50, 50, 50) # black color
                # else:
                #   color = (255, 255, 255) # white color

                rect = (col * SQUSIZE, row * SQUSIZE, SQUSIZE, SQUSIZE)
                # bilt
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    # the position of the label
                    lbl_pos = (5, 5 + row * SQUSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                    # col coordinates
                    if row == 7:
                        # color
                        color = (
                            theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                        )
                        # label
                        lbl = self.config.font.render(
                            Square.get_alphacol(col), 1, color
                        )
                        lbl_pos = (col * SQUSIZE + SQUSIZE - 20, HEIGHT - 20)
                        # blit
                        surface.blit(lbl, lbl_pos)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        # fixing the size of the piece is still 128 pixels we want it return 80 pixels
                        piece.set_texture(size=80)

                        img = pygame.image.load(piece.texture)

                        img_center = (
                            col * SQUSIZE + SQUSIZE // 2,
                            row * SQUSIZE + SQUSIZE // 2,
                        )

                        piece.texture_rect = img.get_rect(center=img_center)

                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            # taking the current piece
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                color = (
                    theme.moves.light
                    if (move.final.row + move.final.col) % 2 == 0
                    else theme.moves.dark
                )
                # rect
                rect = (
                    move.final.col * SQUSIZE,
                    move.final.row * SQUSIZE,
                    SQUSIZE,
                    SQUSIZE,
                )
                # bilt
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = (
                    theme.trace.light
                    if (pos.row + pos.col) % 2 == 0
                    else theme.trace.dark
                )
                # rect
                rect = (pos.col * SQUSIZE, pos.row * SQUSIZE, SQUSIZE, SQUSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (
                self.hovered_sqr.col * SQUSIZE,
                self.hovered_sqr.row * SQUSIZE,
                SQUSIZE,
                SQUSIZE,
            )
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods to make easy for user to see what is happening
    # for the next turn
    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"

    def get_random_piece(self):
        pieces = self.board.get_peaces(self.next_player)
        return random.choice(list(pieces.items()))

    def get_random_move(self):
        piece, pos = self.get_random_piece()
        self.board.calc_moves(piece, pos[0], pos[1], bool=True)
        i = 0

        while piece.moves == [] and i < 100:
            piece, pos = self.get_random_piece()
            self.board.calc_moves(piece, pos[0], pos[1], bool=True)
            i += 1

        print(piece.name, piece.color)
        try:
            move = random.choice(piece.moves)
        except:
            return piece, None

        if not self.board.in_check(piece, move):
            return piece, move

        return piece, None

    def evaluate(self, board, max_color):
        if max_color == "white":
            return board.getWhiteScore(board) - board.getBlackScore(board)
        else:
            return board.getBlackScore(board) - board.getWhiteScore(board)

    def miniMax(self, board, depth, max_player, max_color, alpha, beta, piece, pos):

        board.calc_moves(piece, pos[0], pos[1])
        i = 0
        while piece.moves == []:
            piece, pos = self.get_random_piece()
            board.calc_moves(piece, pos[0], pos[1])
            i += 1
            if i == 1000:
                print("We Broke")
                return None, self.evaluate(board, max_color)
        try:
            best_move = random.choice(piece.moves)
        except:
            print(f"Exception Score = {self.evaluate(board,max_color)}")
            return self.get_random_move(), board.getWhiteScore(
                board
            ) - board.getBlackScore(board)
        if depth == 0:
            print(f"Depth = 0 Score = {self.evaluate(board,max_color)}")
            return None, self.evaluate(board, max_color)
        if max_player:
            max_eval = -inf
            for move in piece.moves:
                boardCpy = deepcopy(board)
                boardCpy.move(piece, move)
                # board.move(piece, move)
                current_eval = self.miniMax(
                    board, depth - 1, False, max_color, alpha, beta, piece, pos
                )[1]
                # board.UndoMove(piece)
                # boardCpy.UndoMove(piece)
                if current_eval > max_eval:
                    print(f"Current Eval = {current_eval},Max = {max_eval}")
                    print(f"best move changed = {move}")
                    max_eval = current_eval
                    best_move = move
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = inf
            for move in piece.moves:
                boardCpy = deepcopy(board)
                boardCpy.move(piece, move)
                # board.move(piece, move)
                current_eval = self.miniMax(
                    board, depth - 1, True, max_color, alpha, beta, piece, pos
                )[1]
                # boardCpy.UndoMove(piece)
                # board.UndoMove(piece)
                if current_eval < min_eval:
                    print(f"best move changed = {move}")
                    min_eval = current_eval
                    best_move = move
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def show_win_msg(self, surface, winner):
        # label
        lbl = self.config.font.render(f"{winner} won!", 1, (255, 255, 255))
        # position
        lbl_pos = (
            WIDTH // 2 - lbl.get_width() // 2,
            HEIGHT // 2 - lbl.get_height() // 2,
        )
        # rectangle spanning the width of the screen and height of the label
        rect = (0, HEIGHT // 2 - lbl.get_height() // 2, WIDTH, lbl.get_height())
        # blit
        pygame.draw.rect(surface, (0, 0, 0), rect)
        # blit
        surface.blit(lbl, lbl_pos)

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
