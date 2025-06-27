import matplotlib.pyplot as plt
from pymongo import MongoClient
import time

def main():
    query = {
        "$or": [
            {"Player1.isWinner": True},
            {"Player2.isWinner": True}
        ]
    }

    steps_dict = {}

    for record in collection.find(query):
        collapse_move_info = record.get("Collapse Move Info")
        collapse_num = len(collapse_move_info)

        if collapse_num in steps_dict:
            steps_dict[collapse_num] += 1
        else:
            steps_dict[collapse_num] = 12
    
    print("Collapse count dictionary: ")
    print(steps_dict)

if __name__ == "__main__":
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["TicTacToe"]
        collection = db["QGameResults"]
        main()