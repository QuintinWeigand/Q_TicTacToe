from pymongo import MongoClient
import matplotlib.pyplot as plt

def main():
    move_dict = {}
    for doc in collection.find():
        player1 = doc.get("Player1")
        player2 = doc.get("Player2")
        player1_moves = player1.get("moves")
        player2_moves = player2.get("moves")
        board = doc.get("Board")
        size = len(player1_moves) + len(player2_moves)

        if size == 4:
            print("Player1: ", player1_moves)
            print("Player2: ", player2_moves)
            print(board)
            print("---------------")
            

        if size in move_dict:
            move_dict[size] += 1
        else:
            move_dict[size] = 1

    sorted_move_dict = dict(sorted(move_dict.items()))
    
    moves = list(sorted_move_dict.keys())
    counts = list(sorted_move_dict.values())

    # Set global font size for better visibility
    plt.rcParams.update({"font.size": 20})
    
    bars = plt.bar(moves, counts, color="maroon")
    plt.xlabel("Number of Moves", fontsize=20)
    plt.ylabel("Number of Games", fontsize=20)
    plt.bar_label(bars, padding=3, fontsize=18)
    
    plt.savefig("plots/num_moves_10M.png", dpi=300, bbox_inches='tight')
    

if __name__ == "__main__":
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["TicTacToe"]
        collection = db["QGameResults_10M"]
        main()