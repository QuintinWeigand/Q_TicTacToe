from pymongo import MongoClient
import matplotlib.pyplot as plt

def main():
    query = {
        "$or": [
            {"Player1.isWinner": True},
            {"Player2.isWinner": True}
        ]
    }

    player1_wins = 0
    player2_wins = 0

    for record in collection.find(query):
        player1 = record.get("Player1")
        player2 = record.get("Player2")
        player1_winner_status = player1.get("isWinner")

        if player1_winner_status:
            player1_wins += 1
        else:
            player2_wins += 1

    # Set global font size for better visibility
    plt.rcParams.update({"font.size": 20})
    
    # Bar plot for wins
    labels = ['Player 1', 'Player 2']
    wins = [player1_wins, player2_wins]
    bars = plt.bar(labels, wins, color=['blue', 'orange'])
    plt.xlabel('Player', fontsize=20)
    plt.ylabel('Number of Wins', fontsize=20)
    plt.tight_layout()
    plt.bar_label(bars, padding=3, fontsize=18)
    
    plt.savefig("plots/total_wins_10M.png", dpi=300, bbox_inches='tight')
    
if __name__ == "__main__":
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["TicTacToe"]
        collection = db["QGameResults_1M"]
        main()