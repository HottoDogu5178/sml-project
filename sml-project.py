from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-tw">
<head>
    <meta charset="UTF-8">
    <title>井字棋遊戲</title>
    <style>
        table { border-collapse: collapse; }
        td { width: 60px; height: 60px; text-align: center; font-size: 2em; border: 1px solid #333; }
        button { width: 100%; height: 100%; font-size: 2em; }
    </style>
</head>
<body>
    <h1>井字棋遊戲</h1>
    <form method="post">
        <table>
            {% for i in range(3) %}
            <tr>
                {% for j in range(3) %}
                <td>
                    {% if board[i][j] == '' %}
                        <button name="move" value="{{i}},{{j}}" {% if winner %}disabled{% endif %}></button>
                    {% else %}
                        {{ board[i][j] }}
                    {% endif %}
                </td>
                {% endfor %}
            </tr>
            {% endfor %}
        </table>
        <input type="hidden" name="board" value="{{ board|tojson|safe }}">
        <input type="hidden" name="turn" value="{{ turn }}">
    </form>
    {% if winner %}
        <h2>{{ winner }} 勝利！</h2>
        <a href="{{ url_for('index') }}">重新開始</a>
    {% endif %}
</body>
</html>
"""

import json

def check_winner(board):
    for row in board:
        if row[0] and row[0] == row[1] == row[2]:
            return row[0]
    for col in range(3):
        if board[0][col] and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
    if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        board = json.loads(request.form["board"])
        turn = request.form["turn"]
        move = request.form["move"]
        i, j = map(int, move.split(","))
        if board[i][j] == "":
            board[i][j] = turn
            winner = check_winner(board)
            next_turn = "O" if turn == "X" else "X"
            return render_template_string(
                TEMPLATE, board=board, turn=next_turn, winner=winner
            )
        else:
            winner = check_winner(board)
            return render_template_string(
                TEMPLATE, board=board, turn=turn, winner=winner
            )
    else:
        board = [[""] * 3 for _ in range(3)]
        turn = "X"
        winner = None
        return render_template_string(
            TEMPLATE, board=board, turn=turn, winner=winner
        )

if __name__ == "__main__":
    app.run(debug=True)