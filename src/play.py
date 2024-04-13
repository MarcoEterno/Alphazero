from agent import Agent, MCTSAgent
from tictactoe import TicTacToe


def play_one_game(game: TicTacToe, agent1: Agent, agent2: Agent, current_player: int = 1, print_board: bool = False):
    """
    Plays one game of Tic Tac Toe between two agents
    :param agent1: the first agent
    :param agent2: the second agent
    :param current_player: the player that starts the game (1 or 2)
    :param print_board: whether to print the board after each move
    :return: the winner of the game
    """
    if current_player not in [1, -1]:
        raise ValueError("Invalid player: player must be 1 or -1")
    while not game.is_over:
        if game.current_player == 1:
            move = agent1.get_move()
        else:
            move = agent2.get_move()
        game.make_move(move)
        if print_board:
            game.board.print_board()
            print("current player: ", game.current_player)
            print("Winner: ", game.check_winner())
            print("Draw: ", game.check_draw())
    return game.check_winner()


if __name__ == "__main__":
    game = TicTacToe()
    agent1 = MCTSAgent(game, num_simulations=1000)
    agent2 = MCTSAgent(game, num_simulations=1000)
    play_one_game(game, agent1, agent2, print_board=True)
    print("Winner: ", game.check_winner())
    print("Draw: ", game.check_draw())
