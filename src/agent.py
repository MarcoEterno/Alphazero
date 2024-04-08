import numpy as np
from tictactoe import TicTacToe


class Agent:
    def __init__(self):
        pass
    
    def get_move(self, game):
        pass

class RandomPlayer(Agent):
    def __init__(self):
        pass
    
    def get_move(self, game: TicTacToe):
        return np.random.choice(game.get_possible_moves()[0])
    
    def play_one_game(self, game):
        """Agent plays one game of Tic Tac Toe against itself and returns the winner
        :param game: the game to play
        :return: the winner of the game
        """
        while True:
            if game.check_winner() != 0:
                return game.check_winner()
            if game.check_draw():
                return 0
            game.make_move(self.get_move(game))

if __name__ == "__main__":
    game = TicTacToe()
    player = RandomPlayer()
    while game.check_winner() == 0 and not game.check_draw():
        move = player.get_move(game)
        game.make_move(move)
        game.board.print_board()
        print("current player: ", game.get_current_player())
        print(game.check_winner())
        print(game.check_draw())
