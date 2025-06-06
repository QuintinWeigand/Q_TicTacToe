from pymongo import MongoClient
import matplotlib.pyplot as plt

def count_results(collection):
    player1_wins = 0
    player2_wins = 0
    draws = 0

    for record in collection.find():
        player1 = record.get("Player1", {})
        player2 = record.get("Player2", {})
        if player1.get("isWinner"):
            player1_wins += 1
        elif player2.get("isWinner"):
            player2_wins += 1
        else:
            draws += 1
    return player1_wins, player2_wins, draws

def main():
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client["TicTacToe"]
        collection = db["GameResults"]
        player1_wins, player2_wins, draws = count_results(collection)
        print(f"Player 1 Wins: {player1_wins}\nPlayer 2 Wins: {player2_wins}\nDraws: {draws}")
    except Exception as e:
        print(f"Error: {e}")

    labels = ["Player 1", "Draws", "Player 2"]
    values = [player1_wins, draws, player2_wins]

    plt.bar(labels, values)

    plt.xlabel("Outcome")
    plt.ylabel("Number of Games")
    plt.title("Tic-Tac-Toe Results Summary")

    plt.tight_layout()  # Add this line to fix cutoff issue
    plt.savefig("plots/wins.png")

if __name__ == "__main__":
    main()