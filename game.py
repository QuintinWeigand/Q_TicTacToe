from Board import Board
from Players import Player
import time
from pymongo import MongoClient
from itertools import permutations

def main():
    # Mongo connection stuff
    client = MongoClient("mongodb://localhost:27017")
    db = client['TicTacToe']
    collection = db["GameResults"]

    board = Board()
    player1 = Player(1)
    player2 = Player(2)
    moveCount = 1


    while(not board.hasWinnerOrDraw()):
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
    
    board.displayBoard()

    gameStatus = board.getGameStatus()

    # print(gameStatus)

    if gameStatus['winner'] == "Player1":
        player1.setPlayerWinner()
    elif gameStatus['winner'] == 'Player2':
        player2.setPlayerWinner()

    # print(player1.dictify())
    # print(player2.dictify())
    
    finalDict = {
        "Player1": player1.dictify(),
        "Player2": player2.dictify(),
        "Epoch": int(time.time())
    }

    # print(finalDict)

    result = collection.insert_one(finalDict)

    print(f"Inserted document with _id: {result.inserted_id}")

if __name__ == "__main__":
    # main()
    possibilies = [1,2,3,4,5,6,7,8,9]
    perms = permutations(possibilies)
    
    count = 0
    for i in perms:
        player1_moves = []
        player2_moves = []
        move_num = 0
        for j in i:
            move_num += 1
            if move_num % 2 == 1:
                # Odd number, Player 1 moves
                player1_moves.append(j)
            else:
                # Even number, Player 2 moves
                player2_moves.append(j)
    
        print("Player 1: ", player1_moves)
        print("Player 2: ", player2_moves)




