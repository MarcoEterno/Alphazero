import pickle
import numpy as np

from mcts2 import MCTS
from tictactoe2 import TicTacToe
from treenode2 import Node

def save_node(node):
    with open('node.pkl', 'wb') as f:
        pickle.dump(node, f)

def load_node():
    with open('node.pkl', 'rb') as f:
        return pickle.load(f)

def save_mcts(mcts):
    with open('mcts.pkl', 'wb') as f:
        pickle.dump(mcts, f)

def load_mcts():
    with open('mcts.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    game = TicTacToe()
    node = Node(game)
    game.make_move(0)
    print(node.game_state.board)
    save_node(node)
    node2 = load_node()
    print(node2.game_state.board)
    mcts = MCTS(game)
    mcts.root = node
    print(mcts.root.game_state.board)
    mcts.root.add_child_given_move(2)
    print(mcts.root.children[2].game_state.board)
    save_mcts(mcts)
    mcts2 = load_mcts()
    print(mcts2.root.children[2].game_state.board)
    print(mcts2.root.children)



