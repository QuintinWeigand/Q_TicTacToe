from QBoardSquare import QBoardSquare
from QParticle import QParticle

# TODO: QBoard will handle the detecting cycles using recursion going through each square finding same subscript particles

class QBoard:
    def __init__(self):
        self.__q_board = [QBoardSquare(i + 1) for i in range(9)]

    def display_board(self):
        for i in range(len(self.__q_board)):
            print(f"{i + 1} | {str(self.__q_board[i])}")

    def add_player_move(self, board_position: int, move_number: int, creation_number: int):
        if board_position >= 1 and board_position <= 9:
            particle = QParticle(move_number, creation_number)
            self.__q_board[board_position - 1].add_particle(particle)
        else: 
            raise ValueError("Incorrect board position")
        
    # TODO: Stub method for now, find cycles in the board (recursion?)
    def detect_cycle(self):
        pass