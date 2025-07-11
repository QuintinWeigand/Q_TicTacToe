from flask import Flask, jsonify
from flask_socketio import SocketIO
from QuantumGame.QuantumGame import QuantumGame
import threading

app = Flask(__name__)
socketio = SocketIO(app)
game = QuantumGame()

@app.route('/game_state', methods=['GET'])
def get_game_state():
    return jsonify({
        'game_over': game.game_over,
        'current_player': game.current_player,
        'board': game.get_game_state()
    })

# Example WebSocket event to broadcast game state
@socketio.on('update_game_state')
def update_game_state():
    socketio.emit('game_state', {
        'game_over': game.game_over,
        'current_player': game.current_player,
        'board': game.get_game_state()
    })

def run_flask():
    socketio.run(app, debug=True, use_reloader=False)

def main():
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

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