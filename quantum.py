from QuantumGame.QuantumGame import QuantumGame

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