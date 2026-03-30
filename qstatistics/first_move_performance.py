from pymongo import MongoClient
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


def analyze_first_move_performance(collection):
    """Analyze win-loss difference for each starting move"""
    first_move_stats = defaultdict(
        lambda: {'wins': 0, 'losses': 0, 'total': 0})

    for doc in collection.find():
        player1 = doc.get("Player1", {})
        player2 = doc.get("Player2", {})
        player1_moves = player1.get("moves", [])
        player2_moves = player2.get("moves", [])

        if not player1_moves:
            continue

        first_move = tuple(player1_moves[0]) if isinstance(
            player1_moves[0], list) else player1_moves[0]

        player1_won = player1.get("isWinner", False)
        player2_won = player2.get("isWinner", False)

        first_move_stats[first_move]['total'] += 1
        if player1_won:
            first_move_stats[first_move]['wins'] += 1
        elif player2_won:
            first_move_stats[first_move]['losses'] += 1

    # Calculate win-loss difference
    results = {}
    for move, stats in first_move_stats.items():
        win_loss_diff = stats['wins'] - stats['losses']
        results[move] = win_loss_diff

    return results


def analyze_first_move_combinations(collection):
    """Analyze win-loss difference for Player 1's first quantum move (two positions)"""
    # Initialize 9x9 matrix for all possible combinations
    heatmap_data = np.zeros((9, 9))
    diagonal_debug = {}  # Track what should be on diagonal
    move_19_count = {'wins': 0, 'losses': 0}  # Track [1,9] specifically
    
    for doc in collection.find():
        player1 = doc.get("Player1", {})
        player2 = doc.get("Player2", {})
        player1_moves = player1.get("moves", [])
        
        # Need at least 1 quantum move for Player 1
        if len(player1_moves) < 1:
            continue
            
        # Extract the two positions from Player 1's first quantum move
        first_quantum_move = player1_moves[0]
        if not isinstance(first_quantum_move, list) or len(first_quantum_move) < 2:
            continue
            
        pos1 = first_quantum_move[0]
        pos2 = first_quantum_move[1]
        
        # Debug: Count [1,9] quantum moves (both orders)
        if (pos1 == 1 and pos2 == 9):
            if player1.get('isWinner', False):
                move_19_count['wins'] += 1
            else:
                move_19_count['losses'] += 1
        
        # Debug: track diagonal cases
        if pos1 == pos2:
            diagonal_debug[f"Game {doc.get('Game Number')}"] = [pos1, pos2]
            continue
        
        # Skip if invalid positions
        if pos1 is None or pos2 is None:
            continue
        
        # X-axis: first position, Y-axis: second position (preserve original order)
        x_pos = pos1
        y_pos = pos2
        
        # Debug: Check for game 22 specifically
        if doc.get('Game Number') == 22:
            print(f"DEBUG Game 22: x_pos={x_pos}, y_pos={y_pos}")
            print(f"DEBUG Game 22: x_idx={x_pos-1}, y_idx={y_pos-1}")
        
        # Convert to 0-based indexing
        x_idx = x_pos - 1
        y_idx = y_pos - 1
        
        # Validate indices are within board bounds (0-8)
        if 0 <= x_idx < 9 and 0 <= y_idx < 9:
            player1_won = player1.get("isWinner", False)
            player2_won = player2.get("isWinner", False)
            
            # Update heatmap: +1 for Player 1 win, -1 for Player 2 win
            if player1_won:
                heatmap_data[y_idx][x_idx] += 1
                # Debug: Check for game 22 specifically
                if doc.get('Game Number') == 22:
                    print(f"DEBUG Game 22: Added +1 at [{y_idx}][{x_idx}], new value = {heatmap_data[y_idx][x_idx]}")
            elif player2_won:
                heatmap_data[y_idx][x_idx] -= 1
                # Debug: Check for game 22 specifically
                if doc.get('Game Number') == 22:
                    print(f"DEBUG Game 22: Added -1 at [{y_idx}][{x_idx}], new value = {heatmap_data[y_idx][x_idx]}")
    
    # Print debug info
    if diagonal_debug:
        print(f"Found {len(diagonal_debug)} diagonal cases (should be 0):")
        for game, moves in list(diagonal_debug.items())[:5]:
            print(f"  {game}: {moves}")
    else:
        print("✓ No diagonal cases found - diagonal should be naturally zero")
    
    # Print [1,9] move statistics
    print(f"\n[1,9] quantum moves: {move_19_count['wins']} wins, {move_19_count['losses']} losses")
    print(f"Expected heatmap value: {move_19_count['wins'] - move_19_count['losses']}")
    
    # Print heatmap values matrix
    print("\nHeatmap values (rows=Y, cols=X):")
    print("    X→", end="")
    for x in range(9):
        print(f"{x+1:>12}", end="")
    print()
    
    for y in range(9):
        print(f"Y{y+1:2}:", end="")
        for x in range(9):
            val = int(heatmap_data[y][x])
            if val == 0:
                print(f"{'0':>12}", end="")
            else:
                print(f"{val:>12}", end="")
        print()
    
    # Print diagonal values specifically
    print("\nDiagonal values (should all be 0):")
    for i in range(9):
        print(f"  Position {i+1}: {int(heatmap_data[i][i])}")
    
    # Check the actual value at [8][0] (Y=9, X=1)
    print(f"\nActual value at [8][0] (Y=9, X=1): {int(heatmap_data[8][0])}")
    
    return heatmap_data


