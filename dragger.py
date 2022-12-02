import pygame

from const import *

class Drager:

    def __init__(self):
        self.piece = None # the piece we are dragging
        self.dragging = False
        self.mousex = 0
        self.mousey = 0
        self.initial_row = 0
        self.initial_col = 0


    # blit method
    # here we need to display the piece that we choose to be bigger when we choose it to move
    def update_blit(self, surface):
        # texture : the path of the piece image
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # img that we will display
        img = pygame.image.load(texture)
        # rect
        img_center = (self.mousex, self.mousey)
        self.piece.texture_rect = img.get_rect(center=img_center)
        # blit
        surface.blit(img, self.piece.texture_rect)



       # other methods to handle different moves or states


    def update_mouse(self, pos):
        self.mousex, self.mousey = pos # (xcor, ycor) to store the cordinates from the update_pos function of pygame



    def save_initiial(self,pos):
        self.initial_row = pos[1] // SQUSIZE
        self.initial_col = pos[0] // SQUSIZE

    # to let the piece on board
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True


    def undrag_piece(self):
        self.piece = None
        self.dragging = False
