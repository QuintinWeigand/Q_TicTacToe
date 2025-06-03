from Board import Board
from Players import Player
from pymongo import MongoClient
from itertools import permutations
import time

def main():
    # Mongo connection stuff
    client = MongoClient("mongodb://localhost:27017")
    db = client['TicTacToe']
    collection = db["GameResults"]

    # All game result dicts in a list
    gameResults = []

    # Game number count
    gameNumber = 0

    # Calculating each players move set for the match
    possibilies = [1,2,3,4,5,6,7,8,9]
    perms = permutations(possibilies)
    
    # This loop goes through each permutation
    for i in perms:
        player1_moves = []
        player2_moves = []
        move_num = 0
        for j in i:
            move_num += 1
            if move_num % 2 == 1:
                player1_moves.append(j)
            else:
                player2_moves.append(j)
        # Create new board and players for each game

        board = Board()
        player1 = Player(1)
        player2 = Player(2)
        gameNumber += 1
        result = playMatch(
            gameNumber,
            board,
            player1,
            player2,
            player1_moves,
            player2_moves,
        )
        gameResults.append(result)

        # print(f"Played match number: {gameNumber}\nPlayer 1 Moves: {player1_moves}\nPlayer 2 Moves: {player2_moves}")

        # Inserting 60 records then clearing the list NOTE: Must be divisible by 9!
        if len(gameResults) == 60:
            print(f"Inserting 60 documents. Currently on game {gameNumber}")
            collection.insert_many(gameResults)
            gameResults.clear()
    



def playMatch(gameNumber: int, board:Board, player1: Player, player2: Player, player1Moves: list, player2Moves: list) -> dict:
    
    moveCount = 1
    player1MoveNum = 0
    player2MoveNum = 0

    while(not board.hasWinnerOrDraw()):
       
        # board.displayBoard()

        # Player 1 move
        if moveCount % 2 == 1:
            try:
                row,col = Board.convertNumPositionToIndex(player1Moves[player1MoveNum])
            except Exception as e:
                raise RuntimeError(f"Something went wrong. Error: {e}")
            
            if board.set(row, col, "X"):
                player1.addMove(player1Moves[player1MoveNum])
            else:
                raise RuntimeError("Board was not set!")
            
            player1MoveNum += 1
        # Player 2 move
        elif moveCount % 2 == 0:
            try:
                row,col = Board.convertNumPositionToIndex(player2Moves[player2MoveNum])
            except Exception as e:
                raise RuntimeError(f"Something went wrong. Error: {e}")
            
            if board.set(row, col, "O"):
                player2.addMove(player2Moves[player2MoveNum])
            else:
                raise RuntimeError("Board was not set!")
            
            player2MoveNum += 1
        # PANIC!!!
        else:
            raise RuntimeError("Panic: Something has gone terribly wrong!!!")
        
        moveCount += 1
    
    # board.displayBoard()

    gameStatus = board.getGameStatus()

    # print(gameStatus)

    if gameStatus['winner'] == "Player1":
        player1.setPlayerWinner()
    elif gameStatus['winner'] == 'Player2':
        player2.setPlayerWinner()

    # print(player1.dictify())
    # print(player2.dictify())
    
    finalDict = {
        "Game Number": gameNumber,
        "Player1": player1.dictify(),
        "Player2": player2.dictify(),
    }

    # Returning the final game dictionary
    return finalDict

    # print(finalDict)

    # result = collection.insert_one(finalDict)

    # print(f"Inserted document with _id: {result.inserted_id}")

if __name__ == "__main__":
    main()




