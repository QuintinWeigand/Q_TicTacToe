from QBoardSquare import QBoardSquare
from QParticle import QParticle

# TODO: QBoard will handle the detecting cycles using recursion going through each square finding same subscript particles

class QBoard:
    def __init__(self):
        self.__q_board = [QBoardSquare(i + 1) for i in range(9)]

    def display_board(self):
        for i in range(len(self.__q_board)):
            square = self.__q_board[i]
            particles = square.get_particle_list_copy()
            # Show only subscripts in the display
            display_str = ' '.join(str(p.get_subscript()) for p in particles) if particles else '-'
            print(f"{i + 1} | {display_str}")

    def add_player_move(self, board_position: int, move_number: int, creation_number: int):
        if board_position >= 1 and board_position <= 9:
            particle = QParticle(move_number, creation_number)
            self.__q_board[board_position - 1].add_particle(particle)
        else: 
            raise ValueError("Incorrect board position")
        
    # TODO: Stub method for now, find cycles in the board (recursion?)
    def detect_cycle(self) -> tuple[bool, list]:
        """
        Detect if there are any cycles in the quantum board.
        Returns: (bool, list) - (whether cycle exists, list of (position, subscript) in cycle)
        """
        # Build adjacency list for each square
        adjacency = {}
        particle_info = {}  # Store creation numbers for each node
        for pos1, square1 in enumerate(self.__q_board, 1):
            for particle1 in square1.get_particle_list_copy():
                key1 = (pos1, particle1.get_subscript())
                if key1 not in adjacency:
                    adjacency[key1] = set()
                    particle_info[key1] = particle1.get_creation_number()
                
                # Find all related particles
                for pos2, square2 in enumerate(self.__q_board, 1):
                    if pos1 != pos2:  # Don't check same square
                        for particle2 in square2.get_particle_list_copy():
                            if (particle1.get_subscript() == particle2.get_subscript() and
                                particle1.get_creation_number() != particle2.get_creation_number()):
                                key2 = (pos2, particle2.get_subscript())
                                adjacency[key1].add(key2)
                                particle_info[key2] = particle2.get_creation_number()
        
        # Function to check for cycles using DFS
        def find_cycle(node, visited, rec_stack, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in adjacency.get(node, []):
                if neighbor in rec_stack:
                    # Found a cycle! Build complete cycle starting from first occurrence
                    cycle = []
                    seen = set()
                    current = neighbor
                    while True:
                        if (current[0], current[1]) in seen and len(cycle) > 0:
                            break
                        cycle.append((current[0], current[1], particle_info[current]))
                        seen.add((current[0], current[1]))
                        # Find next node that hasn't been seen
                        for next_node in adjacency[current]:
                            if (next_node[0], next_node[1]) not in seen:
                                current = next_node
                                break
                    return cycle
                elif neighbor not in visited:
                    result = find_cycle(neighbor, visited, rec_stack, path)
                    if result:
                        return result
            
            path.pop()
            rec_stack.remove(node)
            return None
            
            path.pop()
            rec_stack.remove(node)
            return None
        
        # Check each node for cycles
        visited = set()
        for node in adjacency:
            if node not in visited:
                rec_stack = set()
                path = []
                cycle = find_cycle(node, visited, rec_stack, path)
                if cycle:
                    return True, cycle
        
        return False, []

    def print_relationships(self):
        """Print all relationships between particles with the same subscript."""
        # Keep track of relationships we've already seen
        seen_relationships = set()

        def add_relationship(pos1, particle1, pos2, particle2):
            # Create a sorted tuple of positions and particles to ensure we catch both directions
            relationship = tuple(sorted([(pos1, str(particle1)), (pos2, str(particle2))]))
            if relationship not in seen_relationships:
                seen_relationships.add(relationship)
                print(f"{particle1.get_subscript()}[{pos1}] -> {particle2.get_subscript()}[{pos2}]")

        def find_related_particles(particle, current_square, visited_squares=None):
            if visited_squares is None:
                visited_squares = set()
            
            subscript = particle.get_subscript()
            current_pos = current_square.get_square_num()
            visited_squares.add(current_pos)
            
            # Find all related particles in other squares
            for square_num, square in enumerate(self.__q_board, 1):
                if square_num not in visited_squares:
                    for other_particle in square.get_particle_list_copy():
                        if (other_particle.get_subscript() == subscript and 
                            other_particle.get_creation_number() != particle.get_creation_number()):
                            add_relationship(current_pos, particle, square_num, other_particle)
                            # Recursively find relationships for the related particle
                            find_related_particles(other_particle, square, visited_squares)

        # Search through each square and particle
        visited_pairs = set()  # To avoid processing the same starting point twice
        for square_num, square in enumerate(self.__q_board, 1):
            for particle in square.get_particle_list_copy():
                pair_key = (square_num, particle.get_subscript())
                if pair_key not in visited_pairs:
                    visited_pairs.add(pair_key)
                    find_related_particles(particle, square)