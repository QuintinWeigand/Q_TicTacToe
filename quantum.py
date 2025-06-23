from QuantumGame.QuantumGame import QuantumGame
from Players import Player
import random as rand

from pymongo import MongoClient

def main():
    # Creating the game (relies on classical board in implementation)
    game = QuantumGame()

    # Creating each player
    player1 = Player(1)
    player2 = Player(2)

    # Creating all possible move permutations
    available = []
    pairs = []

    # for i in range(1,10):
    #     for j in range(1,10):
    #         if i != j:
    #             perms.append((i,j))

    # perms_size = len(perms)

    move_number = 0
    collapse_move_list = []


    while not game.game_over:
        game.display_game_state()
        try:
            print(f"\nPlayer {game.current_player}'s turn")
            # print("Enter two different positions (1-9) for quantum superposition")
            # pos1 = int(input("First position: "))
            # pos2 = int(input("Second position: "))

            # Helper to get valid move pairs based on classical board state
            def get_valid_move_pairs():
                available = []
                for pos in range(1, 10):
                    row, col = game.classical_board.convertNumPositionToIndex(pos)
                    if game.classical_board.get(row, col).isdigit():
                        available.append(pos)
                pairs = []
                for i in available:
                    for j in available:
                        if i != j:
                            pairs.append((i, j))
                return pairs
            move = rand.choice(get_valid_move_pairs())
            pos1, pos2 = move

            print(f"Pos1: {pos1} | Pos2: {pos2}")
            
            valid, collapse = game.make_move(pos1, pos2)
            if valid:
                move_number += 1
                # print("Move successful!" + (" (Collapse occurred!)" if collapse else ""))
                if collapse:
                    collapse_move_list.append(move_number)
                if game.current_player == 1:
                    player1.addMove(move)
                else:
                    player2.addMove(move)
            else:
                print("Move failed! Try again.")
                
        except ValueError:
            print("Invalid input! Please enter numbers between 1 and 9.")


    print("\nFinal game state:")
    game.display_game_state()

if __name__ == "__main__":
    # Ensures the client is created and ALWAYS closed correctly (even with an exception)
    with MongoClient("mongodb://localhost:27017") as client:
        database = client["TicTacToe"]
        collection = database["QGameResults"]
        main()