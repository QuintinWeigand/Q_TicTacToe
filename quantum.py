from QBoard import QBoard

def main():
    board = QBoard()
    
    board.add_player_move(1, 1, 1)
    board.add_player_move(2, 1, 2)
    
    board.add_player_move(2, 2, 1)
    board.add_player_move(3, 2, 2)
    
    board.add_player_move(3, 1, 1)
    board.add_player_move(1, 1, 2)

    print("Current board state:")
    board.display_board()
    print("\nRelationships between particles:")
    board.print_relationships()
    print("\nChecking for cycles...")
    has_cycle, cycle_info = board.detect_cycle()
    print(f"Cycle detected: {has_cycle}")
    if has_cycle:
        print("\nCycle detected with subscript", cycle_info[0][1])
        print("\nCycle path:")
        for i, (pos, subscript, creation) in enumerate(cycle_info):
            next_pos = cycle_info[(i + 1) % len(cycle_info)][0]
            print(f"Position {pos} -> {next_pos}")

if __name__ == "__main__":
    main()