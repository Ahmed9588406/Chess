import pygame
from numpy.core.defchararray import center

from const import *
from board import *
from dragger import Drager
from piece import *
from move import *
from config import *

class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Drager()
        self.config = Config()

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
                #else:
                 #   color = (255, 255, 255) # white color


                rect = (col * SQUSIZE, row * SQUSIZE,SQUSIZE, SQUSIZE)
                # bilt
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    #color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    # the position of the label
                    lbl_pos = (5, 5 + row * SQUSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)

                    # col coordinates
                    if row == 7:
                        # color
                        color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                        # label
                        lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
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

                      img_center = col * SQUSIZE + SQUSIZE // 2, row * SQUSIZE + SQUSIZE//2

                      piece.texture_rect = img.get_rect(center=img_center)

                      surface.blit(img, piece.texture_rect)







    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            # taking the current piece
            piece = self.dragger.piece

            # loop all valid moves
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                #rect
                rect = (move.final.col * SQUSIZE, move.final.row * SQUSIZE, SQUSIZE, SQUSIZE)
                #bilt
                pygame.draw.rect(surface, color, rect)


    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQUSIZE, pos.row * SQUSIZE, SQUSIZE, SQUSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * SQUSIZE, self.hovered_sqr.row * SQUSIZE, SQUSIZE, SQUSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods to make easy for user to see what is happening
    # for the next turn
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'


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