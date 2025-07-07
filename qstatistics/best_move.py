from pymongo import MongoClient
from collections import Counter

client = MongoClient("mongodb://localhost:27017/")
db = client["TicTacToe"]
collection = db["QGameResults_10M"]

counter = Counter()

# Loop through all documents
for doc in collection.find({}, {"Player1.moves": 1}):
    moves = doc.get("Player1", {}).get("moves", [])
    if moves:
        first_move = moves[0]
        if isinstance(first_move, list) and len(first_move) == 2:
            counter[tuple(first_move)] += 1

# Find the most common tuple
if counter:
    most_common_tuple, count = counter.most_common(1)[0]
    print("Most common first move for Player 1:", most_common_tuple)
    print("Count:", count)
else:
    print("No Player 1 moves found.")
