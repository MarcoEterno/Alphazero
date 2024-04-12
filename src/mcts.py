import copy
import logging

import numpy as np

from board import Board
from tictactoe import TicTacToe
from treenode import TreeNode


class MCTS:
    def __init__(self, game: TicTacToe, num_simulations=1000):
        """
        Initializes the MCTS algorithm
        :param game: the game to play
        :param agent: the agent to use for the simulations
        :param num_simulations: the number of simulations an agent will do before considering a move
        """
        self.game = game
        self.num_simulations = num_simulations
        self.root = TreeNode(game)
        self.current_node = self.root

    def search_leaf(self, node):
        """Searches for the best leaf node to expand
        :param node: the node to start the search from
        :return: the best leaf node
        """
        if len(node.children) == 0:
            return node
        else:
            return self.search_leaf(node.get_best_child())

    def rollout(self, node):
        """Simulates a random game from the current node to the end and returns the winner
        :param node: the node to simulate from
        """
        game = copy.deepcopy(node.game)
        while not game.is_over:
            moves = game.get_possible_moves()[0]
            move = np.random.choice(moves)
            game.make_move(move)
        return game.check_winner()

    def backpropagate(self, node, result):
        """Backpropagates the result of a simulation to the root nodes
        :param node: the node to start the backpropagation from
        :param result: the result of the simulation
        """
        while node != None:
            node.update(result)
            node = node.parent
            result *= -1  # a win for a player in a given node is a loss for the player in the parent node
        self.game.reset()

    def do_one_step(self, node):
        """
        Does one step of the MCTS algorithm
        :param node: the node to start the search from
        """
        new_node = self.search_leaf(node)
        # If the node has not been visited yet, we simulate the game from this node
        if new_node.visits == 0:
            if self.game.check_winner() == 0 and not self.game.check_draw():
                new_node.add_all_children()
            result = self.rollout(new_node)
            self.backpropagate(new_node, result)
        # If the node has been visited, we simulate the game from the best child node
        else:
            best_child = new_node.get_best_child()
            if best_child is None:
                return
            result = self.rollout(best_child)
            self.backpropagate(best_child, result)

    def build_tree(self, node):
        """
        Builds the tree of possible moves starting from the given node
        :param node: the node to start the tree from
        """
        for _ in range(self.num_simulations):
            self.do_one_step(node)

    def find_best_move_with_mcts(self, node):
        """
        Finds the best move using the MCTS algorithm
        :return: the best move to make
        """

        possible_moves = self.game.get_possible_moves()
        if len(possible_moves) == 0:
            logging.warning("No possible moves were found while searching for the best move with MCTS")
            return None
        self.build_tree(node)
        return node.get_best_move()

    def print_tree(self):
        """Prints the tree of moves played by the MCTS algorithm"""
        def print_node(node, indent):
            if node is None:
                return
            if node.visits != 0:
                print(f"{' ' * indent} State: {node.game_history} Visits: {node.visits}, Wins: {node.wins}")
            for child in node.children:
                print_node(child, indent + 4)

        print_node(self.root, 0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from agent import RandomPlayer

    board = Board()
    game = TicTacToe(board)
    agent = RandomPlayer(game)
    mcts = MCTS(game, num_simulations=100000)
    mcts.build_tree(mcts.root)
    mcts.print_tree()

    #BACK OF THE ENVELOPE CALCULATIONS FOR THE NUMBER OF NODES IN THE TREE
    # N_NODES ~= 9!/(5!*4!)/(SIMME>TRIES) = 9*8*7*6/(4*3*2)/SIMMETRIES = 126/SIMMETRIES = 126/8 = 15.75
    # TOTAL_NODES IN BASE ALGORITHM = 9! = 362880
