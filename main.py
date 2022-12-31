from math import inf
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
        pygame.display.set_caption("Chess Game")
        pygame_icon = pygame.image.load("chess.png")
        pygame.display.set_icon(pygame_icon)
        self.game = Game()
        self.i = 0
        self.black_first_move = True

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        mode = self.game.mode

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
                if mode == "pvp":
                    # click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(
                            event.pos
                        )  # showing the pos of the clicking mouse
                        clicked_row = dragger.mousey // SQUSIZE
                        clicked_col = dragger.mousex // SQUSIZE

                        # if clicked square has a piece
                        if board.squares[clicked_row][clicked_col].has_piece():

                            piece = board.squares[clicked_row][clicked_col].piece
                            # valid piece color
                            if piece.color == game.next_player:
                                board.calc_moves(
                                    piece, clicked_row, clicked_col, bool=True
                                )
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
                                captured = board.squares[released_row][
                                    released_col
                                ].has_piece()
                                if captured:
                                    piecee = board.squares[released_row][
                                        released_col
                                    ].piece
                                    if piecee.color == "white":
                                        board.scorewhite -= piecee.value
                                        print(board.scorewhite, board.scoreblack)
                                    else:
                                        board.scoreblack -= piecee.value
                                        print(board.scorewhite, board.scoreblack)
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
                elif mode == "r":
                    # white player
                    if game.next_player == "white":
                        # click
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            dragger.update_mouse(
                                event.pos
                            )  # showing the pos of the clicking mouse
                            clicked_row = dragger.mousey // SQUSIZE
                            clicked_col = dragger.mousex // SQUSIZE

                            # if clicked square has a piece
                            if board.squares[clicked_row][clicked_col].has_piece():

                                piece = board.squares[clicked_row][clicked_col].piece
                                # valid piece color
                                if piece.color == game.next_player:
                                    board.calc_moves(
                                        piece, clicked_row, clicked_col, bool=True
                                    )
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
                                initial = Square(
                                    dragger.initial_row, dragger.initial_col
                                )
                                final = Square(released_row, released_col)
                                move = Move(initial, final)

                                # checking if the move is a valid one
                                if board.valid_move(dragger.piece, move):
                                    captured = board.squares[released_row][
                                        released_col
                                    ].has_piece()
                                    if captured:
                                        piecee = board.squares[released_row][
                                            released_col
                                        ].piece
                                        if piecee.color == "white":
                                            board.scorewhite -= piecee.value
                                            print(board.scorewhite, board.scoreblack)
                                        else:
                                            board.scoreblack -= piecee.value
                                            print(board.scorewhite, board.scoreblack)
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
                    elif game.next_player == "black":
                        # random move for black
                        piece, move = game.get_random_move()

                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                        if move is None:
                            # show a winning message for white player and exit the game
                            game.gameOver = True
                            game.show_win_msg(screen, "white")
                            pygame.display.update()
                            pygame.time.delay(3000)
                            game.reset()
                            game.mode = "pvp"
                            mode = "pvp"
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            game.gameOver = False
                            board.scorewhite = 1039
                            board.scoreblack = 1039

                        if board.valid_move(piece, move):
                            captured = board.squares[move.final.row][
                                move.final.col
                            ].has_piece()
                            if captured:
                                piecee = board.squares[released_row][released_col].piece
                                if piecee.color == "white":
                                    board.scorewhite -= piecee.value
                                    print(board.scorewhite, board.scoreblack)
                                else:
                                    board.scoreblack -= piecee.value
                                    print(board.scorewhite, board.scoreblack)
                            board.move(piece, move)
                            board.set_true_en_passant(piece)
                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                elif mode == "ai":
                    # white player
                    if game.next_player == "white":
                        # click
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            dragger.update_mouse(
                                event.pos
                            )  # showing the pos of the clicking mouse
                            clicked_row = dragger.mousey // SQUSIZE
                            clicked_col = dragger.mousex // SQUSIZE

                            # if clicked square has a piece
                            if board.squares[clicked_row][clicked_col].has_piece():

                                piece = board.squares[clicked_row][clicked_col].piece
                                # valid piece color
                                if piece.color == game.next_player:
                                    board.calc_moves(
                                        piece, clicked_row, clicked_col, bool=True
                                    )
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
                                initial = Square(
                                    dragger.initial_row, dragger.initial_col
                                )
                                final = Square(released_row, released_col)
                                move = Move(initial, final)

                                # checking if the move is a valid one
                                if board.valid_move(dragger.piece, move):
                                    captured = board.squares[released_row][
                                        released_col
                                    ].has_piece()
                                    if captured:
                                        piecee = board.squares[released_row][
                                            released_col
                                        ].piece
                                        if piecee.color == "white":
                                            board.scorewhite -= piecee.value
                                            print(board.scorewhite, board.scoreblack)
                                        else:
                                            board.scoreblack -= piecee.value
                                            print(board.scorewhite, board.scoreblack)
                                    board.move(dragger.piece, move)
                                    board.set_true_en_passant(piece)
                                    # soundsa
                                    game.play_sound(captured)
                                    # show methods
                                    game.show_bg(screen)
                                    game.show_last_move(screen)
                                    game.show_pieces(screen)
                                    # next turn
                                    game.next_turn()

                            dragger.undrag_piece()
                    elif game.next_player == "black":
                        # get ai move for black

                        piece, move = game.ai.minimax(
                            board, 3, -inf, inf, True, "black"
                        )[0]

                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                        if move is None:
                            # show a winning message for white player and exit the game
                            game.gameOver = True
                            game.show_win_msg(screen, "white")
                            pygame.display.update()
                            pygame.time.delay(3000)
                            game.reset()
                            game.mode = "pvp"
                            mode = "pvp"
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            game.gameOver = False
                            board.scorewhite = 1039
                            board.scoreblack = 1039
                            continue

                        if board.valid_move(piece, move):
                            captured = board.squares[move.final.row][
                                move.final.col
                            ].has_piece()
                            if captured:
                                piecee = board.squares[released_row][released_col].piece
                                if piecee.color == "white":
                                    board.scorewhite -= piecee.value
                                    print(board.scorewhite, board.scoreblack)
                                else:
                                    board.scoreblack -= piecee.value
                                    print(board.scorewhite, board.scoreblack)
                            board.move(piece, move)
                            board.set_true_en_passant(piece)
                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                    # From here
                elif mode == "a":
                    # white player
                    if game.next_player == "white":
                        # click
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            dragger.update_mouse(
                                event.pos
                            )  # showing the pos of the clicking mouse
                            clicked_row = dragger.mousey // SQUSIZE
                            clicked_col = dragger.mousex // SQUSIZE

                            # if clicked square has a piece
                            if board.squares[clicked_row][clicked_col].has_piece():

                                piece = board.squares[clicked_row][clicked_col].piece
                                # valid piece color
                                if piece.color == game.next_player:
                                    board.calc_moves(
                                        piece, clicked_row, clicked_col, bool=True
                                    )
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
                            # game.set_hover(motion_row, motion_col)

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
                                initial = Square(
                                    dragger.initial_row, dragger.initial_col
                                )
                                final = Square(released_row, released_col)
                                move = Move(initial, final)

                                # checking if the move is a valid one
                                if board.valid_move(dragger.piece, move):
                                    captured = board.squares[released_row][
                                        released_col
                                    ].has_piece()
                                    board.move(dragger.piece, move)
                                    board.set_true_en_passant(piece)
                                    # sounds
                                    game.play_sound(captured)
                                    # show methods
                                    game.show_bg(screen)
                                    game.show_last_move(screen)
                                    game.show_pieces(screen)
                                    # next turn
                                    # print(board.moves_series)

                                    game.next_turn()

                            dragger.undrag_piece()

                    elif game.next_player == "black":
                        # generates random moves for first 5
                        # if self.black_first_move:
                        #     piece, move = game.get_random_move()
                        #     self.i += 1
                        #     self.black_first_move = False if self.i == 5 else True
                        # else:
                        # for possible in board.AllPossible(game.next_player):
                        #     print(possible[0].name,possible[1])

                        piece, pos = game.get_random_piece()
                        move, eval = game.miniMax(
                            board,
                            6,
                            True,
                            game.next_player,
                            -inf,
                            inf,
                            piece,
                            pos,
                        )
                        print(board.get_score(board), move)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)

                        if move is None:
                            game.show_win_msg(screen, "white")
                            pygame.display.update()
                            pygame.time.delay(6000)
                            game.reset()
                            game.mode = "a"
                            mode = "a"
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger

                        if board.valid_move(piece, move):
                            captured = board.squares[move.final.row][
                                move.final.col
                            ].has_piece()
                            board.move(piece, move)

                            # board.UndoMove(piece)
                            # print(board.moves_series)

                            board.set_true_en_passant(piece)
                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                # Key press
                if event.type == pygame.KEYDOWN:

                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # changing themes
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                    if event.key == pygame.K_p:
                        game.reset()
                        game.mode = "pvp"
                        mode = "pvp"
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                        board.scorewhite = 49
                        board.scoreblack = -49

                    if event.key == pygame.K_h:
                        game.reset()
                        game.mode = "r"
                        mode = "r"
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                        board.scorewhite = 49
                        board.scoreblack = -49

                    if event.key == pygame.K_a:
                        game.reset()
                        game.mode = "a"
                        mode = "a"
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                        board.scorewhite = 49
                        board.scoreblack = -49

                # Quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.mainloop()
