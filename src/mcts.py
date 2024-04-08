import numpy as np
import copy

from board import Board
from tictactoe import TicTacToe
from agent import Agent, RandomPlayer
from treenode import TreeNode



class MCTS:
    def __init__(self, game: TicTacToe, agent: Agent, num_simulations=1000):
        self.game = game
        self.num_simulations = num_simulations
        self.agent = agent
        self.root = TreeNode(game)
    
    def search_leaf(self, node):
        if len(node.children) == 0:
            return node
        else:
            move = node.get_best_move()
            self.game.make_move(move)
            return self.search_leaf(node.get_best_child())
    
    def rollout(self, node):
        """Simulates a game from the current node to the end and returns the winner
        :param node: the node to simulate from
        """
        game = copy.deepcopy(node.game) # 
        if game.check_winner() != 0:
            return game.check_winner()
        winner = self.agent.play_one_game(game)
        return winner
        
    def backpropagate(self, node, result):
        while node != None:
            node.update(result)
            node = node.parent
        self.game.reset()
    
    def do_one_step(self, node):
        game = copy.deepcopy(node.game)
        node = self.search_leaf(node)
        if node.visits == 0:
            node.add_all_children()
            result = self.rollout(node)
            self.backpropagate(node, result)
        else:
            if game.check_winner() != 0:
                return node.game.check_winner()
            elif game.check_draw():
                return 0
            else:
                new_game = copy.deepcopy(node.game)
                new_game.make_move(self.agent.get_move(new_game))
                return self.simulate(TreeNode(new_game))
    
    def find_best_move_with_mcts(self):
        while self.num_simulations > 0:
            self.do_one_step(self.root)
            self.num_simulations -= 1
        
        return self.root.get_best_move()

if __name__ == "__main__":
    game = TicTacToe()
    agent = RandomPlayer()
    mcts = MCTS(game, agent)
    best_move = mcts.find_best_move_with_mcts()
    print(best_move)