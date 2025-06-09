from QParticle import QParticle
from collections import deque

class QBoardSquare:
    def __init__(self, square_num: int):
        self.__particle_list = deque() # double ended queue can give us linked list functionality
        self.__square_num = square_num

    def get_square_num(self) -> int:
        return self.__square_num
    
    def add_particle(self, particle: QParticle):
        self.__particle_list.append(particle)

    def remove_particle(self, particle: QParticle):
        try:
            self.__particle_list.remove(particle)
        except:
            print("Particle was not found")

    def get_particle_list_copy(self) -> deque:
        return self.__particle_list.copy()