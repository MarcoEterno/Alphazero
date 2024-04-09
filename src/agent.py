import numpy as np
from tictactoe import TicTacToe


class Agent:
    def __init__(self, game):
        self.game = game
    
    def get_move(self, game):
        pass

class RandomPlayer(Agent):
    def __init__(self,game):
        super().__init__(game)
    
    def get_move(self):
        possible_moves = self.game.get_possible_moves()[0]
        if len(possible_moves) > 0:
            return np.random.choice(possible_moves)
        else:
            # Handle the case when there are no possible moves
            # You might want to raise an exception or return a special value
            return None
    
    def play_one_game(self):
        """Agent plays one game of Tic Tac Toe against itself and returns the winner
        :param game: the game to play
        :return: the winner of the game
        """
        while True:
            if self.game.check_winner() != 0:
                return self.game.check_winner()
            if self.game.check_draw():
                return 0
            self.game.make_move(self.get_move())

if __name__ == "__main__":
    game = TicTacToe()
    player = RandomPlayer(game)
    while not game.is_over:
        move = player.get_move()
        game.make_move(move)
        game.board.print_board()
        print("current player: ", game.get_current_player())
        print(game.check_winner())
        print(game.check_draw())
