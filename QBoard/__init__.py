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
        
        # print("\nDEBUG: Running cycle detection...")
        
        # Build adjacency list of entangled pairs: (pos, sub, cr) <-> (other_pos, sub, other_cr)
        from collections import defaultdict, deque
        particles = []
        sub_to_particles = defaultdict(list)  # sub -> list of (pos, cr)
        for pos, square in enumerate(self.__q_board, 1):
            for p in square.get_particle_list_copy():
                sub = p.get_subscript()
                cr = p.get_creation_number()
                particles.append((pos, sub, cr))
                sub_to_particles[sub].append((pos, cr))

        adjacency = defaultdict(set)  # (pos, sub, cr) -> set of (pos, sub, cr)
        # Build two types of adjacency: entangled pairs and same-square
        entangled_adjacency = defaultdict(set)
        for sub, plist in sub_to_particles.items():
            if len(plist) == 2:
                (pos1, cr1), (pos2, cr2) = plist
                entangled_adjacency[(pos1, sub, cr1)].add((pos2, sub, cr2))
                entangled_adjacency[(pos2, sub, cr2)].add((pos1, sub, cr1))

        square_adjacency = defaultdict(set)
        pos_to_particles = defaultdict(list)
        for pos, sub, cr in particles:
            pos_to_particles[pos].append((pos, sub, cr))
        for plist in pos_to_particles.values():
            for i in range(len(plist)):
                for j in range(i + 1, len(plist)):
                    a, b = plist[i], plist[j]
                    square_adjacency[a].add(b)
                    square_adjacency[b].add(a)

        # Cycle search alternates between entangled and square connections
        def find_quantum_cycle():
            for start in particles:
                stack = [(start, [start], True)]  # (current, path, next_is_entangled)
                while stack:
                    node, path, entangled_next = stack.pop()
                    neighbors = entangled_adjacency[node] if entangled_next else square_adjacency[node]
                    for neighbor in neighbors:
                        if neighbor == path[0] and len(path) > 2:
                            # Found a cycle
                            # print(f"[DEBUG] Detected quantum cycle: {path + [neighbor]}")
                            return path + [neighbor]
                        if neighbor not in path:
                            stack.append((neighbor, path + [neighbor], not entangled_next))
            return None

        cycle = find_quantum_cycle()
        if cycle:
            return True, cycle
        # print("[DEBUG] No quantum cycle detected.")
        return False, []

        # Find any cycle in the entanglement graph using BFS
        def find_cycle():
            for start in particles:
                queue = deque([(start, [start])])
                while queue:
                    node, path = queue.popleft()
                    for neighbor in adjacency[node]:
                        if neighbor in path and neighbor != path[-2]:
                            # Found a cycle (not just returning to immediate predecessor)
                            cycle_start = path.index(neighbor)
                            cycle = path[cycle_start:] + [neighbor]
                            print(f"[DEBUG] Detected cycle: {cycle}")
                            return cycle
                        if neighbor not in path:
                            queue.append((neighbor, path + [neighbor]))
            return None

        # print("[DEBUG] Entanglement adjacency list:")
        # for k, v in adjacency.items():
        #     print(f"  {k}: {list(v)}")
        # print(f"[DEBUG] All particles: {particles}")
        cycle = find_cycle()
        if cycle:
            # print(f"[DEBUG] Detected cycle: {cycle}")
            return True, cycle
        # print("[DEBUG] No cycle detected.")
        return False, []
        
    def _find_shortest_cycle_for_subscript(self, subscript, adjacency, particle_info):
        """
        Find the shortest path that connects two particles with the same subscript.
        This represents a quantum superposition that needs to collapse.
        """
        # For each position with this subscript
        nodes_with_subscript = [(pos, subscript) for (pos, sub) in adjacency if sub == subscript]
        
        # print(f"DEBUG: Found {len(nodes_with_subscript)} positions with subscript {subscript}")
        
        if len(nodes_with_subscript) < 2:
            return None
            
        # We should always have exactly 2 positions with same subscript in a quantum move
        pos1, pos2 = nodes_with_subscript[0][0], nodes_with_subscript[1][0]
        # print(f"DEBUG: Looking for cycle between positions {pos1} and {pos2} with subscript {subscript}")
            
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
                        # Remove duplicate nodes from the path
                        seen = set()
                        filtered_path = []
                        for p in new_path:
                            if (p[0], p[1], p[2]) not in seen:
                                filtered_path.append(p)
                                seen.add((p[0], p[1], p[2]))
                        # print(f"DEBUG: Found cycle! Path length: {len(filtered_path)}")
                        return filtered_path  # Return this path as our cycle

                    queue.append((neighbor, new_path))

        return None  # No cycle found between same subscript particles
        
    def _find_any_cycle(self, start, adjacency, particle_info, global_visited=None):
        """Find any cycle in the graph using DFS."""
        if global_visited is None:
            global_visited = set()
            
        # print(f"DEBUG: Starting DFS cycle detection from node {start}")
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
                    # print(f"DEBUG: Found cycle! Node {neighbor} is already in the recursion stack.")
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