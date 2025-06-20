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
        print("\nCycle detected! Quantum collapse needed.")
        print("\nAvailable particles to observe:")
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
            print(f"\nPosition {pos}:")
            for subscript, creation, player in sorted(position_particles[pos]):
                option_id = len(options)
                options.append((pos, subscript, creation))
                print(f"{option_id}: Player {player}'s {subscript}[{creation}]")
        while True:
            print(f"\nPlayer {self.current_player}, enter the number of the particle you want to observe.")
            print(f"Valid choices: {', '.join(str(i) for i in range(len(options)))}")
            choice_raw = input("Your choice: ")
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
            chosen_pos, chosen_subscript, chosen_creation = options[choice]
            return self.resolve_collapse(cycle_info, chosen_pos, chosen_subscript, chosen_creation)

    def handle_quantum_chain_reaction(self, pos, sub, exists, nonexist, to_process, player):
        if pos in exists or pos in nonexist:
            return
        exists[pos] = (sub, player)
        print(f"→ Position {pos} exists for Player {player} (Move {sub})")
        for pair_pos, pair_sub in self.pairs[pos]:
            if pair_pos not in nonexist:
                nonexist.add(pair_pos)
                print(f"→ Position {pair_pos} cannot exist (paired with {pos} in Move {pair_sub})")
                self.handle_nonexistence(pair_pos, exists, nonexist, to_process)
        for shared_pos, shared_sub in self.shares_square[pos]:
            if shared_pos not in nonexist:
                nonexist.add(shared_pos)
                print(f"→ Position {shared_pos} cannot exist (shares square with {pos})")
                self.handle_nonexistence(shared_pos, exists, nonexist, to_process)

    def handle_nonexistence(self, pos, exists, nonexist, to_process):
        for pair_pos, pair_sub in self.pairs[pos]:
            if pair_pos not in exists and pair_pos not in nonexist:
                player = 1 if pair_sub % 2 == 1 else 2
                to_process.append((pair_pos, pair_sub))
                print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {pos})")
        for shared_pos, shared_sub in self.shares_square[pos]:
            if shared_pos not in exists and shared_pos not in nonexist:
                nonexist.add(shared_pos)
                print(f"→ Position {shared_pos} cannot exist (shares square with nonexistent {pos})")
                for pair_pos, pair_sub in self.pairs[shared_pos]:
                    if pair_pos not in exists and pair_pos not in nonexist:
                        player = 1 if pair_sub % 2 == 1 else 2
                        to_process.append((pair_pos, pair_sub))
                        print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {shared_pos})")

    def handle_forced_implications(self, pos, exists, nonexist, to_process):
        for pair_pos, pair_sub in self.pairs[pos]:
            if pair_pos not in exists and pair_pos not in nonexist:
                player = 1 if pair_sub % 2 == 1 else 2
                to_process.append((pair_pos, pair_sub))
                print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {pos})")
        for shared_pos, shared_sub in self.shares_square[pos]:
            if shared_pos not in exists and shared_pos not in nonexist:
                nonexist.add(shared_pos)
                print(f"→ Position {shared_pos} cannot exist (shares square with nonexistent {pos})")
                for pair_pos, pair_sub in self.pairs[shared_pos]:
                    if pair_pos not in exists and pair_pos not in nonexist:
                        player = 1 if pair_sub % 2 == 1 else 2
                        to_process.append((pair_pos, pair_sub))
                        print(f"→ Must process: Position {pair_pos} (Move {pair_sub}, forced by {shared_pos})")

    def resolve_collapse(self, cycle_info, chosen_pos, chosen_subscript, chosen_creation):
        print("\nEMERGENCY QUANTUM COLLAPSE RESOLUTION...")
        print(f"Observing particle {chosen_subscript}[{chosen_creation}] at position {chosen_pos}")
        all_particles = []
        for pos in range(1, 10):
            square = self.quantum_board.get_square(pos)
            for p in square.get_particle_list_copy():
                sub = p.get_subscript()
                cr = p.get_creation_number()
                all_particles.append((pos, sub, cr))
        from collections import defaultdict, deque
        sub_to_particles = defaultdict(list)
        for pos, sub, cr in all_particles:
            sub_to_particles[sub].append((pos, cr))
        particle_pairs = {}
        for sub, particles in sub_to_particles.items():
            if len(particles) == 2:
                (pos1, cr1), (pos2, cr2) = particles
                particle_pairs[(sub, cr1)] = (pos2, cr2)
                particle_pairs[(sub, cr2)] = (pos1, cr1)
        observed = {}
        eliminated_particles = set()
        to_observe = deque([(chosen_pos, chosen_subscript, chosen_creation)])
        while to_observe:
            pos, sub, cr = to_observe.popleft()
            if pos in observed:
                continue
            observed[pos] = (sub, 1 if sub % 2 == 1 else 2)
            print(f"→ Position {pos} exists for Player {observed[pos][1]} (Move {sub}[{cr}])")
            if (sub, cr) in particle_pairs:
                pair_pos, pair_cr = particle_pairs[(sub, cr)]
                eliminated_particles.add((pair_pos, sub, pair_cr))
                print(f"→ Eliminating pair at position {pair_pos} (Move {sub}[{pair_cr}])")
                checked = set()
                while True:
                    forced = []
                    for check_pos in range(1, 10):
                        if check_pos in observed or check_pos in checked:
                            continue
                        square_particles = [(s, c) for p, s, c in all_particles if p == check_pos and (p, s, c) not in eliminated_particles]
                        if len(square_particles) == 1:
                            s2, c2 = square_particles[0]
                            forced.append((check_pos, s2, c2))
                    if not forced:
                        break
                    for fpos, fsub, fcr in forced:
                        if fpos not in observed:
                            to_observe.append((fpos, fsub, fcr))
                            checked.add(fpos)
        while True:
            forced = []
            for pos in range(1, 10):
                if pos in observed:
                    continue
                square_particles = [(sub, cr) for p, sub, cr in all_particles if p == pos and (p, sub, cr) not in eliminated_particles]
                if len(square_particles) == 1:
                    sub, cr = square_particles[0]
                    forced.append((pos, sub, cr))
            if not forced:
                break
            for pos, sub, cr in forced:
                if pos in observed:
                    continue
                observed[pos] = (sub, 1 if sub % 2 == 1 else 2)
                print(f"→ Position {pos} must exist for Player {observed[pos][1]} (Move {sub}[{cr}])")
                if (sub, cr) in particle_pairs:
                    pair_pos, pair_cr = particle_pairs[(sub, cr)]
                    eliminated_particles.add((pair_pos, sub, pair_cr))
                    print(f"→ Eliminating pair at position {pair_pos} (Move {sub}[{pair_cr}])")
        print("\nApplying quantum collapse...")
        for pos, (sub, player) in observed.items():
            row, col = Board.convertNumPositionToIndex(pos)
            mark = 'X' if player == 1 else 'O'
            if self.classical_board.set(row, col, mark):
                print(f"→ Position {pos} collapsed to Player {player}'s {mark}")
        cleared_positions = set(observed.keys()) | set(p for p, _, _ in eliminated_particles)
        for pos in cleared_positions:
            self.quantum_board.clear_position(pos)
            self.pairs.pop(pos, None)
            self.shares_square.pop(pos, None)
        for pos in self.pairs:
            self.pairs[pos] = {(p, s) for p, s in self.pairs[pos] if p not in cleared_positions}
        for pos in self.shares_square:
            self.shares_square[pos] = {(p, s) for p, s in self.shares_square[pos] if p not in cleared_positions}
        print("\nQuantum collapse complete!")
        print("Realized positions:", ", ".join(f"{pos}→P{observed[pos][1]}" for pos in sorted(observed.keys())))
        print("Eliminated positions:", ", ".join(str(pos) for pos, _, _ in eliminated_particles))
        if self.classical_board.hasWinnerOrDraw():
            self.game_over = True
            game_status = self.classical_board.getGameStatus()
            self.winner = game_status.get("winner")
            print(f"\nGame Over! {self.winner} wins!")
            return True
        return False

    def validate_move_position(self, position: int) -> bool:
        if not (1 <= position <= 9):
            print("Position must be between 1 and 9!")
            return False
        row, col = Board.convertNumPositionToIndex(position)
        if not self.classical_board.get(row, col).isdigit():
            print(f"Position {position} already collapsed! Choose another position.")
            return False
        return True

    def make_move(self, position1: int, position2: int) -> bool:
        try:
            if position1 == position2:
                print("Must choose two different positions for quantum superposition!")
                return False
            if not self.validate_move_position(position1) or not self.validate_move_position(position2):
                return False
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
            if self.move_number >= 2:
                has_cycle, cycle_info = self.quantum_board.detect_cycle()
                if has_cycle:
                    if self.handle_collapse(cycle_info):
                        return True
            self.current_player = 3 - self.current_player
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
