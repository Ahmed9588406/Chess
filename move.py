
class Move:


    def __init__(self, initial, final):
        # initial and final are squares
        self.initial = initial
        self.final = final


    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f'-> {self.final.col}, {self.final.row}'
        return s

    # fixing the bug that python wasn't comparing between the move an tha valid move that suppose to the piece to move on so we make this function to make python doing that without looping without puroose
    # and there is comparing between squares that you are in and the one you will move on
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
