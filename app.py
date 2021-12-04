import numpy as np
from flask import Flask, render_template, request, url_for

from game import select_move, check_win

app = Flask(__name__)


@app.route("/")
def main():
    board = "_________"
    return render_template("index.html", board=board, **get_square_images(board))


@app.route("/click_square/<int:x>/<int:y>", methods=["POST"])
def click_square(x, y):
    # Get the current state of the board
    board = request.form["board"]

    # Convert into numpy array
    board_arr = board_str2array(board)
    winner = check_win(board_arr)

    # If move valid, play it and call the AI
    if board_arr[y, x] == 0 and winner is None:
        # Player 1 move
        board_arr[y, x] = 1
        winner = check_win(board_arr)

        # Player 2 move
        if winner is None:
            row, col = select_move(board_arr, player=-1)
            board_arr[row, col] = -1

    # Convert back to string
    board = board_array2str(board_arr)

    # Finally, get image for every square and return updated html
    square_images = get_square_images(board)
    return render_template("index.html", board=board, **square_images)


def board_str2array(board_str: str) -> np.ndarray:
    values_map = {"_": 0, "o": -1, "x": 1}
    board_arr = np.array([values_map[x] for x in list(board_str)]).reshape((3, 3))
    return board_arr


def board_array2str(board_arr: np.ndarray) -> str:
    values_map = {0: "_", -1: "o", 1: "x"}
    board_str = "".join([values_map[x] for x in board_arr.flatten().tolist()])
    return board_str


def get_square_images(board):
    return {
        "square_00_image": get_square_image(board[0]),
        "square_01_image": get_square_image(board[1]),
        "square_02_image": get_square_image(board[2]),
        "square_10_image": get_square_image(board[3]),
        "square_11_image": get_square_image(board[4]),
        "square_12_image": get_square_image(board[5]),
        "square_20_image": get_square_image(board[6]),
        "square_21_image": get_square_image(board[7]),
        "square_22_image": get_square_image(board[8]),
    }


def get_square_image(value: str):
    if value == "x":
        return url_for('static', filename='cross.png')

    if value == "o":
        return url_for('static', filename='circle.png')

    return url_for('static', filename='blank.png')


if __name__ == '__main__':
    app.run()
