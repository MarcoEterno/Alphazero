import numpy as np
import copy

from tictactoe import TicTacToe


class TreeNode:
    def __init__(self, game, parent=None):
        self.game = game
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
    
    def add_child(self, child):
        self.children.append(child)
    
    def update(self, result):
        self.visits += 1
        self.wins += result
    
    def get_ucb(self):
        return float('inf') if self.visits==0 else self.wins/self.visits + np.sqrt(2*np.log(self.parent.visits)/self.visits)
    
    def get_best_move(self):
        best_children = max(self.children, key=lambda x: x.get_ucb())
        # given the board is a 1D array, we can find the move played by finding the index of the board  where the parent and the child differ
        return abs(best_children.game.board.board - self.game.board.board).argmax()
    
    def get_best_child(self):
        return max(self.children, key=lambda x: x.get_ucb())
    
    def add_all_children(self):
        for move in self.game.get_possible_moves()[0]:
            new_game = copy.deepcopy(self.game)
            new_game.make_move(move)
            self.add_child(TreeNode(new_game, self))
    def __repr__(self):
        # returns all the keys and values in the object dictionary
        dictionary = {}
        for key, value in self.__dict__.items():
            dictionary[key] = value
        return str(dictionary)
    
    def __str__(self):
        return self.__dict__.__str__()
    
    def print(self):
        print(self.visits, self.wins, self.get_ucb())
        
            


if __name__ == "__main__":
    game = TicTacToe()
    root = TreeNode(game)
    root.add_all_children()
    for child in root.children:
        child.print()
    print(root.get_best_move())