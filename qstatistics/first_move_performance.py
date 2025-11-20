from pymongo import MongoClient
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


def analyze_first_move_performance(collection):
    """Analyze win-loss difference for each starting move"""
    first_move_stats = defaultdict(
        lambda: {'wins': 0, 'losses': 0, 'total': 0})

    for doc in collection.find():
        player1 = doc.get("Player1", {})
        player2 = doc.get("Player2", {})
        player1_moves = player1.get("moves", [])
        player2_moves = player2.get("moves", [])

        if not player1_moves:
            continue

        first_move = tuple(player1_moves[0]) if isinstance(
            player1_moves[0], list) else player1_moves[0]

        player1_won = player1.get("isWinner", False)
        player2_won = player2.get("isWinner", False)

        first_move_stats[first_move]['total'] += 1
        if player1_won:
            first_move_stats[first_move]['wins'] += 1
        elif player2_won:
            first_move_stats[first_move]['losses'] += 1

    # Calculate win-loss difference
    results = {}
    for move, stats in first_move_stats.items():
        win_loss_diff = stats['wins'] - stats['losses']
        results[move] = win_loss_diff

    return results


def main():
    collection = db["QGameResults_10M"]  # Change as needed

    results = analyze_first_move_performance(collection)

    # Sort by move position (0-8 for 3x3 board)
    sorted_moves = sorted(
        results.keys(), key=lambda x: x[0] if isinstance(x, tuple) else x)
    sorted_results = [results[move] for move in sorted_moves]
    move_labels = [f"Pos {move[0]}" if isinstance(move, tuple) else f"Pos {
        move}" for move in sorted_moves]

    # Create bar plot
    plt.figure(figsize=(12, 6))
    colors = ['green' if x > 0 else 'red' if x <
              0 else 'gray' for x in sorted_results]
    bars = plt.bar(move_labels, sorted_results, color=colors, alpha=0.7)

    plt.xlabel('Starting Move Position', fontsize=12)
    plt.ylabel('Wins - Losses (Player 1)', fontsize=12)
    plt.title('Player 1 Win-Loss Difference by Starting Move', fontsize=14)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.grid(True, alpha=0.3)

    for bar, value in zip(bars, sorted_results):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + (0.1 if height >= 0 else -0.3),
                 f'{value}', ha='center', va='bottom' if height >= 0 else 'top')

    plt.tight_layout()
    plt.savefig('plots/first_move_win_loss_diff.png',
                dpi=300, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["TicTacToe"]
        main()
