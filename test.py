from Board import Board
from Players import Player

def main():
    board = Board()
    player1 = Player(1)
    player2 = Player(2)

    
    # board.displayBoard()
    board.set(0,2, 'X')
    board.set(1,1, 'X')
    board.set(2,0, 'X')
    if board.hasWinner():
        print("Winner!")
    

if __name__ == "__main__":
    main()