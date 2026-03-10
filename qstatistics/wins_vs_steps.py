from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np


def get_wins_by_steps(collection, limit=None):
    """Get wins grouped by total number of steps/moves"""
    wins_by_steps = {}

    query = {
        "$or": [
            {"Player1.isWinner": True},
            {"Player2.isWinner": True}
        ]
    }

    cursor = collection.find(query).limit(
        limit) if limit else collection.find(query)

    for doc in cursor:
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
    N_values = [1e5, 1e6, 1e7]
    collection_name = "QGameResults_10M"

    # Set global font size for better visibility
    plt.rcParams.update({"font.size": 20})

    plt.figure(figsize=(12, 8))

    # Define different line styles and colors for each case
    line_styles = ['-', '--', '-.']
    colors = ['blue', 'green', 'red']

    collection = db[collection_name]

    for i, N in enumerate(N_values):
        try:
            wins_by_steps = get_wins_by_steps(collection, limit=int(N))

            if wins_by_steps:
                steps = sorted(wins_by_steps.keys())
                wins = [wins_by_steps[step] for step in steps]

                # Convert to fraction of total runs
                total_wins = sum(wins)
                fractions = [win / total_wins for win in wins]

                print(f"Processing N = {int(N):,}: {
                      len(steps)} data points, total wins: {total_wins}")
                print(f"Step counts found: {steps}")
                print(f"Wins per step: {wins_by_steps}")
                plt.plot(steps, fractions,
                         label=f'N = {int(N):,}',
                         color=colors[i],
                         linestyle=line_styles[i],
                         linewidth=3,
                         markersize=6)
            else:
                print(f"No data found for N = {int(N):,}")
        except Exception as e:
            print(f"Error processing N = {int(N):,}: {e}")

    plt.xlabel('Number of Steps (Total Moves)', fontsize=20)
    plt.ylabel('Fraction of Total Wins', fontsize=20)
    plt.legend(fontsize=18)
    plt.grid(True, alpha=0.3)

    # Disable scientific notation for x-axis (3-12 range)
    plt.gca().xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, p: f'{int(x)}'))

    # Use scientific notation for y-axis if needed, with 4 significant figures
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, p: f'{x:.4g}'))

    plt.tight_layout()
    plt.savefig('plots/wins_vs_steps_multiple_N.png',
                dpi=300, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["TicTacToe"]
        main()
