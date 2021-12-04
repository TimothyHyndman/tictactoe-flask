from pathlib import Path
from typing import Tuple, Optional

import numpy as np
import tensorflow as tf

MODEL_PATH = Path(__file__).parent / "model_001_32_32_random_opponent.h5"
q_network = tf.keras.models.load_model(MODEL_PATH)


def board_array2state(board_arr: np.ndarray, player=1) -> np.ndarray:
    return np.dstack([(board_arr == player), (board_arr == -player)])


def get_possible_actions(board: np.ndarray) -> np.ndarray:
    return (board == 0).flatten()


def move_probabilities(state: np.ndarray, possible_actions: np.ndarray) -> np.ndarray:
    # Need to add "batch" dimension
    state_reshape = np.expand_dims(state, axis=0)
    predictions = q_network(state_reshape, training=False)

    probabilities = tf.nn.softmax(predictions).numpy()
    probabilities = probabilities * possible_actions
    probabilities = probabilities / np.sum(probabilities)

    return np.reshape(probabilities, (3, 3))


def select_move(board: np.ndarray, player: int = 1) -> Tuple[int, int]:
    possible_actions = get_possible_actions(board)
    state = board_array2state(board, player=player)
    probabilities = move_probabilities(state, possible_actions)

    # Always select highest probability move.
    row, col = np.unravel_index(np.argmax(probabilities), probabilities.shape)

    return row, col


def check_win(board: np.ndarray) -> Optional[int]:
    if (board.sum(0) == 3).any():
        return 1
    if (board.sum(1) == 3).any():
        return 1
    if (board.sum(0) == -3).any():
        return -1
    if (board.sum(1) == -3).any():
        return -1

    if board.diagonal().sum() == 3:
        return 1
    if board.diagonal().sum() == -3:
        return -1
    if np.fliplr(board).diagonal().sum() == 3:
        return 1
    if np.fliplr(board).diagonal().sum() == -3:
        return -1

    if (board != 0).all():
        return 0

    # If the game isn't a draw or a win for either player then no result
    return None
