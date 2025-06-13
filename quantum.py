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

    def handle_collapse(self, cycle_info) -> bool:
        """
        Handle the quantum collapse by letting the current player choose a position.
        Returns True if collapse was successful and led to a win, False otherwise.
        """
        print("\nCycle detected! Quantum collapse needed.")
        print("\nCycle positions (Position: Player):")
        valid_positions = {}
        
        # Show available positions and store their details
        for pos, subscript, creation in cycle_info:
            player = 1 if subscript % 2 == 1 else 2
            print(f"Position {pos}: Player {player}")
            valid_positions[pos] = player

        while True:
            try:
                choice = int(input(f"\nPlayer {self.current_player}, choose a position to collapse: "))
                if choice not in valid_positions:
                    print("Invalid position! Choose from the positions in the cycle.")
                    continue
                
                # Convert to row, col for classical board
                row, col = Board.convertNumPositionToIndex(choice)
                mark = 'X' if valid_positions[choice] == 1 else 'O'
                
                # Update classical board with the collapsed state
                if self.classical_board.set(row, col, mark):
                    print(f"\nPosition {choice} collapsed to Player {valid_positions[choice]}")
                    
                    # Check if this collapse led to a win
                    if self.classical_board.hasWinnerOrDraw():
                        self.game_over = True
                        game_status = self.classical_board.getGameStatus()
                        self.winner = game_status.get("winner")
                        print(f"\nGame Over! {self.winner} wins!")
                        return True
                    return False
                else:
                    print("Position already collapsed! Choose another position.")
                    continue
                    
            except ValueError:
                print("Invalid input! Please enter a number.")

    def validate_move_position(self, position: int) -> bool:
        """
        Check if a move position is valid (not collapsed and within bounds)
        """
        if not (1 <= position <= 9):
            print("Position must be between 1 and 9!")
            return False
            
        row, col = Board.convertNumPositionToIndex(position)
        if not self.classical_board.get(row, col).isdigit():
            print(f"Position {position} already collapsed! Choose another position.")
            return False
            
        return True

    def make_move(self, position1: int, position2: int) -> bool:
        """
        Attempt to make a move by placing particles in two different positions (quantum superposition).
        Each move has:
        - Same move_number (subscript) for both positions
        - Different creation_numbers (1 and 2) to distinguish the two parts of the superposition
        Returns True if the move was successful, False otherwise.
        """
        try:
            # Validate positions
            if position1 == position2:
                print("Must choose two different positions for quantum superposition!")
                return False
                
            if not self.validate_move_position(position1) or not self.validate_move_position(position2):
                return False

            # Add the particles - same move number, different creation numbers
            self.quantum_board.add_player_move(position1, self.move_number, 1)  # First position gets creation number 1
            self.quantum_board.add_player_move(position2, self.move_number, 2)  # Second position gets creation number 2
            
            # Only check for cycles after two complete moves
            if self.move_number >= 2:
                has_cycle, cycle_info = self.quantum_board.detect_cycle()
                if has_cycle:
                    if self.handle_collapse(cycle_info):
                        return True  # Game is over after collapse
            
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
    
    while not game.game_over:
        game.display_game_state()
        try:
            print(f"\nPlayer {game.current_player}'s turn")
            print("Enter two different positions (1-9) for quantum superposition")
            pos1 = int(input("First position: "))
            pos2 = int(input("Second position: "))
            
            if game.make_move(pos1, pos2):
                print("Move successful!")
            else:
                print("Move failed! Try again.")
                
        except ValueError:
            print("Invalid input! Please enter numbers between 1 and 9.")

    print("\nFinal game state:")
    game.display_game_state()

if __name__ == "__main__":
    main()