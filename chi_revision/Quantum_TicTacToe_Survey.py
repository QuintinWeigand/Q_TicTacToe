import sys
from random import choice, choices, sample
import pymongo

class QuantumTicTacToe:
    def __init__(self):
        # The board for Real marks: 1-9. None if empty.
        self.real_board = {i: None for i in range(1, 10)}
        
        # History of moves: (turn_number, player_symbol, grid1, grid2)
        self.moves = []
        
        # Adjacency for cycle detection: node -> list of (neighbor, move_index)
        self.graph = {i: [] for i in range(1, 10)}
        
        self.turn_count = 1
        self.players = ['X', 'O']

        # for recording the end game
        self.recorded_moves = []
        self.winner = -1
        
    def print_board(self):
        
        return
    
        print(f"\n--- Turn {self.turn_count} ({self.current_player()}) ---")
        print("Board State (Real Marks):")
        for r in range(0, 9, 3):
            row_cells = []
            for c in range(1, 4):
                idx = r + c
                val = self.real_board[idx] if self.real_board[idx] else str(idx)
                row_cells.append(val)
            print(" | ".join(row_cells))
            if r < 6: print("-" * 9)
        
        # Show Ghost marks (Superposition)
        print("\nGhost Marks (Spooky):")
        active_moves = [m for i, m in enumerate(self.moves) if not m['collapsed']]
        if not active_moves:
            print("None")
        else:
            for m in active_moves:
                print(f"Move {m['id']} ({m['player']}): {m['s1']} <-> {m['s2']}")
        print("-----------------------")
        

    def clean_board(self):
        # refresh everything for a new game
        self.real_board = {i: None for i in range(1, 10)}
        
        # History of moves: (turn_number, player_symbol, grid1, grid2)
        self.moves = []
        
        # Adjacency for cycle detection: node -> list of (neighbor, move_index)
        self.graph = {i: [] for i in range(1, 10)}
        
        self.turn_count = 1
        
        self.recorded_moves = []
        self.winner = -1
        
        
    def current_player(self):
        return self.players[(self.turn_count - 1) % 2]

    def other_player(self):
        return self.players[self.turn_count % 2]

    def play(self):
        while True:
            self.print_board()
            if self.check_win():
                break
            
            try:
                
                # coun the real board
                avail_grids = []
                
                for i in range(1,10):
                    if self.real_board[i] is None:
                        avail_grids.append(i)
                        
                #print(avail_grids)
                if len(avail_grids) > 1:
                    p1, p2 = sample(avail_grids, k=2)
                else:
                    p1, p2 = avail_grids[0], avail_grids[0]
                
                #print('Step ', self.turn_count, ': ', p1, p2)
                
                if p1 > p2:
                    p1, p2 = p2, p1
                
                self.recorded_moves.append((p1,p2))
                #print((p1, p2))
                
                '''
                # 1. Input
                print(f"Player {self.current_player()}, enter two distinct grid numbers (1-9):")
                inp = input("> ").strip().split()
                if len(inp) != 2:
                    print("Invalid input. Please enter two numbers separated by space.")
                    continue
                
                p1, p2 = int(inp[0]), int(inp[1])
                
                # 2. Validation
                if not (1 <= p1 <= 9 and 1 <= p2 <= 9):
                    print("Numbers must be between 1 and 9.")
                    continue
                #if p1 == p2:
                #    print("You must choose two DIFFERENT grids.")
                #    continue
                if self.real_board[p1] is not None or self.real_board[p2] is not None:
                    print("One of these grids is already occupied by a Real Mark.")
                    continue
                '''

                # 3. Record Move
                move_id = len(self.moves)
                move_data = {
                    'id': move_id,
                    'player': self.current_player(),
                    's1': p1,
                    's2': p2,
                    'collapsed': False, # True if it has become a real mark
                    'final_pos': None   # Will store the grid index when collapsed
                }
                self.moves.append(move_data)
                
                # Add to graph for cycle detection
                self.graph[p1].append((p2, move_id))
                self.graph[p2].append((p1, move_id))

                # 4. Cycle Detection & Measurement
                self.handle_entanglement(move_id)
                
                # Check win immediately after potential collapse
                if self.check_win():
                    break

                self.turn_count += 1

            except ValueError:
                print("Invalid input. Please enter numbers.")

    def handle_entanglement(self, current_move_id):
        """
        Detects if the graph contains a cycle. If so, triggers collapse.
        """
        # We only need to check for cycles involving the newly added edge,
        # but a full search is safer for robustness.
        visited = set()
        path = [] # List of (node, move_id)
        
        cycle_found = self.find_cycle_dfs(self.moves[current_move_id]['s1'], -1, visited, path)
        
        if cycle_found:
            #print("\n*** CYCLIC ENTANGLEMENT DETECTED! ***")
            # Extract the cycle path
            cycle_nodes = [node for node, mid in cycle_found]
            #print(f"Cycle Loop: {cycle_nodes}")
            
            # The User Rule: "Ask the other player to choose"
            self.resolve_cycle(cycle_found)

    def find_cycle_dfs(self, current_node, parent_move_id, visited, path):
        """
        Returns a list of (node, move_id) tuples representing the cycle if found.
        """
        if current_node in [n for n, m in path]:
            # Cycle detected. Slice the path to get the loop.
            # Find index where current_node first appeared
            for i, (n, m) in enumerate(path):
                if n == current_node:
                    return path[i:]
            return None

        visited.add(current_node)
        
        # Sort neighbors to ensure deterministic behavior or prioritization
        neighbors = self.graph[current_node]
        
        for neighbor, move_id in neighbors:
            # Don't go back along the edge we just came from
            if move_id == parent_move_id:
                continue
            
            # Don't traverse already collapsed moves
            if self.moves[move_id]['collapsed']:
                continue

            path.append((current_node, move_id))
            result = self.find_cycle_dfs(neighbor, move_id, visited, path)
            if result:
                return result
            path.pop()
            
        return None

    def resolve_cycle(self, cycle_path):
        """
        Prompts the OTHER player to collapse the cycle.
        cycle_path is a list of (start_node, move_id)
        """
        #print(f"Player {self.other_player()}, a cycle was formed.")
        #print("You must choose how it collapses.")
        
        # A cycle has exactly two stable configurations.
        # Config 1: Move[i] lands on Node[i]
        # Config 2: Move[i] lands on Node[i+1]
        
        # Let's verify the first move in the cycle path
        first_node, first_move_id = cycle_path[0]
        # The edge connects first_node to the next node in the list
        
        # We present the choice based on the first move in the cycle
        m0 = self.moves[first_move_id]
        
        #print(f"Consider Move {first_move_id} (Player {m0['player']}) between {m0['s1']} and {m0['s2']}.")
        #print(f"Option 1: Collapse Move {first_move_id} into {m0['s1']}")
        #print(f"Option 2: Collapse Move {first_move_id} into {m0['s2']}")
        
        #choice = ''
        #while choice not in ['1', '2']:
        #    choice = input("Choose realization (1 or 2): ").strip()
        
        final_choice = choice(['1','2'])
        target = m0['s1'] if final_choice == '1' else m0['s2']
        
        self.recorded_moves.append((0, target))
        
        #print(f"Collapsing Move {first_move_id} into {target}...")
        self.propagate_collapse(first_move_id, target)

    def propagate_collapse(self, start_move_id, start_target):
        """
        Recursive collapse (The "Domino Effect").
        When a move collapses to 'start_target', it becomes Real.
        Any OTHER move touching 'start_target' must flee to its alternative.
        """
        queue = [(start_move_id, start_target)]
        
        while queue:
            mid, target_loc = queue.pop(0)
            move = self.moves[mid]
            
            if move['collapsed']:
                # If already collapsed, check consistency
                if move['final_pos'] != target_loc:
                    # This happens if two collapse waves crash (Quantum Crash).
                    # For this simple implementation, we ignore or log it.
                    pass 
                continue

            # 1. Finalize this move
            move['collapsed'] = True
            move['final_pos'] = target_loc
            self.real_board[target_loc] = move['player']
            #print(f"-> Move {mid} collapsed to {target_loc} ({move['player']})")
            
            # 2. Find neighbors who are now displaced
            # Any active move connected to target_loc must go to its OTHER node
            neighbors = self.graph[target_loc]
            for neighbor_node, neighbor_move_id in neighbors:
                if neighbor_move_id == mid: 
                    continue # Ignore self
                
                neighbor_move = self.moves[neighbor_move_id]
                if not neighbor_move['collapsed']:
                    # Force it to the other node
                    s1, s2 = neighbor_move['s1'], neighbor_move['s2']
                    forced_target = s2 if s1 == target_loc else s1
                    queue.append((neighbor_move_id, forced_target))

    def get_move_id_for_pos(self, position):
        """
        Finds which move_id is currently occupying the given position (1-9).
        Returns -1 if not found (should not happen for real marks).
        """
        for move in self.moves:
            if move['collapsed'] and move['final_pos'] == position:
                return move['id']
        return -1
                    
    def check_win(self):
        b = self.real_board
        wins = [
            (1,2,3), (4,5,6), (7,8,9), # Horizontal
            (1,4,7), (2,5,8), (3,6,9), # Vertical
            (1,5,9), (3,5,7)           # Diagonal
        ]
        
        x_win = False
        o_win = False
        
        
        #for x, y, z in wins:
        #    if b[x] and b[x] == b[y] == b[z]:
        #        if b[x] == 'X': x_win = True
        #        if b[x] == 'O': o_win = True
        
        # Store all completed lines: (Player, Max_Move_ID, Line_Tuple)
        completed_lines = []
        
        for p1, p2, p3 in wins:
        
            # Check if this line is fully occupied by the SAME player
            if b[p1] and b[p1] == b[p2] == b[p3]:
                winner = b[p1]  
                    
                # Retrieve the move_id for each mark in this line
                m1 = self.get_move_id_for_pos(p1)
                m2 = self.get_move_id_for_pos(p2)
                m3 = self.get_move_id_for_pos(p3)

                # The "Timestamp" of this line is the latest move involved
                # (The line couldn't exist before this move was made)
                line_timestamp = max(m1, m2, m3)

                completed_lines.append({
                    'player': winner,
                    'timestamp': line_timestamp,
                    'line': (p1, p2, p3)
                })
        
        if not completed_lines:
            # No lines, check for full board draw
            if all(self.real_board.values()):
                self.print_board()
                print("Board full! It's a DRAW.")
                return True
            return False

        # --- TIE BREAKER LOGIC ---
        
        # Sort lines by timestamp (Ascending = Earliest first)
        # If timestamps are equal (impossible in this logic as move_ids are unique), 
        # it doesn't matter.
        completed_lines.sort(key=lambda x: x['timestamp'])
        
        best_line = completed_lines[0]
        winner = best_line['player']
        
        # Check if the other player also had a line (just for display purposes)
        losers = [l for l in completed_lines if l['player'] != winner]
        
        self.print_board()
        #print(f"\n*** GAME OVER ***")
        
        #if losers:
        #    print("Simultaneous Lines Detected!")
        #    print(f"Player {winner} line: {best_line['line']} (Completed at Move {best_line['timestamp']})")
        #    print(f"Player {losers[0]['player']} line: {losers[0]['line']} (Completed at Move {losers[0]['timestamp']})")
        #    print(f"-> Player {winner} wins because their line was formed earlier!")
        #else:
        #    print(f"Player {winner} Wins with line {best_line['line']}!")
            
        self.winner = self.players.index(winner)
        
        return True
    
        '''
        if x_win and o_win:
            self.print_board()
            print("Both players completed lines simultaneously! It's a DRAW (or specific tie-breaker).")
            return True
        elif x_win:
            self.print_board()
            print("Player X Wins!")
            return True
        elif o_win:
            self.print_board()
            print("Player O Wins!")
            return True
            
        # Check full board
        if all(self.real_board.values()):
            self.print_board()
            print("Board full! It's a DRAW.")
            return True
            
        return False
        '''

