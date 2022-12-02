import pygame
import sys

from const import *
from game import *
from piece import *
from board import *
from square import *
# class Main has two function
# 1. the init function for every time we make an object it directly called
# 2. the main loop function to loop over the functions or action we will do
class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess Game')
        pygame_icon = pygame.image.load('chess.png')
        pygame.display.set_icon(pygame_icon)
        self.game = Game()

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        # display the layout of the pygame window
        while True:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            # fixing 1st bug that make the piece distinct
            if dragger.dragging:
                dragger.update_blit(screen)
            for event in pygame.event.get():
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)# showing the pos of the clicking mouse
                    clicked_row = dragger.mousey // SQUSIZE
                    clicked_col = dragger.mousex // SQUSIZE

                    # if clicked square has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():

                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece color
                        if piece.color == game.next_player:
                           board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                           dragger.save_initiial(event.pos)
                           dragger.drag_piece(piece)
                           # show methods
                           game.show_bg(screen)
                           game.show_last_move(screen)
                           game.show_moves(screen)
                           game.show_pieces(screen)



                # Mouse Motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQUSIZE
                    motion_col = event.pos[0] // SQUSIZE
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # fixing the shadow behind the selected piece
                        game.show_bg(screen)
                        # fixing the all pices that have been copied
                        # show methods
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)



                # Click release
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mousey // SQUSIZE
                        released_col = dragger.mousex // SQUSIZE


                        # create possible moves
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)


                        # checking if the move is a valid one
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            board.set_true_en_passant(piece)
                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()


                    dragger.undrag_piece()

                # Key press
                elif event.type == pygame.KEYDOWN:


                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()


                    # changing themes
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger


                # Quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()



            pygame.display.update()






main = Main()
main.mainloop()









