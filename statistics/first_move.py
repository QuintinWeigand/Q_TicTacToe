from pymongo import MongoClient
import matplotlib.pyplot as plt

def count_first_move(collection):
    corners_played = 0
    edges_played = 0
    center_played = 0
    
    valid_corners = [1,3,5,9]
    valid_edges = [2,4,6,8]

    for record in collection.find():
        player1 = record.get("Player1")
        
        if player1 == None:
            raise ValueError("Player 1 statistics could not be found")
        
        moves = player1.get("moves")

        if moves == None:
            raise ValueError("Player 1 moves could not be found")
        
        if player1.get("isWinner") == True:
            if moves[0] in valid_corners:
                corners_played += 1
            elif moves[0] in valid_edges:
                edges_played += 1
            else:
                center_played += 1
    
    return corners_played, edges_played, center_played

def main():
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client["TicTacToe"]
        collection = db["GameResults"]
        played_corners, played_edges, played_center = count_first_move(collection)
    except Exception as e:
        raise RuntimeError(f"Error: {e}")

    # Plotting the bar graph
    labels = ['Corners', 'Edges', 'Center']
    values = [played_corners, played_edges, played_center]

    plt.bar(labels, values, color=['blue', 'orange', 'green'])
    plt.xlabel('First Move Position')
    plt.ylabel('Number of Wins')
    plt.title('Winning First Moves: Corners vs Edges vs Center')
    plt.tight_layout()

    bars = plt.bar(labels, values, color=['blue', 'orange', 'green'])
    plt.bar_label(bars, padding=3)

    plt.savefig("plots/first_win_move.png")

if __name__ == "__main__":
    main()