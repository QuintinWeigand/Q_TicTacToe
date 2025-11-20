from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np


def get_wins_by_steps(collection):
    """Get wins grouped by total number of steps/moves"""
    wins_by_steps = {}

    query = {
        "$or": [
            {"Player1.isWinner": True},
            {"Player2.isWinner": True}
        ]
    }

    for doc in collection.find(query):
        player1 = doc.get("Player1", {})
        player2 = doc.get("Player2", {})
        player1_moves = player1.get("moves", [])
        player2_moves = player2.get("moves", [])

        total_steps = len(player1_moves) + len(player2_moves)

        if total_steps not in wins_by_steps:
            wins_by_steps[total_steps] = 0
        wins_by_steps[total_steps] += 1

    return wins_by_steps


def main():
    N_values = [1e7]
    collection_names = ["QGameResults_10M"]

    plt.figure(figsize=(12, 8))

    colors = ['blue', 'green', 'orange', 'red']

    for i, (N, collection_name) in enumerate(zip(N_values, collection_names)):
        try:
            collection = db[collection_name]
            wins_by_steps = get_wins_by_steps(collection)

            if wins_by_steps:
                steps = sorted(wins_by_steps.keys())
                wins = [wins_by_steps[step] for step in steps]

                plt.plot(steps, wins, 'o-',
                         label=f'N = {int(N):,}',
                         color=colors[i],
                         linewidth=2,
                         markersize=6)
        except Exception as e:
            print(f"Error processing {collection_name}: {e}")

    plt.xlabel('Number of Steps (Total Moves)', fontsize=12)
    plt.ylabel('Number of Wins', fontsize=12)
    plt.title(
        'Number of Wins as a Function of Steps for Different N Values', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig('plots/wins_vs_steps_multiple_N.png',
                dpi=300, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["TicTacToe"]
        main()
