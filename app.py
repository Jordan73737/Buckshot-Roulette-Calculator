from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Game state
game_state = {
    "total_shells": 0,
    "live_shells": 0,
    "blank_shells": 0,
    "shells": [],  # This will track the actual shells (live, blank, or unknown)
    "selected_shell": None  # Tracks the currently selected shell
}

@app.route('/')
def index():
    return render_template('index.html', game_state=game_state)

@app.route('/start', methods=['POST'])
def start_game():
    data = request.json
    try:
        total = int(data.get('total_shells'))
        live = int(data.get('live_shells'))
    except (ValueError, TypeError):
        return jsonify({"message": "Total shells and live shells must be integers between 1 and 7", "error": True}), 400

    # Enforce shell count limits
    if total < 1 or total > 8:
        return jsonify({"message": "Total shells must be between 1 and 8", "error": True}), 400
    if live < 0 or live > total:
        return jsonify({"message": "Live shells must be between 0 and the total number of shells", "error": True}), 400

    blank = total - live

    # Initialize shells list: all start as "unknown"
    shells = ["unknown"] * total

    game_state.update({
        "total_shells": total,
        "live_shells": live,
        "blank_shells": blank,
        "shells": shells,  # All shells start as unknown
        "selected_shell": None
    })
    return jsonify({"message": "Game started successfully", "game_state": game_state})

@app.route('/select', methods=['POST'])
def select_shell():
    data = request.json
    index = data.get('index')
    if 0 <= index < len(game_state["shells"]):
        game_state["selected_shell"] = index
        return jsonify({"message": "Shell selected", "game_state": game_state})
    return jsonify({"message": "Invalid shell index", "error": True}), 400

@app.route('/configure', methods=['POST'])
def configure_shell():
    data = request.json
    shell_type = data.get('type')
    index = game_state["selected_shell"]

    if index is None or shell_type not in ["live", "blank"]:
        return jsonify({"message": "Invalid configuration", "error": True}), 400

    # Only configure if the selected shell is still "unknown"
    if game_state["shells"][index] == "unknown":
        game_state["shells"][index] = shell_type
        if shell_type == "live":
            game_state["live_shells"] -= 1
            game_state["total_shells"] -=1
        elif shell_type == "blank":
            game_state["blank_shells"] -= 1
            game_state["total_shells"] -=1
        game_state["selected_shell"] = None

    # Calculate remaining shells dynamically
    remaining_live = game_state["live_shells"]
    remaining_blank = game_state["blank_shells"]
    total_unknown = remaining_live + remaining_blank

    # Calculate probabilities dynamically based on remaining shells
    prob_live = 0
    prob_blank = 0
    if total_unknown > 0:
        prob_live = (remaining_live / total_unknown) * 100
        prob_blank = (remaining_blank / total_unknown) * 100

    # Update and return the game state
    return jsonify({
        "message": "Shell configured successfully",
        "game_state": {
            "total_shells": game_state["total_shells"],
            "live_shells": game_state["live_shells"],
            "blank_shells": game_state["blank_shells"],
            "shells": game_state["shells"],
            "prob_live": prob_live,
            "prob_blank": prob_blank
        }
    })

@app.route('/clear', methods=['POST'])
def clear_shell():
    index = game_state["selected_shell"]

    if index is None:
        return jsonify({"message": "No shell selected", "error": True}), 400

    # Only clear if the shell is currently configured
    current_type = game_state["shells"][index]
    if current_type in ["live", "blank"]:
        game_state["shells"][index] = "unknown"
        if current_type == "live":
            game_state["live_shells"] += 1
            game_state["total_shells"] += 1
        elif current_type == "blank":
            game_state["blank_shells"] += 1
            game_state["total_shells"] += 1

    game_state["selected_shell"] = None

    # Recalculate probabilities dynamically
    remaining_live = game_state["live_shells"]
    remaining_blank = game_state["blank_shells"]
    total_unknown = remaining_live + remaining_blank

    prob_live = 0
    prob_blank = 0
    if total_unknown > 0:
        prob_live = (remaining_live / total_unknown) * 100
        prob_blank = (remaining_blank / total_unknown) * 100

    return jsonify({
        "message": "Shell cleared successfully",
        "game_state": {
            "total_shells": game_state["total_shells"],
            "live_shells": game_state["live_shells"],
            "blank_shells": game_state["blank_shells"],
            "shells": game_state["shells"],
            "prob_live": prob_live,
            "prob_blank": prob_blank
        }
    })


@app.route('/reset', methods=['POST'])
def reset_game():
    game_state.update({
        "total_shells": 0,
        "live_shells": 0,
        "blank_shells": 0,
        "shells": [],
        "selected_shell": None
    })
    return jsonify({"message": "Game reset successfully", "game_state": game_state})

if __name__ == '__main__':
    app.run(debug=True)
