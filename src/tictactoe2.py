import numpy as np


class TicTacToe:
    horizontal_size = 3
    vertical_size = 3

    def __init__(self, board=None, current_player: int = 1):
        self.board = board if board is not None else np.zeros((self.horizontal_size * self.vertical_size), dtype=int)
        self.current_player = current_player
        self.game_history = []

    def return_winner(self):
        """
        Checks if a player has won the game and returns it. If no player has won, returns None.
        :return: the player that has won the game, None if no player has won, 0 for a draw.
        """
        # Check for horizontal win
        for i in range(self.horizontal_size):
            if all(self.board[i * self.vertical_size:(i + 1) * self.vertical_size] == 1):
                return 1
            elif all(self.board[i * self.vertical_size:(i + 1) * self.vertical_size] == -1):
                return -1

        # Check for vertical win
        for i in range(self.vertical_size):
            if all(self.board[i::self.vertical_size] == 1):
                return 1
            elif all(self.board[i::self.vertical_size] == -1):
                return -1

        # Check for diagonal win
        if all(self.board[0::self.vertical_size + 1] == 1) or all(
                self.board[self.vertical_size - 1:-1:self.vertical_size - 1] == 1):
            return 1
        elif all(self.board[0::self.vertical_size + 1] == -1) or all(
                self.board[self.vertical_size - 1:-1:self.vertical_size - 1] == -1):
            return -1

        # Check for draw
        if 0 not in set([i for i in self.board]):
            return 0

        return None

    @property
    def is_over(self):
        """
        Checks if the game is over
        :return: True if the game is over, False otherwise
        """
        return self.return_winner() is not None

    def make_move(self, move: int):
        """
        Makes a move on the board for the current player and starts the turn of the other player
        :param move: the position to make the move at
        """
        if 0 <= move < self.horizontal_size * self.vertical_size and self.board[move] == 0:
            self.board[move] = self.current_player
            self.game_history.append(move)
            self.current_player = -self.current_player
        else:
            raise ValueError(
                "Invalid move: a player has already made a move at this position or the move is out of bounds")

    def get_updated_game_state(self, move: int):
        """
        Returns a new game state with the given move made
        :param move: the move to make
        :return: a new game state with the given move made
        """
        game = TicTacToe(board=self.board.copy(), current_player=self.current_player)
        game.game_history = self.game_history.copy()
        game.make_move(move)
        return game

    def get_possible_moves(self):
        """
        Finds all possible moves on the board
        :return: a list of possible moves
        """
        return [i for i in range(self.horizontal_size * self.vertical_size) if self.board[i] == 0]

    def get_last_move(self):
        """
        Gets the last move made in the game
        :return: the last move made in the game
        """
        return self.game_history[-1] if len(self.game_history) > 0 else None

    def reset(self):
        """
        Resets the game
        """
        self.board = np.zeros((self.horizontal_size * self.vertical_size), dtype=int)
        self.current_player = 1
        self.game_history = []

    def print_board(self):
        """
        Prints the current board
        """
        for i in range(self.vertical_size):
            print(self.board[i * self.horizontal_size:(i + 1) * self.horizontal_size])

if __name__ == "__main__":
    game = TicTacToe()
    game.make_move(1)
    game.make_move(0)
    game.make_move(3)
    game.make_move(2)
    game.make_move(5)
    game.make_move(6)
    game.make_move(4)
    print(game.game_history)
    print(game.return_winner())
    print(game.is_over)
    game.print_board()