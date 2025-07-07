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

    # Bar plot for wins
    labels = ['Player 1', 'Player 2']
    wins = [player1_wins, player2_wins]
    bars = plt.bar(labels, wins, color=['blue', 'orange'])
    plt.xlabel('Player')
    plt.ylabel('Number of Wins')
    plt.title('Total Wins by Player - 1M')
    plt.tight_layout()
    plt.bar_label(bars, padding=3)
    
    plt.savefig("plots/total_wins_1M.png")
    
if __name__ == "__main__":
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["TicTacToe"]
        collection = db["QGameResults_1M"]
        main()