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

@app.route('/api/get-collapse-options', methods=['GET'])
def get_collapse_options():
    if game.collapse_options:
        return jsonify({"success": True, "options": game.collapse_options})
    return jsonify({"success": True, "options": None})

@app.route('/api/submit-collapse-choice', methods=['POST'])
def submit_collapse_choice():
    data = request.get_json()
    print(f"Received data for collapse choice: {data}")  # Debug print statement
    if not data or "choice" not in data:
        return jsonify({"success": False, "message": "Invalid data."}), 400

    choice = data["choice"]
    try:
        choice = int(choice)
        if 0 <= choice < len(game.collapse_options):
            chosen_pos, chosen_subscript, chosen_creation = game.collapse_options[choice]
            game.resolve_collapse([], chosen_pos, chosen_subscript, chosen_creation)
            game.collapse_options = []  # Clear collapse options
            game.game_paused = False  # Resume the game
            emit_game_state()  # Push updated game state to clients
            return jsonify({"success": True, "message": "Collapse choice processed successfully!"})
        else:
            return jsonify({"success": False, "message": "Choice out of range."}), 400
    except ValueError:
        return jsonify({"success": False, "message": "Invalid choice format."}), 400

if __name__ == "__main__":
    socketio.run(app, port=5000)


