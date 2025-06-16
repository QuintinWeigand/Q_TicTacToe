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
        # Specifically focusing on the shortest path between particles with the same subscript.
        # Returns (bool, list): whether cycle exists, list of (position, subscript, creation) in cycle
        
        print("\nDEBUG: Running cycle detection...")
        
        # Build adjacency list for each square and its subscripts
        square_subscripts = {}  # Maps square -> set of subscripts in that square
        adjacency = {}  # Maps (pos, subscript) -> set of connected (pos, subscript)
        particle_info = {}  # Maps (pos, subscript) -> creation number
        
        # Maps subscript -> list of (pos, creation) for particles with this subscript
        subscript_locations = {}
        
        # First, collect all subscripts in each square and map by subscript
        for pos, square in enumerate(self.__q_board, 1):
            particles = square.get_particle_list_copy()
            if particles:
                square_subscripts[pos] = {}
                for p in particles:
                    sub = p.get_subscript()
                    cr = p.get_creation_number()
                    square_subscripts[pos][sub] = cr
                    
                    # Group by subscript for faster cycle detection between same subscript
                    if sub not in subscript_locations:
                        subscript_locations[sub] = []
                    subscript_locations[sub].append((pos, cr))
                    
                    # Setup adjacency entries
                    key = (pos, sub)
                    if key not in adjacency:
                        adjacency[key] = set()
                        particle_info[key] = cr
        
        # Build connections between different subscripts that share squares
        for pos, sub_dict in square_subscripts.items():
            # For each subscript in this square
            for sub1 in sub_dict:
                key1 = (pos, sub1)
                # Connect to other subscripts in the same square
                for sub2 in sub_dict:
                    if sub1 != sub2:  # Don't connect to self
                        # Find other squares that have sub2
                        for other_pos, other_sub_dict in square_subscripts.items():
                            if other_pos != pos and sub2 in other_sub_dict:
                                key2 = (other_pos, sub2)
                                adjacency[key1].add(key2)
        
        # First, look for shortest cycle between particles with same subscript
        # which would be the most direct representation of a quantum superposition
        for sub, locations in subscript_locations.items():
            if len(locations) > 1:  # Need at least 2 particles with same subscript
                # Check for a cycle involving this subscript
                shortest_cycle = self._find_shortest_cycle_for_subscript(sub, adjacency, particle_info)
                if shortest_cycle:
                    return True, shortest_cycle
        
        # If no direct cycles between same subscript, look for any cycle
        visited = set()
        for node in adjacency:
            if node not in visited:
                cycle = self._find_any_cycle(node, adjacency, particle_info, visited)
                if cycle:
                    return True, cycle
        
        return False, []
        
    def _find_shortest_cycle_for_subscript(self, subscript, adjacency, particle_info):
        """
        Find the shortest path that connects two particles with the same subscript.
        This represents a quantum superposition that needs to collapse.
        """
        # For each position with this subscript
        nodes_with_subscript = [(pos, subscript) for (pos, sub) in adjacency if sub == subscript]
        
        print(f"DEBUG: Found {len(nodes_with_subscript)} positions with subscript {subscript}")
        
        if len(nodes_with_subscript) < 2:
            return None
            
        # We should always have exactly 2 positions with same subscript in a quantum move
        pos1, pos2 = nodes_with_subscript[0][0], nodes_with_subscript[1][0]
        print(f"DEBUG: Looking for cycle between positions {pos1} and {pos2} with subscript {subscript}")
            
        # Use BFS to find shortest path between the two positions with same subscript
        start = nodes_with_subscript[0]
        target = nodes_with_subscript[1]
            
        # BFS from start node to target node
        visited = {start}
        queue = [(start, [(start[0], start[1], particle_info[start])])]
            
        while queue:
            node, path = queue.pop(0)
                
            # Check each neighbor
            for neighbor in adjacency.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                        
                    # Create new path with this neighbor
                    new_path = path + [(neighbor[0], neighbor[1], particle_info[neighbor])]
                        
                    # If we reached the target node (same subscript, different position)
                    if neighbor == target:
                        print(f"DEBUG: Found cycle! Path length: {len(new_path)}")
                        return new_path  # Return this path as our cycle
                            
                    queue.append((neighbor, new_path))
        
        return None  # No cycle found between same subscript particles
        
    def _find_any_cycle(self, start, adjacency, particle_info, global_visited=None):
        """Find any cycle in the graph using DFS."""
        if global_visited is None:
            global_visited = set()
            
        print(f"DEBUG: Starting DFS cycle detection from node {start}")
        rec_stack = set()
        path = []
        
        def dfs(node):
            global_visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in adjacency.get(node, []):
                # If neighbor is in current recursion stack, we found a cycle
                if neighbor in rec_stack:
                    # Extract cycle from path
                    idx = path.index(neighbor)
                    print(f"DEBUG: Found cycle! Node {neighbor} is already in the recursion stack.")
                    cycle_nodes = path[idx:] + [neighbor]
                    return [(n[0], n[1], particle_info[n]) for n in cycle_nodes]
                
                # If not visited, continue DFS
                elif neighbor not in global_visited:
                    result = dfs(neighbor)
                    if result:
                        return result
            
            # Backtrack
            path.pop()
            rec_stack.remove(node)
            return None
            
        return dfs(start)

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