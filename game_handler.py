from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from QuantumGame.QuantumGame import QuantumGame
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app)

game = QuantumGame()

# Emit game state whenever it changes
def emit_game_state():
     socketio.emit('game_state', {
        'game_over': game.game_over,
        'current_player': game.current_player,
        'board': game.get_game_state()
    })

@app.route('/api/play-move', methods=['POST'])
def play_move():
    print("play_move route accessed")  # Log route access
    data = request.get_json()  # Extract JSON payload
    print(f"Received data: {data}")  # Log the data
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    pos1 = data.get("input1")
    pos2 = data.get("input2")

    try:
        pos1 = int(pos1)
        pos2 = int(pos2)
        print(f"Positions received: pos1={pos1}, pos2={pos2}")  # Log positions
        if game.make_move(pos1, pos2):
            emit_game_state()  # Push updated game state to clients
            return jsonify({"success": True, "message": "Move successful!"})
        else:
            return jsonify({"success": False, "message": "Move failed! Try again."})
    except ValueError:
        return jsonify({"error": "Invalid positions! Must be numbers between 1 and 9."}), 400

@app.route('/api/game-state', methods=['GET'])
def game_state():
    return jsonify({
        'game_over': game.game_over,
        'current_player': game.current_player,
        'board': game.get_game_state(),
        'winner': game.winner
    })

@app.route('/api/restart-game', methods=['POST'])
def restart_game():
    print("Restarting the game...")  # Log the restart action
    game.reset()  # Call the reset method in your game logic
    return jsonify({"success": True, "message": "Game restarted successfully!"})

if __name__ == "__main__":
    socketio.run(app, port=5000)


