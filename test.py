from Board import Board
from Players import Player

def main():
    board = Board()
    player1 = Player(1)
    player2 = Player(2)
    moveCount = 1

    
    row, col = Board.convertNumPositionToIndex(1)
    print(row, col)
    

if __name__ == "__main__":
    main()