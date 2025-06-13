from QBoard import QBoard
from Board import Board

class QuantumGame:
    def __init__(self):
        self.quantum_board = QBoard()
        self.classical_board = Board()  # Tracks collapsed/observed reality
        self.current_player = 1
        self.move_number = 1
        self.game_over = False
        self.winner = None

    def make_move(self, position: int) -> bool:
        """
        Attempt to make a move at the given position.
        Returns True if the move was successful, False otherwise.
        """
        try:
            # Add the particle with current move number for current player
            self.quantum_board.add_player_move(position, self.move_number, self.current_player)
            
            # Check for cycles after move
            has_cycle, cycle_info = self.quantum_board.detect_cycle()
            if has_cycle:
                print("\nCycle detected! Quantum collapse needed.")
                print("Cycle details:")
                for pos, subscript, creation in cycle_info:
                    print(f"Position {pos} (Player {creation})")
                
                # For now, we'll collapse the first position in the cycle
                # TODO: Add logic to let players choose collapse position
                collapse_pos = cycle_info[0][0]
                collapse_player = cycle_info[0][2]
                
                # Convert to row, col for classical board
                row, col = Board.convertNumPositionToIndex(collapse_pos)
                mark = 'X' if collapse_player == 1 else 'O'
                
                # Update classical board with the collapsed state
                if self.classical_board.set(row, col, mark):
                    print(f"\nPosition {collapse_pos} collapsed to Player {collapse_player}")
                    
                    # Check if this collapse led to a win
                    if self.classical_board.hasWinnerOrDraw():
                        self.game_over = True
                        game_status = self.classical_board.getGameStatus()
                        self.winner = game_status.get("winner")
                        print(f"\nGame Over! {self.winner} wins!")
                        return True
            
            # Switch players if game isn't over
            self.current_player = 3 - self.current_player  # Switches between 1 and 2
            self.move_number += 1
            return True
            
        except ValueError as e:
            print(f"Invalid move: {e}")
            return False

    def display_game_state(self):
        print(f"\nCurrent player: {self.current_player}")
        print(f"Move number: {self.move_number}")
        print("\nQuantum board state:")
        self.quantum_board.display_board()
        print("\nClassical board state:")
        self.classical_board.displayBoard()
        print("\nQuantum relationships:")
        self.quantum_board.print_relationships()

def main():
    game = QuantumGame()
    
    # Test moves that should create a cycle and collapse
    moves = [
        (1, 1),  # Player 1 -> pos 1
        (2, 2),  # Player 2 -> pos 2
        (2, 1),  # Player 1 -> pos 2 (creates relationship with pos 2)
        (3, 2),  # Player 2 -> pos 3
        (3, 1),  # Player 1 -> pos 3 (creates relationship with pos 3)
        (1, 2)   # Player 2 -> pos 1 (should create cycle)
    ]
    
    for pos, expected_player in moves:
        if game.game_over:
            print("\nGame is already over!")
            break
            
        print(f"\nPlayer {expected_player} moving to position {pos}")
        if game.make_move(pos):
            game.display_game_state()
        else:
            print(f"Move to position {pos} failed!")

if __name__ == "__main__":
    main()