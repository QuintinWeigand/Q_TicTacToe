from pymongo import MongoClient
import matplotlib.pyplot as plt
from collections import Counter

def count_moves(collection):
    player1_num_moves = []
    player2_num_moves = []

    for record in collection.find():
        player1 = record.get("Player1")
        player2 = record.get("Player2")

        if player1 == None or player2 == None:
            raise ValueError("Could not find player statistics in record")
        
        if player1.get("isWinner") == True:
            player1_num_moves.append(len(player1.get("moves")))
        elif player2.get("isWinner") == True:
            player2_num_moves.append(len(player2.get("moves")))

    return player1_num_moves, player2_num_moves

def main():
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client["TicTacToe"]
        collection = db["GameResults"]
        player1_win_moves, player2_win_moves = count_moves(collection)
    except Exception as e:
        raise RuntimeError(f"Error: {e}")

    # Count occurrences of each move number
    p1_counter = Counter(player1_win_moves)
    p2_counter = Counter(player2_win_moves)
    all_moves = sorted(set(p1_counter.keys()).union(p2_counter.keys()))

    p1_counts = [p1_counter.get(m, 0) for m in all_moves]
    p2_counts = [p2_counter.get(m, 0) for m in all_moves]

    bar_width = 0.4
    x = range(len(all_moves))

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    bars1 = ax.bar([i - bar_width/2 for i in x], p1_counts, width=bar_width, color='blue', label='Player 1 Wins')
    bars2 = ax.bar([i + bar_width/2 for i in x], p2_counts, width=bar_width, color='red', label='Player 2 Wins')
    plt.xlabel('Number of Moves to Win')
    plt.ylabel('Number of Wins')
    plt.title('Number of Wins by Moves to Win')
    plt.xticks(x, all_moves)
    plt.legend()
    plt.tight_layout()

    # Most abstracted way to add labels
    ax.bar_label(bars1, label_type='edge', color='blue')
    ax.bar_label(bars2, label_type='edge', color='red')

    plt.savefig("plots/move_counts_bar.png")

if __name__ == "__main__":
    main()