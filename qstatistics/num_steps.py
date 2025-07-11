import matplotlib.pyplot as plt
from pymongo import MongoClient

def main():
    query = {
        "$or": [
            {"Player1.isWinner": True},
            {"Player2.isWinner": True}
        ]
    }

    counter = {}

    for document in collection.find(query):
        player1 = document.get("Player1")
        player1_moves = player1.get("moves")
        player2 = document.get("Player2")
        player2_moves = player2.get("moves")

        total_moves = len(player1_moves) + len(player2_moves)

        if total_moves in counter:
            counter[total_moves] += 1
        else:
            counter[total_moves] = 1

        if total_moves == 3:
            print(player1_moves)
            print(player2_moves)
            print(document["Board"])

    keys = list(counter.keys())
    values = list(counter.values())

    bars = plt.bar(keys, values)
    plt.xlabel('Total Moves')
    plt.ylabel('Number of Games')
    plt.title('Distribution of Total Moves in Games - 10M')
    plt.tight_layout()

    plt.bar_label(bars, padding=3)
    
    plt.savefig("plots/num_steps_10M.png")


if __name__ == "__main__":
    with MongoClient("mongodb://localhost:27017") as client:
        database = client["TicTacToe"]
        collection = database["QGameResults_10M"]
        main()