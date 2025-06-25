from QuantumGame.QuantumGame import QuantumGame
from Players import Player
import random as rand

from pymongo import MongoClient

def main():
    num_games = 1000000
    # (Moved game creation inside the game loop)

    # Creating all possible move permutations
    available = []
    pairs = []
    
    # (Moved player1 and player2 instantiation inside the game loop)

    # for i in range(1,10):
    #     for j in range(1,10):
    #         if i != j:
    #             perms.append((i,j))

    # perms_size = len(perms)

    # (Moved move_number and collapse_move_list initialization inside the game loop)

    game_number = 0
    game_document_list = []

    while game_number < num_games:
        game = QuantumGame()
        player1 = Player(1)
        player2 = Player(2)
        move_number = 0
        collapse_move_list = []
        while not game.game_over:
            # game.display_game_state()
            try:
                prev_player = game.current_player  # Store before move

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

                valid_pairs = get_valid_move_pairs()
                if not valid_pairs:
                    # print("No valid move pairs left. Ending game.")
                    game.game_over = True
                    break

                move = rand.choice(valid_pairs)
                pos1, pos2 = move

                # print(f"Current Player: {game.current_player} | Pos1: {pos1} | Pos2: {pos2}")
                # print(f"Pos1: {pos1} | Pos2: {pos2}")
                
                valid, collapse = game.make_move(pos1, pos2)
                if valid:
                    move_number += 1
                    if collapse:
                        collapse_move_list.append(move_number)
                    if prev_player == 1:
                        player1.addMove(move)
                    else:
                        player2.addMove(move)
                else:
                    print("Move failed! Try again.")     
            except ValueError:
                print("Invalid input! Please enter numbers between 1 and 9.")

        # print("\nFinal game state:")
        # game.display_game_state()
        # game.classical_board.displayBoard()
        # print(game.classical_board.getBoard())
        game_number += 1
        # print(f"Winner: {game.winner}")

        if game.winner == "Player1":
            player1.setPlayerWinner()
        elif game.winner == "Player2":
            player2.setPlayerWinner()

        final_game_stats = {
            "Game Number": game_number,
            "Player1": player1.dictify(),
            "Player2": player2.dictify(),
            "Collapse Move Info": collapse_move_list,
            "Board": game.classical_board.getBoard()
        }

        game_document_list.append(final_game_stats)

        # print(final_game_stats)

        if game_number % 10000 == 0:
            print(f"Game Number: {game_number} | {((game_number / num_games) * 100):.2f}%")

        if len(game_document_list) == 100:
            # print("Appending 10 documents to the database")
            collection.insert_many(game_document_list)
            game_document_list.clear()

if __name__ == "__main__":
    # Ensures the client is created and ALWAYS closed correctly (even with an exception)
    with MongoClient("mongodb://localhost:27017") as client:
        database = client["TicTacToe"]
        collection = database["QGameResults"]
        main()