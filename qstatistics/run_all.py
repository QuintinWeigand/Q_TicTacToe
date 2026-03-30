import subprocess
import sys
import os

def main():
    scripts = [
        ("total_wins.py", "Total Wins"),
        ("first_move_performance.py", "First Move Performance"),
        ("wins_vs_steps.py", "Wins vs Steps"),
        ("num_moves.py", "Number of Moves"),
        ("num_steps.py", "Number of Steps"),
    ]
    
    base_dir = os.path.dirname(__file__)
    
    for script_name, title in scripts:
        script_path = os.path.join(base_dir, script_name)
        print(f"\n{'='*50}")
        print(f"Running: {title}")
        print(f"{'='*50}")
        result = subprocess.run([sys.executable, script_path])
        if result.returncode != 0:
            print(f"Error running {script_name}")
        else:
            print(f"Completed: {title}")

if __name__ == "__main__":
    main()
