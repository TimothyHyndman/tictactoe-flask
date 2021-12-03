from typing import List

from flask import Flask, render_template, request, url_for

app = Flask(__name__)


@app.route("/")
def main():
    board = "_________"
    return render_template("index.html", board=board, **get_square_images(board))


@app.route("/click_square/<int:x>/<int:y>", methods=["POST"])
def click_square(x, y):
    board = request.form["board"]
    board = update_board(board, x=x, y=y, value="x")
    square_images = get_square_images(board)
    return render_template("index.html", board=board, **square_images)


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


def update_board(board: str, x: int, y: int, value: str) -> str:
    board_list = list(board)
    str_loc = y * 3 + x
    board_list[str_loc] = value

    return "".join(board_list)


def get_square_image(value: str):
    if value == "x":
        return url_for('static', filename='cross.png')
    if value == "o":
        return url_for('static', filename='cross.png')

    return url_for('static', filename='blank.png')


if __name__ == '__main__':
    app.run()