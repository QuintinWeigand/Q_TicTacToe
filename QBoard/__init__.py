from QBoardSquare import QBoardSquare
from QParticle import QParticle

class QBoard:
    def __init__(self):
        self.__q_board = [QBoardSquare(i + 1) for i in range(9)]

    def display_board(self):
        for i in range(len(self.__q_board)):
            square = self.__q_board[i]
            particles = square.get_particle_list_copy()
            # Show subscripts and creation numbers
            display_str = ' '.join(f"{p.get_subscript()}[{p.get_creation_number()}]" for p in particles) if particles else '-'
            print(f"{i + 1} | {display_str}")

    def add_player_move(self, board_position: int, move_number: int, creation_number: int):
        if board_position >= 1 and board_position <= 9:
            particle = QParticle(move_number, creation_number)
            self.__q_board[board_position - 1].add_particle(particle)
        else: 
            raise ValueError("Incorrect board position")
        
    def detect_cycle(self) -> tuple[bool, list]:
        
        # Detect cycles between particles from different moves that share squares.
        # Returns (bool, list): whether cycle exists, list of (position, subscript, creation) in cycle
        
        # Build adjacency list for each square and its subscripts
        square_subscripts = {}  # Maps square -> set of subscripts in that square
        adjacency = {}  # Maps (pos, subscript) -> set of connected (pos, subscript)
        particle_info = {}  # Maps (pos, subscript) -> creation number
        
        # First, collect all subscripts in each square
        for pos, square in enumerate(self.__q_board, 1):
            particles = square.get_particle_list_copy()
            if particles:
                square_subscripts[pos] = {p.get_subscript() for p in particles}
                # Also initialize adjacency entries
                for p in particles:
                    key = (pos, p.get_subscript())
                    if key not in adjacency:
                        adjacency[key] = set()
                        particle_info[key] = p.get_creation_number()
        
        # Build connections between different subscripts that share squares
        for pos, subscripts in square_subscripts.items():
            # For each subscript in this square
            for sub1 in subscripts:
                key1 = (pos, sub1)
                # Connect to other subscripts in the same square
                for sub2 in subscripts:
                    if sub1 != sub2:  # Don't connect to self
                        # Find other squares that have sub2
                        for other_pos, other_subs in square_subscripts.items():
                            if other_pos != pos and sub2 in other_subs:
                                key2 = (other_pos, sub2)
                                adjacency[key1].add(key2)
        
        # Function to check for cycles using DFS
        def find_cycle(node, visited, rec_stack, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in adjacency.get(node, []):
                if neighbor in rec_stack:
                    # Found a cycle! Build complete cycle starting from this node
                    cycle = []
                    current = neighbor
                    while True:
                        cycle.append((current[0], current[1], particle_info[current]))
                        next_nodes = [n for n in adjacency[current] if n not in {node for node, _, _ in cycle}]
                        if not next_nodes or (len(cycle) > 0 and next_nodes[0] == neighbor):
                            break
                        current = next_nodes[0]
                    return cycle
                elif neighbor not in visited:
                    result = find_cycle(neighbor, visited, rec_stack, path)
                    if result:
                        return result
            
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
        # Print all relationships between particles with different subscripts that share squares
        # Keep track of relationships we've already seen
        seen_relationships = set()

        def add_relationship(pos1, particle1, pos2, particle2):
            # Only show relationships between different subscripts
            if particle1.get_subscript() != particle2.get_subscript():
                # Create a sorted tuple of positions and particles to ensure we catch both directions
                relationship = tuple(sorted([(pos1, str(particle1)), (pos2, str(particle2))]))
                if relationship not in seen_relationships:
                    seen_relationships.add(relationship)
                    print(f"{particle1.get_subscript()}[{pos1}] -> {particle2.get_subscript()}[{pos2}]")

        # For each square
        for pos1, square1 in enumerate(self.__q_board, 1):
            particles1 = square1.get_particle_list_copy()
            # For each particle in this square
            for particle1 in particles1:
                # Look for relationships in other squares
                for pos2, square2 in enumerate(self.__q_board, 1):
                    if pos1 != pos2:  # Don't check same square
                        for particle2 in square2.get_particle_list_copy():
                            # If they share a square
                            shared_square = False
                            for pos3, square3 in enumerate(self.__q_board, 1):
                                if pos3 != pos1 and pos3 != pos2:
                                    particles3 = square3.get_particle_list_copy()
                                    if any(p.get_subscript() == particle1.get_subscript() for p in particles3) and \
                                       any(p.get_subscript() == particle2.get_subscript() for p in particles3):
                                        shared_square = True
                                        break
                            if shared_square:
                                add_relationship(pos1, particle1, pos2, particle2)

    def clear_position(self, position: int):
        # Clear all particles from a position after collapse
        if 1 <= position <= 9:
            self.__q_board[position - 1].clear_particles()

    def get_square(self, position: int) -> QBoardSquare:
        # Get the QBoardSquare at the given position (1-9)
        if 1 <= position <= 9:
            return self.__q_board[position - 1]
        raise ValueError("Position must be between 1 and 9")