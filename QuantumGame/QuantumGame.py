from QBoard import QBoard
from Board import Board
from collections import defaultdict
import random

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
        # print("\nCycle detected! Quantum collapse needed.")
        # print("\nAvailable particles to observe:")
        position_particles = {}
        cycle_positions = set(pos for pos, _, _ in cycle_info)
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
        options = []
        for pos in sorted(position_particles.keys()):
            # print(f"\nPosition {pos}:")
            for subscript, creation, player in sorted(position_particles[pos]):
                option_id = len(options)
                options.append((pos, subscript, creation))
                # print(f"{option_id}: Player {player}'s {subscript}[{creation}]")
        # The player who did NOT close the cycle chooses the collapse
        chooser_player = 3 - self.current_player
        if not options:
            # print("No available particles to observe.")
            return False
        
        if len(options) == 1:
            choice = 0
        else:
            choice = random.randint(0, 1)
        
        chosen_pos, chosen_subscript, chosen_creation = options[choice]
        # print(f"[BOT] Randomly selected particle {choice}: Position {chosen_pos}, Subscript {chosen_subscript}, Creation {chosen_creation} for collapse.")
        return self.resolve_collapse(cycle_info, chosen_pos, chosen_subscript, chosen_creation)

    def handle_quantum_chain_reaction(self, pos, sub, exists, nonexist, to_process, player):
        if pos in exists or pos in nonexist:
            return
        exists[pos] = (sub, player)
        # print(f"→ Position {pos} exists for Player {player} (Move {sub})")
        for pair_pos, pair_sub in self.pairs[pos]:
            if pair_pos not in nonexist:
                nonexist.add(pair_pos)
                # print(f"→ Position {pair_pos} cannot exist (paired with {pos} in Move {pair_sub})")
                self.handle_nonexistence(pair_pos, exists, nonexist, to_process)
        for shared_pos, shared_sub in self.shares_square[pos]:
            if shared_pos not in nonexist:
                nonexist.add(shared_pos)
                # print(f"→ Position {shared_pos} cannot exist (shares square with {pos})")
                self.handle_nonexistence(shared_pos, exists, nonexist, to_process)

    def handle_nonexistence(self, pos, exists, nonexist, to_process):
        for pair_pos, pair_sub in self.pairs[pos]:
            if pair_pos not in exists and pair_pos not in nonexist:
                player = 1 if pair_sub % 2 == 1 else 2
                to_process.append((pair_pos, pair_sub))
                # print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {pos})")
        for shared_pos, shared_sub in self.shares_square[pos]:
            if shared_pos not in exists and shared_pos not in nonexist:
                nonexist.add(shared_pos)
                # print(f"→ Position {shared_pos} cannot exist (shares square with nonexistent {pos})")
                for pair_pos, pair_sub in self.pairs[shared_pos]:
                    if pair_pos not in exists and pair_pos not in nonexist:
                        player = 1 if pair_sub % 2 == 1 else 2
                        to_process.append((pair_pos, pair_sub))
                        # print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {shared_pos})")

    def handle_forced_implications(self, pos, exists, nonexist, to_process):
        for pair_pos, pair_sub in self.pairs[pos]:
            if pair_pos not in exists and pair_pos not in nonexist:
                player = 1 if pair_sub % 2 == 1 else 2
                to_process.append((pair_pos, pair_sub))
                # print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {pos})")
        for shared_pos, shared_sub in self.shares_square[pos]:
            if shared_pos not in exists and shared_pos not in nonexist:
                nonexist.add(shared_pos)
                # print(f"→ Position {shared_pos} cannot exist (shares square with nonexistent {pos})")
                for pair_pos, pair_sub in self.pairs[shared_pos]:
                    if pair_pos not in exists and pair_pos not in nonexist:
                        player = 1 if pair_sub % 2 == 1 else 2
                        to_process.append((pair_pos, pair_sub))
                        # print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {shared_pos})")

    def resolve_collapse(self, cycle_info, chosen_pos, chosen_subscript, chosen_creation):
        # This is the final, correct implementation of the collapse logic.

        # 1. Data setup: Get all particles on the board for easy lookup.
        all_particles = []
        for pos in range(1, 10):
            square = self.quantum_board.get_square(pos)
            for p in square.get_particle_list_copy():
                all_particles.append((pos, p.get_subscript(), p.get_creation_number()))
        
        sub_to_all_particles = defaultdict(list)
        for p in all_particles:
            sub_to_all_particles[p[1]].append(p)

        # 2. The collapse process
        observed = {}
        
        # A queue of positions that we know the final state of.
        # It stores tuples of (position, subscript) that are now classical facts.
        resolution_queue = [(chosen_pos, chosen_subscript)]
        resolved_positions = set()

        while resolution_queue:
            pos_to_set, sub_to_set = resolution_queue.pop(0)

            if pos_to_set in resolved_positions:
                continue

            # This position is now resolved. Record its state.
            player = 1 if sub_to_set % 2 == 1 else 2
            observed[pos_to_set] = (sub_to_set, player)
            resolved_positions.add(pos_to_set)

            # CONSEQUENCE: Find all other particles that were at this newly resolved position.
            # They are annihilated. Their entangled partners' positions must now resolve.
            for p_pos, p_sub, p_cr in all_particles:
                # If a different particle was also at this position...
                if p_pos == pos_to_set and p_sub != sub_to_set:
                    
                    # ...find its entangled partner.
                    pair = sub_to_all_particles.get(p_sub, [])
                    if len(pair) == 2:
                        p1, p2 = pair
                        other_particle = p2 if p1[0] == pos_to_set else p1
                        other_pos, other_sub, _ = other_particle
                        
                        # The partner's position is now forced to resolve. Add it to the queue.
                        if other_pos not in resolved_positions:
                            resolution_queue.append((other_pos, other_sub))

        # Apply the fully resolved collapse to the classical board.
        for pos, (sub, player) in observed.items():
            row, col = Board.convertNumPositionToIndex(pos)
            mark = 'X' if player == 1 else 'O'
            self.classical_board.set(row, col, mark)

        # Clear all affected particles from the quantum board.
        cleared_positions = set(observed.keys())
        for pos in cleared_positions:
            self.quantum_board.clear_position(pos)

        if self.classical_board.hasWinnerOrDraw():
            self.game_over = True
            game_status = self.classical_board.getGameStatus()
            self.winner = game_status.get("winner")
            return True
        return False

    def validate_move_position(self, position: int) -> bool:
        if not (1 <= position <= 9):
            # print("Position must be between 1 and 9!")
            return False
        row, col = Board.convertNumPositionToIndex(position)
        if not self.classical_board.get(row, col).isdigit():
            # print(f"Position {position} already collapsed! Choose another position.")
            return False
        return True

    def make_move(self, position1: int, position2: int):
        """
        Returns (valid, collapse_occurred):
            valid: True if the move was valid, False otherwise
            collapse_occurred: True if a collapse occurred on this move, False otherwise
        """
        try:
            if position1 == position2:
                return (False, False)
            if not self.validate_move_position(position1) or not self.validate_move_position(position2):
                return (False, False)
            self.quantum_board.add_player_move(position1, self.move_number, 1)
            self.quantum_board.add_player_move(position2, self.move_number, 2)
            self.pairs[position1].add((position2, self.move_number))
            self.pairs[position2].add((position1, self.move_number))
            for pos in [position1, position2]:
                square = self.quantum_board.get_square(pos)
                for particle in square.get_particle_list_copy():
                    if particle.get_subscript() != self.move_number:
                        other_pos = pos
                        self.shares_square[pos].add((other_pos, particle.get_subscript()))
                        self.shares_square[other_pos].add((pos, self.move_number))
            collapse = False
            if self.move_number >= 2:
                has_cycle, cycle_info = self.quantum_board.detect_cycle()
                if has_cycle:
                    if self.handle_collapse(cycle_info):
                        collapse = True
            self.current_player = 3 - self.current_player
            self.move_number += 1
            return (True, collapse)
        except ValueError as e:
            return (False, False)

    def display_game_state(self):
        # print(f"\nCurrent player: {self.current_player}")
        # print(f"Move number: {self.move_number}")
        # print("\nQuantum board state:")
        self.quantum_board.display_board()
        # print("\nClassical board state:")
        self.classical_board.displayBoard()
        # print("\nQuantum relationships:")
        self.quantum_board.print_relationships()

    def get_game_state(self):
        # Returns a string representation of the current game state.
        
        state = []
        state.append(f"Current player: {self.current_player}")
        state.append(f"Move number: {self.move_number}")
        state.append("\nQuantum board state:")
        state.append(self.quantum_board.get_board())  # Assuming QBoard has a method to return board as string
        state.append("\nClassical board state:")
        state.append(self.classical_board.getBoard())  # Assuming Board has a method to return board as string
        return "\n".join(state)


