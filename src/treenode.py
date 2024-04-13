import copy

import numpy as np

from tictactoe import TicTacToe


class TreeNode:
    def __init__(self, game, parent=None):
        self.game = game
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.game_history = parent.game_history + [self.last_move] if parent is not None else []

    @property
    def last_move(self):
        return abs(self.game.board.board - self.parent.game.board.board).argmax()

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def update(self, result):
        self.visits += 1
        self.wins += result

    def get_ucb(self):
        if self.visits == 0:
            return float('inf')
        if self.parent is None:
            return self.wins / self.visits
        else:
            return self.wins / self.visits + np.sqrt(2 * np.log(self.parent.visits) / self.visits)

    def get_best_move(self):
        best_children = max(self.children, key=lambda x: x.ucb())
        # given the board is a 1D array, we can find the move played by finding the index of the board  where the parent and the child differ
        return abs(best_children.game.board.board - self.game.board.board).argmax()

    def get_best_child(self):
        """
        Returns the child with the highest UCB value from the list of children.
        if there are no children, return None
        :return: the child with the highest UCB value
        """
        return max(self.children, key=lambda x: x.ucb()) if len(self.children) > 0 else None

    def add_all_children(self):
        for move in self.game.get_possible_moves()[0]:
            new_game = copy.deepcopy(self.game)
            new_game.make_move(move)
            self.add_child(TreeNode(new_game, self))

    def __repr__(self):
        # returns all the keys and values in the object dictionary
        return f"State: {self.game_history}, Visits: {self.visits}, Wins: {self.wins}, UCB: {self.get_ucb()}"

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
