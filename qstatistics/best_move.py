from pymongo import MongoClient
from collections import Counter

client = MongoClient("mongodb://localhost:27017/")
db = client["TicTacToe"]
collection = db["QGameResults"]

counter = Counter()

# Loop through all documents
for doc in collection.find({}, {"Player1.moves": 1, "Player2.moves": 1}):
    for player_key in ["Player1", "Player2"]:
        moves = doc.get(player_key, {}).get("moves", [])
        for move in moves:
            if isinstance(move, list) and len(move) == 2:
                counter[tuple(move)] += 1

# Find the most common tuple
most_common_tuple, count = counter.most_common(1)[0]
print("Most common tuple:", most_common_tuple)
print("Count:", count)
