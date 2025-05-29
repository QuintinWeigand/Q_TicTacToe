from Board import Board
from Players import Player

def main():
    board = Board()
    player1 = Player(1)
    player2 = Player(2)
    moveCount = 1


    while(not board.hasWinner()):
        board.displayBoard()
        if moveCount % 2 == 1:
            playerMoveSquare = input("Player 1: Please enter a square to place your 'X' -> : ")
            try:
                playerMoveSquare = int(playerMoveSquare)
                row, col = Board.convertNumPositionToIndex(playerMoveSquare)
            except Exception as e:
                print(f"Invalid input: {e}")
                continue

            if board.set(row, col, 'X'):
                player1.addMove(playerMoveSquare)
            else:
                continue
        elif moveCount % 2 == 0:
            playerMoveSquare = input("Player 2: Please enter a square to place your 'O' -> : ")
            try:
                playerMoveSquare = int(playerMoveSquare)
                row, col = Board.convertNumPositionToIndex(playerMoveSquare)
            except Exception as e:
                print(f"Invalid input: {e}")
                continue

            if board.set(row, col, 'O'):
                player2.addMove(playerMoveSquare)
            else:
                continue
        else:
            raise RuntimeError("Panic: Something has gone terribly wrong!!!")
        
        moveCount += 1

    

if __name__ == "__main__":
    main()