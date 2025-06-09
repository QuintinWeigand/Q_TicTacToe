from QBoard import QBoard

def main():
    board = QBoard()
    board.add_player_move(1, 1, 1)
    board.add_player_move(1,2,1)
    board.add_player_move(2,2,1)
    board.display_board()

if __name__ == "__main__":
    main()