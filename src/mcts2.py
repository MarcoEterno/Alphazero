import copy
import logging
from typing import Optional

import numpy as np

from utils import timer
from tictactoe2 import TicTacToe
from treenode2 import Node


class MCTS:
    def __init__(self, game: TicTacToe, num_simulations=1000):
        """
        Initializes the MCTS algorithm
        :param game: the game to play
        :param num_simulations: the number of simulations an agent will do before considering a move
        """
        self.game = game
        self.num_simulations = num_simulations
        self.root = Node(game)

    def search_leaf(self, node):
        """Searches the tree for the best leaf node to expand
        :param node: the node to start the search from
        :return: the best leaf node
        """
        if len(node.children) == 0:
            return node
        else:
            best_move = node.get_best_move_from_possible_children() # function already checks if the move is possible

            if best_move is not None:
                return self.search_leaf(node.children[best_move])
            return node

    def rollout(self, node):
        """Simulates a random game from the current node to the end and returns the winner
        :param node: the node to simulate from
        """
        if node is None:
            logging.warning("Node is None in rollout")
            return 0
        game = copy.deepcopy(node.game_state)
        while not game.is_over:
            moves = game.get_possible_moves()
            move = np.random.choice(moves)
            game.make_move(move)
        return game.return_winner()

    def backpropagate(self, node, result):
        """Backpropagates the result of a simulation to the root nodes
        :param node: the node to start the backpropagation from
        :param result: the result of the simulation
        """
        while node != None:
            node.visits += 1
            node.wins += result
            node = node.parent
            result *= -1  # a win for a player in a given node is a loss for the player in the parent node

    def do_one_step(self, node: Optional[Node] = None):
        """
        Does one step of the MCTS algorithm
        """
        node = self.root if node is None else node
        leaf = self.search_leaf(node)
        if leaf.visits > 0:
            leaf.add_all_children()
            if leaf.best_child:
                result = self.rollout(leaf.best_child)
                self.backpropagate(leaf.best_child, result)
        if leaf.visits == 0:
            result = self.rollout(leaf)
            self.backpropagate(leaf, result)
    @timer
    def build_mcts_tree(self, node: Optional[Node] = None):
        """
        Builds the MCTS tree by doing num_simulations steps
        :param node: the node to start the tree building from
        """
        node = self.root if node is None else node
        for _ in range(self.num_simulations):
            self.do_one_step()

    @timer
    def print_tree(self, node: Optional[Node] = None):
        """Prints the tree of moves played by the MCTS algorithm"""
        def print_node(node, indent):
            if node is None:
                return
            if node.visits != 0:
                print(f"{' ' * indent} State: {node.game_state.game_history} Visits: {node.visits}, Wins: {node.wins}")
            for child in node.children.values():
                print_node(child, indent + 4)

        node = self.root if node is None else node
        print_node(node, 0)

    def find_best_move_with_mcts(self, node: Node):
        """
        Finds the best move using the MCTS algorithm
        :param node: the node to start the search from
        :return: the best move
        """
        self.build_mcts_tree(node)
        return node.get_best_move_from_possible_children()



if __name__ == "__main__":
    game = TicTacToe()
    mcts = MCTS(game, num_simulations=1000000)
    mcts.build_mcts_tree()
    mcts.print_tree()