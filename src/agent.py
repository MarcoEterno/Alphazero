import copy
import logging
from typing import Optional

import numpy as np

from board import Board
from mcts import MCTS
from tictactoe import TicTacToe

logging.basicConfig(level=logging.INFO)


class Agent:
    def __init__(self, game: Optional[TicTacToe] = None):
        self.game = game if game is not None else TicTacToe()

    def choose_random_move(self, game: Optional[TicTacToe] = None):
        """
        Chooses a random move from the possible moves
        :return: a random move from the possible moves
        """
        game = game if game is not None else self.game
        possible_moves = game.get_possible_moves()[0]
        if len(possible_moves) > 0:
            return np.random.choice(possible_moves)
        else:
            return None

    def play_one_game(self, game: Optional[TicTacToe] = None, play_random: bool = False):
        """Agent plays one game of Tic Tac Toe against itself and returns the winner
        :return: the winner of the game
        """
        game = game if game is not None else copy.deepcopy(self.game)
        while True:
            if game.check_winner() != 0:
                winner = self.game.check_winner()
                del game
                return winner
            if game.check_draw():
                del game
                return 0
            # if neither of the above conditions are true, the game is still ongoing and a move can be made
            if play_random:
                next_move = self.choose_random_move()
            else:
                next_move = self.get_move()
            if next_move is None:
                logging.error(
                    "No possible moves left in the game, even though check_winner() and check_draw() returned False")
                break
            self.game.make_move(next_move)

    def get_move(self):
        pass


class MCTSAgent(Agent):
    def __init__(self, game: Optional[TicTacToe], mcts: Optional[MCTS] = None, num_simulations=1000):
        """
        Initializes the MCTS agent
        :param game: the game to play
        :param mcts: the mcts object to use for the agent
        :param num_simulations: the number of simulations to run for each move
        """
        super().__init__(game if game is not None else TicTacToe())
        self.mcts = mcts if (not mcts is None) else MCTS(game, self, num_simulations)
        self.num_simulations = num_simulations

    def get_move(self, game: Optional[TicTacToe] = None):
        """
        Gets the best move for the current player using the MCTS algorithm
        :return: the best move for the current player if there are possible moves, None otherwise
        """
        game = game if game is not None else copy.deepcopy(self.game)
        possible_moves = game.get_possible_moves()[0]
        if len(possible_moves) > 0:
            return self.mcts.find_best_move_with_mcts(self.mcts.)
        else:
            # Handle the case when there are no possible moves
            # You might want to raise an exception or return a special value
            return None


class RandomPlayer(Agent):
    def __init__(self, game):
        super().__init__(game)

    def get_move(self):
        possible_moves = self.game.get_possible_moves()[0]
        if len(possible_moves) > 0:
            return np.random.choice(possible_moves)
        else:
            # Handle the case when there are no possible moves
            # You might want to raise an exception or return a special value
            return None


if __name__ == "__main__":
    board = Board()
    game = TicTacToe(board)
    mcts = MCTS(game)
    mcts_player = MCTSAgent(game=game, mcts=mcts, num_simulations=1000)
    mcts_player.mcts.build_tree(mcts_player.mcts.root)
    mcts_player.mcts.print_tree()

    for i in range(5):
        move = mcts_player.get_move()
        print(move)
        mcts_player.game.make_move(move)
        mcts_player.game.board.print_board()
