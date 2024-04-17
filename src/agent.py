import copy
import logging
from typing import Optional

import numpy as np

from mcts import MCTS
from tictactoe import TicTacToe
from treenode import Node
from saver import load_mcts, save_mcts


class Agent:
    @staticmethod
    def return_winner_match(
            agent1,
            agent2,
            game: TicTacToe = None,
            print_game: bool = False,
            print_mcts_move_evals: bool = False):
        """
        Plays a game between two agents and returns the winner
        :param agent1: the first agent
        :param agent2: the second agent
        :param game: the game to play
        :return: the winner of the game, 0 if it is a draw
        """
        game = copy.deepcopy(game) if game is not None else TicTacToe()
        players = [agent1, agent2]
        current_player = 0
        while not game.is_over:
            move = players[current_player].get_move(game)
            game.make_move(move)
            current_player = 1 - current_player
            if print_game:
                game.print_board()
                if (game.is_over):
                    print("Winner:", game.return_winner())
        return game.return_winner()

    @staticmethod
    def play_multiple_matches(
            agent1,
            agent2,
            num_games: int,
            print_game: bool = False,
            print_mcts_move_evals: bool = False):
        """
        Plays multiple games between two agents
        :param agent1: the first agent
        :param agent2: the second agent
        :param num_games: the number of games to play
        :return: a dictionary with the number of wins for each player and the number of draws
        """
        wins = {0: 0, 1: 0, -1: 0}
        for _ in range(num_games):
            winner = Agent.return_winner_match(agent1, agent2, print_game=print_game)
            wins[winner] += 1
        return wins

    def __init__(self, game: Optional[TicTacToe] = None):
        self.game = game if game is not None else TicTacToe()

    def choose_random_move(self, game: Optional[TicTacToe] = None):
        """
        Chooses a random move from the possible moves
        :return: a random move from the possible moves
        """
        game = game if game is not None else self.game
        possible_moves = game.get_possible_moves()
        if len(possible_moves) > 0:
            return np.random.choice(possible_moves)
        else:
            logging.waring("No possible moves left in the game")
            return None

    def play_one_game_vs_itself(self,
                                game: Optional[TicTacToe] = None,
                                play_random: bool = False,
                                print_game: bool = False):
        """Agent plays one game of Tic Tac Toe against itself
        :return: the winner of the game
        """
        game = copy.deepcopy(game if game is not None else self.game)
        while not game.is_over:
            # if neither of the above conditions are true, the game is still ongoing and a move can be made
            if play_random:
                next_move = self.choose_random_move(game)
            else:
                next_move = self.get_move(game)
            if next_move is None:
                logging.error(
                    "No possible moves left in the game, even though check_winner() and check_draw() returned False")
                break
            game.make_move(next_move)
            if print_game:
                game.print_board()
            if game.return_winner() is not None:
                winner = game.return_winner()
                del game
                return winner

    def get_move(self):
        pass


class RandomAgent(Agent):
    def get_move(self, game: Optional[TicTacToe] = None):
        """
        Chooses a random move from the possible moves but does not play it
        :param game:
        :return:
        """
        return self.choose_random_move(game)


class MCTSAgent(Agent):
    def __init__(self, game: Optional[TicTacToe] = None, mcts: Optional[MCTS] = None, num_simulations=1000):
        """
        Initializes the MCTS agent
        :param game: the game to play
        :param mcts: the mcts object to use for the agent
        :param num_simulations: the number of simulations to run for each move
        """
        super().__init__(game if game is not None else TicTacToe())
        self.mcts = mcts if (not mcts is None) else MCTS(game, num_simulations)

    def get_move(self, game: Optional[TicTacToe] = None):
        """
        Chooses the best move according to the MCTS algorithm
        :param game: the game to play
        :return: the best move
        """
        game = game if game is not None else self.game
        self.mcts.root = Node(game_state=game)
        best_move = self.mcts.find_best_move_with_mcts(node=self.mcts.root)
        return best_move


class HumanAgent(Agent):
    def get_move(self, game: Optional[TicTacToe] = None):
        """
        Gets the move from the human player
        :param game: the game to play
        :return: the move from the human player
        """
        game = game if game is not None else self.game
        move = int(input("Enter your move as integer in range [0,8]: "))
        return move


if __name__ == "__main__":
    game = TicTacToe()
    mcts = MCTS(game, num_simulations=10000)
    mcts = load_mcts(mcts, num_simulations=100000)
    mcts_player = MCTSAgent(game=game, mcts=mcts)
    human_player = HumanAgent(game=game)
    random_player = RandomAgent(game=game)
    print(Agent.play_multiple_matches(mcts_player, random_player, num_games=3, print_game=True))
    # print(Agent.return_winner_match(mcts_player, random_player, game, print_game=True))
