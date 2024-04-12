from typing import Optional

from board import Board


class TicTacToe:
    def __init__(self, board: Optional[Board] = None, current_player: int = 1):
        self.board = board if board is not None else Board()
        self.current_player = current_player

    def make_move(self, move: int):
        """
        Makes a move on the board for the current player and starts the turn to the other player
        :param move: the position to make the move at
        """
        self.board.make_move(move, self.current_player)
        self.current_player = -self.current_player

    def check_winner(self):
        """
        Checks if a player has won the game
        :return: the player that has won the game, 0 if no player has won
        """
        return self.board.check_winner()

    def check_draw(self):
        """
        Checks if the game is a draw
        :return: True if the game is a draw, False otherwise
        """
        return self.board.check_draw()

    @property
    def is_over(self):
        return self.check_winner() != 0 or self.check_draw()

    def get_possible_moves(self):
        """
        Gets all possible moves on the board
        :return: a list of possible moves
        """
        return self.board.get_possible_moves()

    def get_board(self):
        return self.board.get_board()

    def get_current_player(self):
        return self.current_player

    def reset(self):
        self.board = Board()
        self.current_player = 1


if __name__ == "__main__":
    game = TicTacToe()
    game.make_move(1)
    game.make_move(0)
    game.make_move(3)
    game.make_move(2)
    game.make_move(5)
    print(game.check_winner())
    print(game.check_draw())
    print(game.get_possible_moves())
    game.board.print_board()