def create_heatmap(heatmap_data):
    """Create 9x9 heatmap visualization with custom colormap"""
    # Set global font size for better visibility
    plt.rcParams.update({"font.size": 20})
    
    plt.figure(figsize=(10, 8))
    
    # Create custom colormap to show variance in all-positive data
    # Use sequential colormap from light to dark red
    vmin = heatmap_data.min()
    vmax = heatmap_data.max()
    
    # Use 'Reds' colormap for better variance in positive data
    im = plt.imshow(heatmap_data, cmap='Reds', aspect='auto', 
                     vmin=vmin, vmax=vmax)
    
    # Set ticks and labels
    plt.xticks(range(9), [f'{i+1}' for i in range(9)], fontsize=18)
    plt.yticks(range(9), [f'{i+1}' for i in range(9)], fontsize=18)
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Wins - Losses (Player 1)', fontsize=20)
    
    # Set labels
    plt.xlabel('Player 1 First Position', fontsize=20)
    plt.ylabel('Player 1 Second Position', fontsize=20)
    
    plt.tight_layout()
    plt.savefig('plots/first_move_heatmap.png', dpi=300, bbox_inches='tight')


def main():
    collection = db["QGameResults_1M"]  # Change as needed

    # Generate heatmap data
    heatmap_data = analyze_first_move_combinations(collection)
    create_heatmap(heatmap_data)

    # Also keep the original bar plot
    results = analyze_first_move_performance(collection)

    # Sort by move position (0-8 for 3x3 board)
    sorted_moves = sorted(
        results.keys(), key=lambda x: x[0] if isinstance(x, tuple) else x)
    sorted_results = [results[move] for move in sorted_moves]
    move_labels = [f"Pos {move[0]}" if isinstance(move, tuple) else f"Pos {
        move}" for move in sorted_moves]

    # Set global font size for better visibility
    plt.rcParams.update({"font.size": 20})
    
    # Create bar plot with color intensity based on magnitude
    plt.figure(figsize=(12, 6))

    # Normalize values for color intensity
    max_abs_val = max(abs(min(sorted_results)), abs(max(sorted_results)))
    normalized_vals = [val/max_abs_val for val in sorted_results]

    # Create color map: green for positive, red for negative, intensity based on magnitude
    colors = []
    for val, norm_val in zip(sorted_results, normalized_vals):
        if val > 0:
            # Green with intensity
            colors.append((0, 1-norm_val*0.7, 0, 0.7+norm_val*0.3))
        elif val < 0:
            # Red with intensity
            colors.append((1-norm_val*0.7, 0, 0, 0.7+norm_val*0.3))
        else:
            colors.append((0.5, 0.5, 0.5, 0.7))  # Gray for zero

    _ = plt.bar(move_labels, sorted_results, color=colors,
                edgecolor='black', linewidth=1)

    plt.xlabel('Starting Move Position', fontsize=20)
    plt.ylabel('Wins - Losses (Player 1)', fontsize=20)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    plt.grid(True, alpha=0.3)

    # Add a text annotation explaining the color coding
    plt.text(0.02, 0.98, 'Color intensity = magnitude of win-loss difference',
             transform=plt.gca().transAxes, fontsize=16, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('plots/first_move_win_loss_diff.png',
                dpi=300, bbox_inches='tight')
    # plt.show()


if __name__ == "__main__":
    with MongoClient("mongodb://localhost:27017") as client:
        db = client["TicTacToe"]
        main()
