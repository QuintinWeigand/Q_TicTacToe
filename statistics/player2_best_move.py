from pymongo import MongoClient
import matplotlib.pyplot as plt

def count_player2_moves(collection):
    # Specific Query to find games that player 2 won or drew
    query = {
        "Player1.isWinner": False,
        "Player1.moves.0": {"$in": [1, 3, 5, 9]}
    }
    move_counter = {}
    for record in collection.find(query):
        player2 = record.get("Player2")

        if player2 is None:
            raise ValueError("Could not find Player2 statistics")
        
        player2_moves = player2.get("moves")

        if player2_moves is None:
            raise ValueError("Could not find Player2 move set")
        
        first_move = player2_moves[0]
        if first_move in move_counter:
            move_counter[first_move] += 1
        else:
            move_counter[first_move] = 1

    return move_counter

def main():
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client["TicTacToe"]
        collection = db["GameResults"]
        player2_move_dict = count_player2_moves(collection)
    except Exception as e:
        raise RuntimeError(f"Error: {e}")
    
    player2_move_dict = dict(sorted(player2_move_dict.items()))

    print(player2_move_dict)

    # Plotting the results
    moves = list(player2_move_dict.keys())
    counts = list(player2_move_dict.values())

    bars = plt.bar(moves, counts, color=['red', 'grey', 'blue'])
    plt.xlabel('Player 2 First Move')
    plt.ylabel('Number of Wins/Draws')
    plt.title('Player 2 First Move Frequency (Wins/Draws)')
    plt.xticks(moves)
    plt.tight_layout()

    plt.bar_label(bars, padding=3)
    
    plt.savefig("plots/player2_best_move.png")
    


if __name__ == "__main__":
    main()