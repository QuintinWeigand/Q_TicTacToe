from QBoard import QBoard
from Board import Board
from collections import defaultdict

class QuantumGame:
    def __init__(self):
        self.quantum_board = QBoard()
        self.classical_board = Board()
        self.current_player = 1
        self.move_number = 1
        self.game_over = False
        self.winner = None
        # Persistent quantum relationship tracking
        self.pairs = defaultdict(set)          # pos -> set of (other_pos, subscript) that are paired
        self.shares_square = defaultdict(set)  # pos -> set of (other_pos, subscript) that share the square

    def handle_collapse(self, cycle_info) -> bool:
        
        # Handle the quantum collapse by letting the current player choose a specific particle to observe.
        # Returns True if collapse was successful and led to a win, False otherwise.
        
        print("\nCycle detected! Quantum collapse needed.")
        print("\nAvailable particles to observe:")
        
        # Group particles by position and show options
        position_particles = {}
        # Get all particles in each position from the quantum board
        for pos in range(1, 10):
            square = self.quantum_board.get_square(pos)
            particles = square.get_particle_list_copy()
            if particles:
                position_particles[pos] = []
                for particle in particles:
                    subscript = particle.get_subscript()
                    creation = particle.get_creation_number()
                    player = 1 if subscript % 2 == 1 else 2
                    position_particles[pos].append((subscript, creation, player))
        
        # Display options with unique identifiers
        options = []
        for pos in sorted(position_particles.keys()):
            print(f"\nPosition {pos}:")
            for subscript, creation, player in sorted(position_particles[pos]):
                option_id = len(options)
                options.append((pos, subscript, creation))
                print(f"{option_id}: Player {player}'s {subscript}[{creation}]")
        
        while True:
            print(f"\nPlayer {self.current_player}, enter the number of the particle you want to observe.")
            print(f"Valid choices: {', '.join(str(i) for i in range(len(options)))}")
            choice_raw = input("Your choice: ")
            
            # Validate input
            choice_clean = choice_raw.strip()
            if not choice_clean:
                print("Empty input. Please enter a number.")
                continue
                
            if not choice_clean.isdigit():
                print("Invalid input. Please enter a number.")
                continue
                
            choice = int(choice_clean)
            if not (0 <= choice < len(options)):
                print(f"Invalid choice. Please choose from: {', '.join(str(i) for i in range(len(options)))}")
                continue
                
            # Valid choice - get the selected particle info
            chosen_pos, chosen_subscript, chosen_creation = options[choice]
            return self.resolve_collapse(cycle_info, chosen_pos, chosen_subscript, chosen_creation)

    def handle_quantum_chain_reaction(self, pos, sub, exists, nonexist, to_process, player):
        
        # Handle the complete chain reaction of a quantum collapse,
        # ensuring ALL implications are properly processed.
        
        if pos in exists or pos in nonexist:
            return
            
        # Make this position exist
        exists[pos] = (sub, player)
        print(f"→ Position {pos} exists for Player {player} (Move {sub})")
        
        # Process quantum pairs (same move)
        for pair_pos, pair_sub in self.pairs[pos]:
            if pair_pos not in nonexist:
                nonexist.add(pair_pos)
                print(f"→ Position {pair_pos} cannot exist (paired with {pos} in Move {pair_sub})")
                # Force quantum implications
                self.handle_nonexistence(pair_pos, exists, nonexist, to_process)
        
        # Process shared squares
        for shared_pos, shared_sub in self.shares_square[pos]:
            if shared_pos not in nonexist:
                nonexist.add(shared_pos)
                print(f"→ Position {shared_pos} cannot exist (shares square with {pos})")
                # Force quantum implications
                self.handle_nonexistence(shared_pos, exists, nonexist, to_process)

    def handle_nonexistence(self, pos, exists, nonexist, to_process):
        
        # Handle all implications of a position becoming non-existent.
        
        # Force pairs to exist
        for pair_pos, pair_sub in self.pairs[pos]:
            if pair_pos not in exists and pair_pos not in nonexist:
                player = 1 if pair_sub % 2 == 1 else 2
                to_process.append((pair_pos, pair_sub))
                print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {pos})")
        
        # Affect shared squares
        for shared_pos, shared_sub in self.shares_square[pos]:
            if shared_pos not in exists and shared_pos not in nonexist:
                nonexist.add(shared_pos)
                print(f"→ Position {shared_pos} cannot exist (shares square with nonexistent {pos})")
                # Process their pairs too
                for pair_pos, pair_sub in self.pairs[shared_pos]:
                    if pair_pos not in exists and pair_pos not in nonexist:
                        player = 1 if pair_sub % 2 == 1 else 2
                        to_process.append((pair_pos, pair_sub))
                        print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {shared_pos})")

    def handle_forced_implications(self, pos, exists, nonexist, to_process):
        
        # Handle all implications of a position becoming non-existent.
        # Force pairs to exist and process shared square implications.
        
        # Force pairs to exist
        for pair_pos, pair_sub in self.pairs[pos]:
            if pair_pos not in exists and pair_pos not in nonexist:
                player = 1 if pair_sub % 2 == 1 else 2
                to_process.append((pair_pos, pair_sub))
                print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {pos})")
        
        # Process implications from shared squares
        for shared_pos, shared_sub in self.shares_square[pos]:
            if shared_pos not in exists and shared_pos not in nonexist:
                nonexist.add(shared_pos)
                print(f"→ Position {shared_pos} cannot exist (shares square with nonexistent {pos})")
                # Process their pairs too
                for pair_pos, pair_sub in self.pairs[shared_pos]:
                    if pair_pos not in exists and pair_pos not in nonexist:
                        player = 1 if pair_sub % 2 == 1 else 2
                        to_process.append((pair_pos, pair_sub))
                        print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {shared_pos})")

    def resolve_collapse(self, cycle_info, chosen_pos, chosen_subscript, chosen_creation):
        
        # Handles all entanglements and ensures proper propagation through the cycle!
        
        print("\nEMERGENCY QUANTUM COLLAPSE RESOLUTION...")
        print(f"Observing particle {chosen_subscript}[{chosen_creation}] at position {chosen_pos}")
        
        # Initialize quantum state
        exists = {}      # pos -> (subscript, player)
        nonexist = set() # positions that don't exist
        
        # Map particles to their positions and pair info
        particle_pairs = {}  # (sub, cr) -> (other_pos, other_cr)
        for pos, sub, cr in cycle_info:
            # Find its pair in the same move
            for other_pos, other_sub, other_cr in cycle_info:
                if pos != other_pos and sub == other_sub:
                    particle_pairs[(sub, cr)] = (other_pos, other_cr)
        
        # Start with the chosen particle
        exists[chosen_pos] = (chosen_subscript, 1 if chosen_subscript % 2 == 1 else 2)
        print(f"\nCollapse chain reaction:")
        print(f"→ Position {chosen_pos} exists for Player {1 if chosen_subscript % 2 == 1 else 2} (Move {chosen_subscript}[{chosen_creation}])")
        
        # Find and eliminate its pair
        if (chosen_subscript, chosen_creation) in particle_pairs:
            pair_pos, pair_cr = particle_pairs[(chosen_subscript, chosen_creation)]
            nonexist.add(pair_pos)
            print(f"→ Position {pair_pos} cannot contain {chosen_subscript}[{pair_cr}] (paired with chosen particle)")
        
        # Process implications until nothing changes
        changed = True
        while changed:
            changed = False
            
            # Check each position
            for pos in range(1, 10):
                if pos not in exists and pos not in nonexist:
                    square = self.quantum_board.get_square(pos)
                    valid_particles = []
                    
                    # Check each particle
                    for particle in square.get_particle_list_copy():
                        sub = particle.get_subscript()
                        cr = particle.get_creation_number()
                        
                        # A particle is valid if:
                        # 1. It hasn't been materialized elsewhere
                        # 2. Its pair isn't marked as nonexistent
                        if (sub, cr) in particle_pairs:
                            pair_pos, pair_cr = particle_pairs[(sub, cr)]
                            if pair_pos not in nonexist and not any(p == sub for p, _ in exists.values()):
                                valid_particles.append((sub, cr))
                    
                    # If exactly one valid particle remains, it must materialize
                    if len(valid_particles) == 1:
                        sub, cr = valid_particles[0]
                        player = 1 if sub % 2 == 1 else 2
                        exists[pos] = (sub, player)
                        print(f"→ Position {pos} must exist for Player {player} (Move {sub}[{cr}] - only valid particle)")
                        
                        # Its pair must be eliminated
                        if (sub, cr) in particle_pairs:
                            pair_pos, pair_cr = particle_pairs[(sub, cr)]
                            if pair_pos not in nonexist:
                                nonexist.add(pair_pos)
                                print(f"→ Position {pair_pos} cannot exist (contains pair {sub}[{pair_cr}])")
                        changed = True
                    
                    # If no valid particles remain, position is nonexistent
                    elif len(valid_particles) == 0 and pos not in nonexist:
                        nonexist.add(pos)
                        print(f"→ Position {pos} cannot exist (no valid particles)")
                        changed = True
        
        print("\nApplying quantum collapse...")
        for pos in sorted(exists.keys()):
            sub, player = exists[pos]
            row, col = Board.convertNumPositionToIndex(pos)
            mark = 'X' if player == 1 else 'O'
            if self.classical_board.set(row, col, mark):
                print(f"→ Position {pos} collapsed to Player {player}'s {mark}")
        
        # Clear quantum state and update relationships
        cleared_positions = exists.keys() | nonexist
        for pos in cleared_positions:
            self.quantum_board.clear_position(pos)
            # Clean up relationships
            self.pairs.pop(pos, None)
            self.shares_square.pop(pos, None)
        
        # Clean up references to cleared positions in remaining relationships
        for pos in self.pairs:
            self.pairs[pos] = {(p, s) for p, s in self.pairs[pos] if p not in cleared_positions}
        for pos in self.shares_square:
            self.shares_square[pos] = {(p, s) for p, s in self.shares_square[pos] if p not in cleared_positions}

        print("\nQuantum collapse complete!")
        print("Realized positions:", ", ".join(f"{pos}→P{exists[pos][1]}" for pos in sorted(exists.keys())))
        print("Non-existent positions:", ", ".join(str(pos) for pos in sorted(nonexist)))

        # Check for win
        if self.classical_board.hasWinnerOrDraw():
            self.game_over = True
            game_status = self.classical_board.getGameStatus()
            self.winner = game_status.get("winner")
            print(f"\nGame Over! {self.winner} wins!")
            return True
        
        return False

    def validate_move_position(self, position: int) -> bool:
        
        # Check if a move position is valid (not collapsed and within bounds)
        
        if not (1 <= position <= 9):
            print("Position must be between 1 and 9!")
            return False
            
        row, col = Board.convertNumPositionToIndex(position)
        if not self.classical_board.get(row, col).isdigit():
            print(f"Position {position} already collapsed! Choose another position.")
            return False
            
        return True

    def make_move(self, position1: int, position2: int) -> bool:
        
        # Attempt to make a move by placing particles in two different positions (quantum superposition).
        # Each move has:
        # - Same move_number (subscript) for both positions
        # - Different creation numbers (1 and 2) to distinguish the two parts of the superposition
        # Returns True if the move was successful, False otherwise.
        
        try:
            # Validate positions
            if position1 == position2:
                print("Must choose two different positions for quantum superposition!")
                return False
                
            if not self.validate_move_position(position1) or not self.validate_move_position(position2):
                return False

            # Add the particles - same move number, different creation numbers
            self.quantum_board.add_player_move(position1, self.move_number, 1)
            self.quantum_board.add_player_move(position2, self.move_number, 2)
            
            # Update quantum relationships
            # Add pair relationship
            self.pairs[position1].add((position2, self.move_number))
            self.pairs[position2].add((position1, self.move_number))
            
            # Update shared square relationships with existing particles
            for pos in [position1, position2]:
                square = self.quantum_board.get_square(pos)
                for particle in square.get_particle_list_copy():
                    if particle.get_subscript() != self.move_number:  # Different move
                        other_pos = pos  # Same position, different move
                        self.shares_square[pos].add((other_pos, particle.get_subscript()))
                        self.shares_square[other_pos].add((pos, self.move_number))
            
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