if __name__ == "__main__":
    
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["QuantumTicTacToe"]
    collection = db["NewQGameResults_1M"]
    
    game = QuantumTicTacToe()
    
    # Buffer for bulk insertion
    batch_size = 1000
    results_buffer = []
    
    # Number of games to simulate
    total_games = 1_000_000  # Running full simulation
    
    print(f"Starting simulation of {total_games} games...")
    
    for i in range(total_games):
        game.play()

        # Count actual moves (excluding collapse resolutions which start with 0)
        n_steps = len([pair for pair in game.recorded_moves if pair[0] != 0])

        # Prepare document for MongoDB
        game_doc = {
            "game_index": i,
            "first_move": {
                "s1": int(game.recorded_moves[0][0]),
                "s2": int(game.recorded_moves[0][1])
            },
            "total_steps": int(n_steps),
            "winner": int(game.winner),
            "moves_history": game.recorded_moves  # Stores full sequence [(s1, s2), (0, collapse_target), ...]
        }
        
        results_buffer.append(game_doc)

        # Batch insert
        if len(results_buffer) >= batch_size:
            collection.insert_many(results_buffer)
            results_buffer = []
            if (i+1) % 10000 == 0:
                print(f"Simulated {i + 1} games...")

        game.clean_board()
        
    # Insert remaining documents
    if results_buffer:
        collection.insert_many(results_buffer)
        
    print("Simulation complete. Results saved to MongoDB.")
